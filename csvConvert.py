import pyshark
import pandas as pd
def convert(pcap_in):
    data = []
    csv_output = "wireshark_dataframe.csv"
    pcap_in = pyshark.FileCapture(pcap_in, display_filter="tcp")
    #filter our wireshark file via tcp traffic only
    for packet in pcap_in:
        try:
            #after the filter we take only the data we need to make our analysis
            timestamp = packet.sniff_time
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            src_port = packet.tcp.srcport
            dst_port = packet.tcp.dstport
            seq = packet.tcp.seq
            ack = packet.tcp.ack
            window_size = packet.tcp.window_size_value
            flags = packet.tcp.flags


            data.append([timestamp, src_ip, dst_ip, src_port, dst_port, seq, ack, window_size, flags])

        except AttributeError:
            continue

    df = pd.DataFrame(data, columns=["Timestamp", "Source IP", "Destination IP", "Source Port", "Destination Port",
                                     "Sequence", "Ack Number", "Window", "Flags"])
    df.to_csv(csv_output, index=False)
    print(f"Data saved to {csv_output}")