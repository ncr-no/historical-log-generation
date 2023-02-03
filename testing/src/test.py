pkts = rdpcap('packet.pcap')
oneMonth = 2630000
newPackets=[]
for packet in pkts:
  packet.time = packet.time - oneMonth
  packetModified=packet
  newPackets.append(packetModified)