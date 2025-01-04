# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Try programiz.pro")
addr = """10.1.1.2
10.1.2.1
10.2.1.2
10.2.2.1

10.1.2.2
10.1.3.1
10.2.2.2
10.2.3.1

10.1.3.2
10.1.4.1
10.2.3.2
10.2.4.1

10.1.4.2
10.1.5.1
10.2.4.2
10.2.5.1

"""

cfg = """conf t
ip vrf vrf1
ip vrf vrf2

router ospf 10 vrf vrf1
router ospf 20 vrf vrf2

! IPs follow 10.vrf.network.location
int g1/0
 ip vrf forwarding vrf1
 ip ospf 10 a 0
 ip add {1} 255.255.255.0
 no shut
int g2/0
 ip vrf forwarding vrf1
 ip ospf 10 a 0
 ip add {0} 255.255.255.0
 no shut
int g3/0
 ip vrf forwarding vrf2
 ip ospf 20 a 0
 ip add {3} 255.255.255.0
 no shut
int g4/0
 ip vrf forwarding vrf2
 ip ospf 20 a 0
 ip add {2} 255.255.255.0
 no shut
"""
"""
ip route vrf vrf1 10.1.1.1 255.255.255.255 g1/0
ip route vrf vrf2 10.2.1.1 255.255.255.255 g3/0
ip route vrf vrf1 10.1.5.2 255.255.255.255 g2/0
ip route vrf vrf2 10.2.5.2 255.255.255.255 g4/0

"""

a = addr.splitlines()
print(a)
print(a[0:4])
print(a[5:9])
#x = int(input())*5
#print(cfg.format(*a[x:x+4]))

for i in range(4):
	with open(f"R{i+1}.txt", 'w') as f:
		f.write(cfg.format(*a[i*5:i*5+4]).replace('\n',"\r\n"))
