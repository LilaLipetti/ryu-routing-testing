
#!/usr/bin/python


from mininet.log import setLogLevel, info
from subprocess import call
import requests
import json



def delete():

    info( '*** delete all active routes' )


      
    ## first we need to clear out all route config
    ###curl -X DELETE -d '{"route_id":"all"}' http://1.100.53.2:8080/router/all    
    postTo="http://1.100.53.2:8080/router/all"        
    rule1data={"route_id":"all"}
    r = requests.delete(postTo,data=json.dumps(rule1data))
	
    
     
    
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    delete()


