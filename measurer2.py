"""
OF 1.0 - POX end-to-end latency measurer

"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
import os
import datetime
import time
import traceback
from service_thread import ServiceThread

log = core.getLogger()

#XXX SOLVED
#XXX: Are you going to set s always True? shouldn't we swap?
#XXX: I have my doubts aobout if it's going to work. You are calling metwork_measurer.switch statically without getting the instance, maybe you should pass the network_measurer instance as method param.
def handle_timer(message, nm):
    print "\n"+mcolors.OKGREEN+"INFO: %s" % message, mcolors.ENDC

    if nm.switched == True:
        nm.switched = False
        message2 = "Link Failure Simulation Raised at: %s" % get_time_now()
    else:
        nm.switched = True
        message2 = "Link Failure Simulation Raised at: %s" % get_time_now()

    ServiceThread.start_in_new_thread(network_measurer.logger_thread, message2)
    flow_flush()


    return

#XXX works(pox wiki points it that way) - I'm not sure if its going to work also, probably you should pass the network measurer instance and get the connections from there.
def flow_flush():
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)

    for connection in core.openflow.connections:
        connection.send(msg)
        log.info("-> Clearing all flows from %s!" % (dpidToStr(connection.dpid),))

def get_time_now():
    return str(datetime.datetime.now().strftime('%M:%S.%f')[:-3])


class mcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKGREEN = ''
        self.FAIL = ''
        self.ENDC = ''


class network_measurer(object):

    switched = False

    def __init__(self, reactive, ignore=None):
        """
        Initialize

        See LearningSwitch for meaning of 'transparent'
        'reactive' indicates how
        'ignore' is an optional list/set of DPIDs to ignore
        """
        log.info(" Initializing Measurer")
        core.openflow.addListeners(self)
        self.reactive = reactive
        self.ignore = set(ignore) if ignore else ()

        if self.reactive:
            core.openflow.addListenerByName("PacketIn", self._handle_PacketIn)
        else:
            None    #core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)

        log.info(" Measurer Initialized")


    def logger(self, message):
        #XXX SOLVED! - We need a lot of accuracy on our measurements, I think we should start the method in a new Thread.
        #XXX look at the service_thread.py on this directory
        #XXX In example we could decouple logger method in another static class (Logger) and thencall ServiceThread.star_in_new_thread(Logger.log_measurement, message)
        ServiceThread.start_in_new_thread(network_measurer.logger_thread, message)


    @staticmethod
    def logger_thread(message, log_file="./time_log.txt"):
        if os.path.exists(log_file):
            l = open(log_file, 'a')
            l.write(message+"\n")

        else:
            l = open(log_file, 'wb')
            l.write(message+"\n")
        l.close()


    def _handle_PacketIn(self, event):
        """
        OF 1.0 compatible flowmod messages for the switches
        """
        log.info(" Packet-in Event: DPID %s Port:%d" % (dpidToStr(event.dpid), event.port))
        log.info(" Link fail status: %s" % str(self.switched))
        #message = str(datetime.datetime.now())

        eth_headers = event.parse() #Ethernet part of the packet L2

        #if eth_headers != pkt.ethernet.LLDP_TYPE:
        vlan_headers = eth_headers.next #VLAN part of the Packet L2
        log.info("VLAN Header found: %s" % str(vlan_headers.id))
        vlan_id = vlan_headers.id

        if network_measurer.switched:

            if (event.dpid == 2) and (vlan_id == 1550):
                if event.port == 7:
                    message = "B-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # start-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    msg.actions.append(of.ofp_action_output(port=2))
                    event.connection.send(msg)
                    log.info("Forwarding B, [@Tx] => S2.P7 -> S2.P2")

                elif event.port == 4:
                    message = "B-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # start-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    msg.actions.append(of.ofp_action_output(port=2))
                    event.connection.send(msg)
                    log.info("Forwarding B, [@Tx] => S2.P4 -> S2.P2")

                elif event.port == 6:
                    message = "B-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # start-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    msg.actions.append(of.ofp_action_output(port=2))
                    event.connection.send(msg)
                    log.info("Forwarding B, [@Tx] => S2.P6 -> S2.P2")

                elif event.port == 1:
                    message = "B-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # start-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    msg.actions.append(of.ofp_action_output(port=2))
                    event.connection.send(msg)
                    log.info("Forwarding B, [@Tx] => S2.P1 -> S2.P2")

                else:
                    log.info("Packet-In From in DPID %d port %d" % (event.dpid, event.port))

            if (event.dpid == 5) and (vlan_id == 1550):
                if event.port == 6:
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    msg.actions.append(of.ofp_action_output(port=5))
                    event.connection.send(msg)
                    log.info("Forwarding B, [@S2.P2] => S5.P6 -> S5.P5")

            if (event.dpid == 4) and (vlan_id == 1550):
                if event.port == 7:
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.actions.append(of.ofp_action_output(port=4))
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    event.connection.send(msg)
                    log.info("Forwarding B, [@S5.P6] => S4.P7 -> S3.P6")

            if (event.dpid == 3) and (vlan_id == 1550):
                if event.port == 6:
                    message = "B-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # end-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.actions.append(of.ofp_action_output(port=7))
                    #msg.actions.append(of.ofp_action_output(port=3))
                    #msg.actions.append(of.ofp_action_output(port=5))
                    #msg.actions.append(of.ofp_action_output(port=2))
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    event.connection.send(msg)
                    log.info("Forwarding B, [@S4.P4] => S3.P6 -> S3.P7")

        else:
            # switched is False!!!
            if (event.dpid == 2) and (vlan_id == 1550):
                if event.port == 7:
                    message = "A-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # start-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    msg.actions.append(of.ofp_action_output(port=3))
                    event.connection.send(msg)
                    log.info("Forwarding A, [@Tx] => S2.P7 -> S2.P3")

                elif event.port == 4:
                    message = "A-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # start-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    msg.actions.append(of.ofp_action_output(port=3))
                    event.connection.send(msg)
                    log.info("Forwarding A, [@Tx] => S2.P4 -> S2.P3")

                elif event.port == 6:
                    message = "A-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # start-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    msg.actions.append(of.ofp_action_output(port=3))
                    event.connection.send(msg)
                    log.info("Forwarding A, [@Tx] => S2.P6 -> S2.P3")

                elif event.port == 1:
                    message = "A-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # start-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    msg.actions.append(of.ofp_action_output(port=3))
                    event.connection.send(msg)
                    log.info("Forwarding A, [@Tx] => S2.P1 -> S2.P3")

                else:
                    log.info("Packet-In From in DPID %d port %d" % (event.dpid, event.port))

            if (event.dpid == 1) and (vlan_id == 1550):
                if event.port == 1:
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.actions.append(of.ofp_action_output(port=6))
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    event.connection.send(msg)
                    log.info("Forwarding A, [@S2.P3] => S1.P1 -> S1.P6")

            if (event.dpid == 4) and (vlan_id == 1550):
                if event.port == 6:
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.actions.append(of.ofp_action_output(port=4))
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    event.connection.send(msg)
                    log.info("Forwarding A, [@S1.P6] => S4.P6 -> S4.P4")


            if (event.dpid == 3) and (vlan_id == 1550):
                if event.port == 6:
                    message = "A-Packet_In DPID:%s Time: %s " % (dpidToStr(event.dpid), get_time_now())
                    self.logger(message)
                    log.info("Flowmoding %s", dpidToStr(event.dpid))
                    # end-point switch
                    msg = of.ofp_flow_mod()
                    msg.match = of.ofp_match(in_port=event.port, dl_vlan=1550)
                    msg.actions.append(of.ofp_action_output(port=7))
                    #msg.actions.append(of.ofp_action_output(port=3))
                    #msg.actions.append(of.ofp_action_output(port=5))
                    #msg.actions.append(of.ofp_action_output(port=2))
                    msg.idle_timeout = 200
                    msg.hard_timeout = 200
                    event.connection.send(msg)
                    log.info("Forwarding A, [@S4.P4] => S3.P6 -> S3.P7")


def launch(reactive=False):
    global start_time
    start_time = datetime.datetime.now()
    print "start_time: ", start_time

    log.info(" Registering Measurement App")
    core.registerNew(network_measurer, reactive)

    Timer(10, handle_timer, args=["10 SECONDS - SWITCHING PATHS", network_measurer], recurring=True)

