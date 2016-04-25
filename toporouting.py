#!/usr/bin/python


from subprocess import call
import requests
import json

############################# ROUTE 1 #########################################################################
## settin gateway ie default router for each router
## difference with routing3 is that statics will be set first
##  static s3->s4 destination:172.16.40.0/24, gateway:10.10.10.10
##  static s3->s1 destination:172.16.10.0/24, gateway:10.10.10.5
##
## curl -X POST -d '{"destination":"172.16.40.0/24", "gateway":"10.10.10.10"}' http://1.100.53.2:8080/router/0000000000000003
## curl -X POST -d '{"destination":"172.16.10.0/24", "gateway":"10.10.10.5"}' http://1.100.53.2:8080/router/0000000000000003


## default gateway of
##  s1  is s3 ,  gateway:10.10.10.6
##  s3  is s1 ,  gateway:10.10.10.5
##  s4  is s3 ,  gateway:10.10.10.9
## 
## curl -X POST -d '{"gateway":"10.10.10.6"}' http://1.100.53.2:8080/router/0000000000000001
## curl -X POST -d '{"gateway":"10.10.10.5"}' http://1.100.53.2:8080/router/0000000000000003
## curl -X POST -d '{"gateway":"10.10.10.9"}' http://1.100.53.2:8080/router/0000000000000004	

## curl -X DELETE -d '{"route_id":"all"}' http://1.100.53.2:8080/router/0000000000000001




##storing topology route 1 data
## curl -X POST -d '{"toporoute":"1", "sw":"0000000000000003", "destination":"172.16.40.0/24", "gateway":"10.10.10.10"}'  http://1.100.53.2:8080/toporoute/
## curl -X POST -d '{"toporoute":"1", "sw":"0000000000000003", "destination":"172.16.10.0/24", "gateway":"10.10.10.5"}'  http://1.100.53.2:8080/toporoute/
## curl -X POST -d '{"toporoute":"1", "sw":"0000000000000001", "gateway":"10.10.10.6"}'  http://1.100.53.2:8080/toporoute/
## curl -X POST -d '{"toporoute":"1", "sw":"0000000000000003", "gateway":"10.10.10.5"}'  http://1.100.53.2:8080/toporoute/
## curl -X POST -d '{"toporoute":"1", "sw":"0000000000000004", "gateway":"10.10.10.9"}'  http://1.100.53.2:8080/toporoute/

## view route
## curl -X GET -d '{}' http://1.100.53.2:8080/toporoute/1

## view all route
## curl -X GET -d '{}' http://1.100.53.2:8080/toporoute/all


## enable/disable topology route 1
## curl -X POST -d '{"enable":"true"}' http://1.100.53.2:8080/toporoute/1
## curl -X POST -d '{"enable":"false"}' http://1.100.53.2:8080/toporoute/1
## ryu controller url
serverUrl="http://1.100.53.2:8080/"

## postToRyu will genereate a json request to ryu server
## parameters
##    switchID : in string format
##    ruleData : in json string format
## the request result will be print out to console
## if an error happens an exception will be raised
def postToRyu(switchID,ruleData):    
    fullUrl=serverUrl + "toporoute/"
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

    
def myGatewayRouteset1():

    print "*** Routeset 1: Adding default static routes to switches with ryu app.rest.router controller "+serverUrl+"\n" 


    print "*** Routeset 1: Set static route between s3<->s4 \n" 
    rule4data={"toporoute":"1", "sw":"0000000000000003", "destination":"172.16.40.0/24", "gateway":"10.10.10.10"}    
    postToRyu("0000000000000003",rule4data)

    print "*** Routeset 1: Set static route between s3<->s1 \n"     
    rule5data={"toporoute":"1", "sw":"0000000000000003", "destination":"172.16.10.0/24", "gateway":"10.10.10.5"}    
    postToRyu("0000000000000003",rule5data)


    print "*** Routeset 1: Adding default routes to switches with ryu app.rest.router controller "+serverUrl+"\n" 

    ## setting the default gateways 
    print "*** Routeset 1: Set router s3 as the default route of router s1 \n"
    rule1data={"toporoute":"1", "sw":"0000000000000001", "gateway":"10.10.10.6"}    
    postToRyu("0000000000000001",rule1data)
	
    print "*** Routeset 1: Set router s1 as the default route of router s3 \n"    
    rule2data={"toporoute":"1", "sw":"0000000000000003", "gateway":"10.10.10.5"}    
    postToRyu("0000000000000003",rule2data)
   
    print "*** Routeset 1: Set router s3 as the default route of router s4 \n"    
    rule3data={"toporoute":"1", "sw":"0000000000000004", "gateway":"10.10.10.9"}
    postToRyu("0000000000000004",rule3data)
 


def myGatewayRouteset2():

    print "*** Routeset 2: Adding default static routes to switches with ryu app.rest.router controller "+serverUrl+"\n" 

    print "*** Routeset 2: Set static route between s2<->s4 \n" 
    rule4data={"toporoute":"2", "sw":"0000000000000002", "destination":"172.16.40.0/24", "gateway":"10.10.10.14"}    
    postToRyu("0000000000000003",rule4data)

    print "*** Routeset 2: Set static route between s2<->s1 \n"     
    rule5data={"toporoute":"2", "sw":"0000000000000002", "destination":"172.16.10.0/24", "gateway":"10.10.10.1"}    
    postToRyu("0000000000000003",rule5data)


    print "*** Routeset 2: Adding default routes to switches with ryu app.rest.router controller "+serverUrl+"\n" 

    ## setting the default gateways 
    print "*** Routeset 2: Set router s2 as the default route of router s1 \n"
    rule1data={"toporoute":"2", "sw":"0000000000000001", "gateway":"10.10.10.2"}    
    postToRyu("0000000000000001",rule1data)
	
    print "*** Routeset 2: Set router s1 as the default route of router s2 \n"    
    rule2data={"toporoute":"2", "sw":"0000000000000002", "gateway":"10.10.10.1"}    
    postToRyu("0000000000000003",rule2data)
   
    print "*** Routeset 2: Set router s2 as the default route of router s4 \n"    
    rule3data={"toporoute":"2", "sw":"0000000000000004", "gateway":"10.10.10.13"}
    postToRyu("0000000000000004",rule3data)

if __name__ == '__main__':    
    myGatewayRouteset1()
    myGatewayRouteset2()	
    getRyuData()
    
