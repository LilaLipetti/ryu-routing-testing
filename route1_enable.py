
#!/usr/bin/python


from mininet.log import setLogLevel, info
from subprocess import call
import requests
import json



def enable1():

    info( '*** enable route 1' )


      
    ## first we need to clear out all route config
    ###curl -X DELETE -d '{"route_id":"all"}' http://1.100.53.2:8080/router/all    
    postTo="http://1.100.53.2:8080/router/all"        
    rule1data={"route_id":"all"}
    r = requests.delete(postTo,data=json.dumps(rule1data))
	
    
    ## then we enable routeset 1
    ##curl -X POST -d '{"enable":"true"}' http://1.100.53.2:8080/toporoute/1
    postTo="http://1.100.53.2:8080/toporoute/1"
    rule2data={"enable":"true"}
    r = requests.post(postTo,data=json.dumps(rule2data))
    
    
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    enable1()


