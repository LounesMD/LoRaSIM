from utils.WorldMap import WorldMap
import sys
import random
import string
from random import *
from threading import Thread
import time
from utils.ApplicationServer import generateApplicationServers
from utils.EndDevice import generateRandomEndDevice
from utils.Gateway import generateSmartGateway
from utils.WorldMap import WorldMap
from Simulator_WithoutBlockchain.utils.NetworkServer import generateNetworkServers
from utils.JoinServer import generateJoinServers
import matplotlib.pyplot as plt
SF = 'SF7_DR5'
AppKey = 'Sixteen byte key'
NwkKey = 'Sixteen byte key'



size,nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers,nbOfDownServer = 150,1000,10,10,1,10
WorldMap = WorldMap()

#Generation of join Servers
nbJoinServers = nbOfJoinServer
JoinServers = generateJoinServers(nbJoinServers)

JoinServersAvailable = list()
JoinServersAvailable = JoinServers.copy()


#We save the DevEUI in a random join server     
EndDevices,EndDevicesPos = generateRandomEndDevice(nbOfEndDevice, JoinServersAvailable, WorldMap , size*1000 , SF)

#Gateways,GatewaysPos = generateRandomGateway(500 , WorldMap)
capacity = 28
Gateways,GatewaysPos = generateSmartGateway(WorldMap,size*1000 , capacity)
nbGateways = len(Gateways)
#Generation of Network Servers
nbNetworkServers = nbOfNetworkServers
NetworkServers = generateNetworkServers(nbNetworkServers)


#We link the network servers between them
for ns1 in NetworkServers:
    for ns2 in NetworkServers:
        ns1.addnetworkServer(ns2)
#Generation of Application Servers
nbAppServers = nbOfAppServers
AppServers = generateApplicationServers(nbAppServers)

#We add the devices and the gateways to the WorldMap
for Device in EndDevices:
    WorldMap.addEndDevice(Device)
for gateway in Gateways:    
    WorldMap.addGateway(gateway)

#Plot the represnetaion of the devices and the gateways
f,s = list(),list()
for (x,y) in EndDevicesPos :
    f.append(x)
    s.append(y)
plt.scatter(f,s,c='g',marker='x',s=1/20,label='End-devices')
f,s,circles = list(),list(),list()
for (x,y) in GatewaysPos :
    f.append(x)
    s.append(y)
    circles.append(plt.Circle((x,y), 15000, color='b',alpha=0.05))
plt.scatter(f, s, color = 'b', marker = 'x' , s =3 , label ='Gateways')
    
#Plot the network servers
xns = list()
yns = list()    
for i in range(nbNetworkServers):
    xns.append(size*1100+5*1000+15000)
    yns.append((i*((size*1000)/nbNetworkServers))/2)
plt.scatter(xns,yns, color = 'r', marker = 's' , s =3, label = 'Network Servers')

#Plot the join servers
xjs = list()
yjs = list()
for i in range(nbJoinServers):
    xjs.append((i*((size*1000)/nbJoinServers))/2 + size*1100 +15000)
    yjs.append(((size + size/2)/2)*1000 )
plt.scatter(xjs,yjs, color = 'y', marker = 'd' , s =3 , label = 'Join Servers')
    
#Plot the application servers
xas = list()
yas = list()
for i in range(nbAppServers):
    xas.append(2*size*1000 + 15000)
    yas.append((i*((size*1000)/nbAppServers)))
plt.scatter(xas,yas, color = 'k', marker = 'p' , s =3 , label = 'Application Servers')

#Random link between gatways and network servers. And plot a line between link elements
for gateway in Gateways:
    j = 3 #randint(1,nbNetworkServers) #We take a random number of network server
    nserversPos =  sample([p for p in range(nbNetworkServers)], j)
    for val in nserversPos:
        NetworkServers[val].addGateway(gateway)
        gateway.addNetworkServers(NetworkServers[val])
        (x1,y1) = gateway.getPosition()
        (x2,y2) = xns[val],yns[val]
        plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='r')

#Random link between network servers and join servers. And plot a line between link elements
for i in range(nbNetworkServers):
    j = 3 #randint(1,nbJoinServers) #We take a random number of join server
    jServerPos =  sample([p for p in range(nbJoinServers)], j)
    for val in jServerPos:
        NetworkServers[i].addJoinServers(JoinServers[val])
        JoinServers[val].addNetworkServers(NetworkServers[i], NwkKey)
        (x2,y2) = xjs[val],yjs[val]
        (x1,y1) = xns[i],yns[i]
        plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='y')

#Teh following section links the devices with a reachable gateway and then with a reachable join server (and stores the device ID in the join server)
for ed in EndDevices:
    gtw = choice(ed.WorldMap.matriceAdjacenceVersGateway[ed.getDevEUI()])
    ns = choice([i for i in gtw.networkServers])
    js = choice([i for i in ns.joinServers.values()])
    ed.JoinEUI = js.getJoinEUI()
    js.addDevices(ed.getDevEUI() , ed.NwkKey , ed.AppKey)



#Random link between join servers and application servers.
for i in range(nbJoinServers):
    j = randint(nbAppServers//2,nbAppServers) #We take a random number of join server
    AServersPos =  sample([p for p in range(j)], j)
    for val in AServersPos:
        JoinServers[i].addapplicationServers(AppServers[val], AppKey)        
        (x2,y2) = xas[val],yas[val]
        (x1,y1) = xjs[i],yjs[i]
        plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='k')


#Random link between network servers and application servers.
for i in range(nbNetworkServers):
    j = randint(nbAppServers//2,nbAppServers) #We take a random number of join server
    AServersPos =  sample([p for p in range(j)], j)
    for val in AServersPos:
        (x2,y2) = xas[val],yas[val]
        (x1,y1) = xns[i],yns[i]
        plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='k')


    

plt.legend(title='Legend',title_fontsize=30,loc='center left',bbox_to_anchor=(1, 0.5))
plt.title("LoRaWAN Simulator")
#plt.axis('off')

for circle in circles: #Thos circles represent the range of the gateways
    plt.gca().add_patch(circle)
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)

#    plt.savefig('Img.svg',bbox_inches='tight')
plt.show()
