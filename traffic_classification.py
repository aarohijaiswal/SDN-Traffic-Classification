from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ipv4

log = core.getLogger()

# Traffic counters
traffic_stats = {
    "ICMP": 0,
    "TCP": 0,
    "UDP": 0,
    "OTHER": 0
}

def _handle_PacketIn(event):
    try:
        packet = event.parsed
        if not packet.parsed:
            return

        ip_packet = packet.find('ipv4')

        if ip_packet:
            # ✅ Classification
            if ip_packet.protocol == ipv4.ICMP_PROTOCOL:
                traffic_stats["ICMP"] += 1
                proto = "ICMP"

            elif ip_packet.protocol == ipv4.TCP_PROTOCOL:
                traffic_stats["TCP"] += 1
                proto = "TCP"

            elif ip_packet.protocol == ipv4.UDP_PROTOCOL:
                traffic_stats["UDP"] += 1
                proto = "UDP"

            else:
                traffic_stats["OTHER"] += 1
                proto = "OTHER"

            log.info("Packet Classified: %s", proto)

            # ✅ Statistics
            log.info("Stats -> ICMP:%s TCP:%s UDP:%s OTHER:%s",
                     traffic_stats["ICMP"],
                     traffic_stats["TCP"],
                     traffic_stats["UDP"],
                     traffic_stats["OTHER"])

            # 🔥 TRAFFIC DISTRIBUTION ANALYSIS
            total = sum(traffic_stats.values())

            if total > 0:
                icmp_p = (traffic_stats["ICMP"] / total) * 100
                tcp_p = (traffic_stats["TCP"] / total) * 100
                udp_p = (traffic_stats["UDP"] / total) * 100

                log.info("Traffic Distribution -> ICMP: %.2f%% | TCP: %.2f%% | UDP: %.2f%%",
                         icmp_p, tcp_p, udp_p)

                # ✅ Dominant traffic
                dominant = max(traffic_stats, key=traffic_stats.get)
                log.info("Dominant Traffic Type: %s", dominant)

        # ✅ Install flow rule
        flow_msg = of.ofp_flow_mod()
        flow_msg.match = of.ofp_match.from_packet(packet)
        flow_msg.idle_timeout = 10
        flow_msg.hard_timeout = 30
        flow_msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(flow_msg)

        # ✅ Forward current packet (IMPORTANT)
        packet_out = of.ofp_packet_out()
        packet_out.data = event.ofp
        packet_out.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(packet_out)

    except:
        # ✅ Prevent crash (Python 3.12 + POX issue)
        return


def launch():
    log.info("Traffic Classification Controller Started")
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)