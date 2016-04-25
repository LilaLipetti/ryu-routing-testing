
#!/usr/bin/python


from subprocess import call
import requests
import json

## Add addresses on switch interfaces. The syntax of the adding addresses with cURL:
## curl -X POST -d '{"address": "ip-address/mask"}' http://localhost:8080/router/switchID

## s1, h1
## h1 : 172.16.10.10/24
## 0000000000000001	172.16.10.1/24
## 0000000000000001	10.10.10.1/30
## 0000000000000001	10.10.10.5/30

## curl -X POST -d '{"address":"172.16.10.1/24"}'http://1.100.53.2:8080/router/0000000000000001
## curl -X POST -d '{"address":"10.10.10.1/30"}'http://1.100.53.2:8080/router/0000000000000001
## curl -X POST -d '{"address":"10.10.10.5/30"}'http://1.100.53.2:8080/router/0000000000000001
 
## s2
## 0000000000000002	10.10.10.2/30
## 0000000000000002	10.10.10.13/30	
## curl -X POST -d '{"address":"10.10.10.2/30"}'http://1.100.53.2:8080/router/0000000000000002
## curl -X POST -d '{"address":"10.10.10.13/30"}'http://1.100.53.2:8080/router/0000000000000002

## s3
## 0000000000000003	10.10.10.6/30
## 0000000000000003	10.10.10.9/30
## curl -X POST -d '{"address":"10.10.10.6/30"}'http://1.100.53.2:8080/router/0000000000000003
## curl -X POST -d '{"address":"10.10.10.9/30"}'http://1.100.53.2:8080/router/0000000000000003

## s4, h2
## h1 : 172.16.40.10/24
## 0000000000000004	172.16.40.1/24
## 0000000000000004	10.10.10.10/30
## 0000000000000004	10.10.10.14/30
## curl -X POST -d '{"address":"172.16.40.1/24"}'http://1.100.53.2:8080/router/0000000000000004
## curl -X POST -d '{"address":"10.10.10.10/30"}'http://1.100.53.2:8080/router/0000000000000004
## curl -X POST -d '{"address":"10.10.10.14/30"}'http://1.100.53.2:8080/router/0000000000000004

	
## ryu controller url 
serverUrl="http://1.100.53.3:8080/"


## postToRyu will genereate a json request to ryu server
## parameters
##    switchID : in string format
##    ruleData : in json string format
## the request result will be print out to console
## if an error happenes an exception will be raised
def postToRyu(switchID,ruleData):    
    fullUrl=serverUrl+"router/"+switchID	
    r = requests.post(fullUrl,data=json.dumps(ruleData))
    
    print r.text + "\n"
    
    if r.status_code != requests.codes.ok :
        r.raise_for_status()
		
## getRyuData: helper function to print out 
## current configuration from ryu
def getRyuData():
    fullUrl=serverUrl+"router/all/all"
    r=requests.get(fullUrl)
    print "\n current ryu configs are: \n"
    print r.text+"\n"

    
    
def myAddresses():

    print "*** Adding addresses to switch ports with ryu app.rest.router controller  ip=1.100.53.3 \n"

    print "*** to switch1 ports \n"
	
    rule1data={"address":"172.16.10.1/24"}
    postToRyu("0000000000000001",rule1data)	
	
    rule2data={"address":"10.10.10.1/30"}    
    postToRyu("0000000000000001",rule2data)
	
    rule3data={"address":"10.10.10.5/30"}    
    postToRyu("0000000000000001",rule3data)

    print "*** to switch2 ports \n "
    
    rule4data={"address":"10.10.10.2/30"}    
    postToRyu("0000000000000002",rule4data)
	
    rule5data={"address":"10.10.10.13/30"}    
    postToRyu("0000000000000002",rule5data)
   
    print "*** to switch3 ports \n"
    
    rule6data={"address":"10.10.10.6/30"}    
    postToRyu("0000000000000003",rule6data)
	
    rule7data={"address":"10.10.10.9/30"}    
    postToRyu("0000000000000003",rule7data)

    print "*** to switch4 ports \n"
    
    rule8data={"address":"172.16.40.1/24"}    
    postToRyu("0000000000000004",rule8data)
	
    rule9data={"address":"10.10.10.10/30"}    
    postToRyu("0000000000000004",rule9data)
	
    rule10data={"address":"10.10.10.14/30"}    
    postToRyu("0000000000000004",rule10data)

if __name__ == '__main__':   
    myAddresses()
    getRyuData()


