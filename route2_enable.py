
#!/usr/bin/python


from mininet.log import setLogLevel, info
from subprocess import call
import requests
import json



def enable2():

    info( '*** enable route 2' )


      
    ## first we need to clear out all route config
    ###curl -X DELETE -d '{"route_id":"all"}' http://1.100.53.2:8080/router/all    
    postTo="http://1.100.53.2:8080/router/all"        
    rule1data={"route_id":"all"}
    r = requests.delete(postTo,data=json.dumps(rule1data))
	
    
    ## then we enable routeset 2
    ##curl -X POST -d '{"enable":"true"}' http://1.100.53.2:8080/toporoute/2
    postTo="http://1.100.53.2:8080/toporoute/2"
    rule2data={"enable":"true"}
    r = requests.post(postTo,data=json.dumps(rule2data))
    
    
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    enable2()


