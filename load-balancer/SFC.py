from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ether
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.app.wsgi import ControllerBase
from ryu.app.wsgi import Response
from ryu.app.wsgi import route
from ryu.app.wsgi import WSGIApplication
from ryu.lib import dpid as dpid_lib
from netaddr import IPAddress

SFC_dict = {
    "001": [
        {
            "dpid": "0000000000000001",
            "flows": [
                {"ipv4_src": "10.0.0.1", "in_port": 11, "out_port": 2},
                {"ipv4_dst": "10.0.0.1", "in_port": 2, "out_port": 11}]
        }, {
            "dpid": "0000000000000002",
            "flows": [
                {"ipv4_src": "10.0.0.1", "in_port": 1, "out_port": 2},
                {"ipv4_dst": "10.0.0.1", "in_port": 2, "out_port": 1}]
        }, {
            "dpid": "0000000000000003",
            "flows": [
                {"ipv4_src": "10.0.0.1", "in_port": 2, "out_port": 11},
                {"ipv4_dst": "10.0.0.1", "in_port": 11, "out_port": 2}]
        }
    ],
    "002": [
        {
            "dpid": "0000000000000001",
            "flows": [
                {"ipv4_src": "10.0.0.2", "in_port": 12, "out_port": 1},
                {"ipv4_dst": "10.0.0.2", "in_port": 1, "out_port": 12}]
        }, {
            "dpid": "0000000000000003",
            "flows": [
                {"ipv4_src": "10.0.0.2", "in_port": 1, "out_port": 12},
                {"ipv4_dst": "10.0.0.2", "in_port": 12, "out_port": 1}]
        }
    ]
}

simple_switch_instance_name = 'simple_switch_app'
url = '/sfc/manage/{sfcid}'
SFCID_PATTERN = r'[0-9]{3}'


class SimpleSwitchSFC13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitchSFC13, self).__init__(*args, **kwargs)
        self.switches = {}
        self.mac_to_port = {}
        wsgi = kwargs['wsgi']
        wsgi.register(SFCController,
                      {simple_switch_instance_name: self})

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    def del_flow(self, datapath, match):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        mod = parser.OFPFlowMod(datapath=datapath,
                                command=ofproto.OFPFC_DELETE,
                                out_port=ofproto.OFPP_ANY,
                                out_group=ofproto.OFPG_ANY,
                                match=match)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        self.switches[datapath.id] = datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(eth_type=ether.ETH_TYPE_ARP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src

        dpid = format(datapath.id, "d").zfill(16)
        self.mac_to_port.setdefault(dpid, {})

        if eth.ethertype != ether_types.ETH_TYPE_ARP:
            return

        if src in self.mac_to_port[dpid] and self.mac_to_port[dpid][src] != in_port:
            return

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(eth_type=ether.ETH_TYPE_ARP, in_port=in_port, eth_dst=dst, eth_src=src)
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    def manage_sfc_flow(self, dpid, flow, add=True):
        datapath = self.switches.get(dpid)
        if datapath is None:
            return

        parser = datapath.ofproto_parser
        if "ipv4_src" in flow:
            match = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP, in_port=flow["in_port"], ipv4_src=IPAddress(flow["ipv4_src"]))
            if add:
                actions = [parser.OFPActionOutput(flow["out_port"])]
                self.add_flow(datapath, 1, match, actions)
            else:
                self.del_flow(datapath, match)
        elif "ipv4_dst" in flow:
            match = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP, in_port=flow["in_port"], ipv4_dst=IPAddress(flow["ipv4_dst"]))
            if add:
                actions = [parser.OFPActionOutput(flow["out_port"])]
                self.add_flow(datapath, 1, match, actions)
            else:
                self.del_flow(datapath, match)


class SFCController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SFCController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data[simple_switch_instance_name]

    @route('sfc', url, methods=['PUT'], requirements={'sfcid': SFCID_PATTERN})
    def add_sfc(self, req, **kwargs):

        simple_switch = self.simple_switch_app
        sfcid = kwargs['sfcid']
        if sfcid not in SFC_dict:
            return Response(status=404)

        sfc = SFC_dict[sfcid]
        for hop in sfc:
            dpid = dpid_lib.str_to_dpid(hop["dpid"])
            for flow in hop["flows"]:
                simple_switch.manage_sfc_flow(dpid, flow, add=True)
        return Response(status=200)

    @route('sfc', url, methods=['DELETE'], requirements={'sfcid': SFCID_PATTERN})
    def del_sfc(self, req, **kwargs):

        simple_switch = self.simple_switch_app
        sfcid = kwargs['sfcid']
        if sfcid not in SFC_dict:
            return Response(status=404)

        sfc = SFC_dict[sfcid]
        for hop in sfc:
            dpid = dpid_lib.str_to_dpid(hop["dpid"])
            for flow in hop["flows"]:
                simple_switch.manage_sfc_flow(dpid, flow, add=False)
        return Response(status=200)


