#!/usr/bin/python
import sys
import socket
import fcntl
import struct
import array
from netaddr import IPNetwork, IPAddress

def all_interfaces():
    is_64bits = sys.maxsize > 2**32
    struct_size = 40 if is_64bits else 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    max_possible = 8 # initial value
    while True:
        bytes = max_possible * struct_size
        names = array.array('B', '\0' * bytes)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            s.fileno(),
            0x8912,  # SIOCGIFCONF
            struct.pack('iL', bytes, names.buffer_info()[0])
        ))[0]
        if outbytes == bytes:
            max_possible *= 2
        else:
            break
    namestr = names.tostring()
    return [(namestr[i:i+16].split('\0', 1)[0],
             socket.inet_ntoa(namestr[i+20:i+24]))
            for i in range(0, outbytes, struct_size)]

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

def getHostname(ip):
  try:
    return socket.gethostbyaddr(ip)[0]
  except socket.herror:
    return "None"

def getNetSize(netmask):
    binary_str = ''
    for octet in netmask.split("."):
        binary_str += bin(int(octet))[2:].zfill(8)
    return len(binary_str.rstrip('0'))

def getNetwork(ip, networks):
  addr = IPAddress(ip)
  for name, net in networks.iteritems():
    CIDR = getNetSize(net[1])
    if addr in IPNetwork("%s/%d" % (net[0], CIDR)):
      return name
  return "Unknown"

networks = {"CS Departmental Servers":("130.85.88.65","255.255.255.224"),
  "CS Dynamic Departmental Clients":("130.85.93.1","255.255.255.128"),
  "CS Static Departmental Clients":("130.85.94.1","255.255.254.0"),
  "CS Departmental Printers":("130.85.89.17","255.255.255.240"),
  "CS Departmental Classrooms":("130.85.91.1","255.255.255.128"),
  "CS Departmental Classrooms":("130.85.86.192","255.255.255.192"),
  "ECS Computer Room":("130.85.34.1","255.255.255.224"),
  "CS Departmental Servers":("130.85.172.1","255.255.255.240"),
  "Dynamic CS Departmental Clients":("130.85.172.129","255.255.255.192"),
  "Static CS Departmental Clients":("130.85.172.193","255.255.255.224"),
  "CS Department Printers":("130.85.172.33","255.255.255.240"),
  "ECS Computer Room":("130.85.36.65","255.255.255.192"),
  "ENG Computer Room - Researchers":("130.85.37.0","255.255.255.224"),
  "Loopback":("127.0.0.1","255.0.0.0"),}

interfaces = all_interfaces()
interfaces = [(x[0],
  x[1],
  getHwAddr(x[0]),
  getNetwork(x[1], networks),
  getHostname(x[1]),) for x in interfaces]

for i in interfaces:
  print i
