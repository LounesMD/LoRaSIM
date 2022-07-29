# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 13:47:49 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""
import sys
from EndDevice import *
from WorldMap import *
from JoinServer import *
from NetworkServer import *
from Gateway import *
from ApplicationServer import *
import random
import string
from random import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

EU_Frequencies = []
#WorldMap = WorldMap()
JoinEUI = '8JoinEUI'
DevEUI =  '8 DevEUI'
AppKey = 'Sixteen byte key'
NwkKey = 'Sixteen byte key'
GatewayId = 'GatewayId'
capacity = 10
GatewayPos = (0,0)
EndDevicePos = (200,1000)
SF = 'SF7_DR5'

SpreedingFactor = {'SF7_DR6' : 0.1844, 'SF7_DR5' : 0.3689, 'SF8_DR4':0.6559, 'SF9_DR3':1.1684, 'SF10_DR2':2.132,'SF11_DR1':4.6735,'SF12_DR0':8.364} #airtime associed to every spread factor https://www.thethingsnetwork.org/docs/lorawan/spreading-factors/
def get_random_string(length):
    #https://pynative.com/python-generate-random-string/
    # choose from all lowercase letter
    letters = string.printable 
    result_str = ''.join(choice(letters) for i in range(length))
    return result_str
    

def generateRandomEndDeviceBIS(nb , JoinEUI , WorldMap,size , SF):
    #AppKeys,NwkKeys
    """
    -> They connect them to a random join server
    /!\ Pls manage smartly your AppKey NwkKey. With this function you cannot get those keys. So yes, my example below doesn't work if you want to get the session keys
    """
    AllDevEUI = list()
    EndDevices = list()
    EndDevicesPos = list()
    for i in range(nb):
        DevEUI = get_random_string(8)        
        while DevEUI in AllDevEUI:
            DevEUI = get_random_string(8)        
        JoinEUI = choice(JoinEUI)
        AppKey =  get_random_string(16) #AppKeys[i]
        NwkKey = get_random_string(16) #NwkKeys[i]
        (x,y) = (randint(0,size) , randint(0,size)) #1000km x 1000km
        EndDevicePos = (x,y)
        SpF = SF #choice(list(SpreedingFactor.keys()))
        endDevice = EndDevice(DevEUI, JoinEUI, AppKey, NwkKey, EndDevicePos, WorldMap,SpF)
        EndDevices.append(endDevice)
        EndDevicesPos.append((x,y))
        AllDevEUI.append(DevEUI)
    return EndDevices,EndDevicesPos
AppKey = 'Sixteen byte key'
NwkKey = 'Sixteen byte key'

def generateRandomEndDevice(nb , JoinEUIAvailable , WorldMap,size , SF):
    #AppKeys,NwkKeys
    """
    -> They connect them to a random join server
    /!\ Pls manage smartly your AppKey NwkKey. With this function you cannot get those keys. So yes, my example below doesn't work if you want to get the session keys
    """
    AllDevEUI = list()
    EndDevices = list()
    EndDevicesPos = list()
    for i in range(nb):
        DevEUI = get_random_string(8)        
        while DevEUI in AllDevEUI:
            DevEUI = get_random_string(8)        
        JoinEUI = choice(JoinEUIAvailable)
        (x,y) = (randint(0,size) , randint(0,size)) #1000km x 1000km
        EndDevicePos = (x,y)
        SpF = SF #choice(list(SpreedingFactor.keys()))
        endDevice = EndDevice(DevEUI, JoinEUI, AppKey, NwkKey, EndDevicePos, WorldMap,SpF)
        EndDevices.append(endDevice)
        EndDevicesPos.append((x,y))
        AllDevEUI.append(DevEUI)
    return EndDevices,EndDevicesPos

def generateRandomGateway(nb, WorldMap,size):
    frequence = 'EU433'
    #We suppose that they all use EU433 
    Gateways = list()
    GatewaysPos = list()
    for i in range(nb):
        (x,y) = (randint(0,size) , randint(0,size))
        GatewayId = get_random_string(8)+str(i)
        gateway = Gateway((x,y),GatewayId,WorldMap,frequence)
        Gateways.append(gateway)
        GatewaysPos.append((x,y))
    return Gateways,GatewaysPos

def generateSmartGateway(WorldMap,size,capacity):
    """
    With this function you have one gateway every 15km
    """
    frequence = 'EU433'
    Gateways = list()
    GatewaysPos = list()
    for i in range(size//15000 ):
        for j in range(size//15000 ):
            (x,y) = ( i*15000+15000/2 , j*15000+15000/2)
            GatewayId = get_random_string(8)+str(i)
            gateway = Gateway((x,y),GatewayId,WorldMap,frequence,capacity)
            Gateways.append(gateway)
            GatewaysPos.append((x,y))
    return Gateways,GatewaysPos

def generateNetworkServers(nb):
    networkServers = list()
    for i in range(nb):
        networkServers.append(NetworkServer())
    return networkServers

def generateNetworkServers(nb):
    networkServers = list()
    for i in range(nb):
        networkServers.append(NetworkServer())
    return networkServers

def generateApplicationServers(nb):
    ApplicationServers = list()
    nb = nb
    for i in range(nb):
        ApplicationServers.append(ApplicationServer(AppKey))
    return ApplicationServers

def generateJoinServers(nb):
    AllJoinEUI = list()
    joinServers = list()
    for i in range(nb):
        JoinEUI = get_random_string(8)        
        while JoinEUI in AllJoinEUI:
            JoinEUI = get_random_string(8)        
        AllJoinEUI.append(JoinEUI)
        joinServers.append(JoinServer(JoinEUI , 0))
    return joinServers

"""
#####################################################
frequence = 'EU433'
Device = EndDevice(DevEUI, JoinEUI, AppKey, NwkKey, EndDevicePos, WorldMap,SF)
Gateway1 = Gateway(GatewayPos,GatewayId,WorldMap,frequence)
Gateway2 = Gateway((1,1),GatewayId+'2',WorldMap,frequence)

NetworkServer1 = NetworkServer()
NetworkServer2 = NetworkServer()
JoinServer = JoinServer(JoinEUI , capacity)
ApplicationServer = ApplicationServer(AppKey)
#Ajout du device et du Gateway a une distance de moins de 15km
WorldMap.addEndDevice(Device)
WorldMap.addGateway(Gateway1)
WorldMap.addGateway(Gateway2)

#Connection entre le Gateway et les network servers
NetworkServer1.addGateway(Gateway1)
NetworkServer2.addGateway(Gateway1)
Gateway1.addNetworkServers(NetworkServer1)
Gateway1.addNetworkServers(NetworkServer2)
#Ajout d'une frequence
#Gateway1.addFrequency(876)
#Gateway2.addFrequency(876)

#Connection Network Server 1 et JoinServer
NetworkServer1.addJoinServers(JoinServer)
JoinServer.addNetworkServers(NetworkServer1, NwkKey)


NetworkServer2.addJoinServers(JoinServer)
JoinServer.addNetworkServers(NetworkServer2, NwkKey)
#Connection JoinServer ApplicationServer
JoinServer.addapplicationServers(ApplicationServer, AppKey)
#Ajout du EndDevice dans le joinServer
JoinServer.addDevices(DevEUI, NwkKey, AppKey)
cpt = 0
t = Device.joinRequestMessage(434)
"""
#print(Device.joinRequestMessage(876)) #Normalement on utilise une fréquence aléatoire #https://lora-developers.semtech.com/documentation/tech-papers-and-guides/the-book/joining-and-rejoining

#AppKeys = [get_random_string(16) for i in range]
#from numba import jit

#@jit
#Main For Time Connection and Connection Rate
def main(Mapsize ,  nbOfEndDevice, nbOfJoinServer,nbOfNetworkServers,nbOfAppServers,WorldMap,nbOfConnectionIteration):
    """
    

    Parameters
    ----------
    Mapsize : TYPE
        DESCRIPTION.
    nbOfEndDevice : TYPE
        DESCRIPTION.
    nbOfJoinServer : TYPE
        DESCRIPTION.
    nbOfNetworkServers : TYPE
        DESCRIPTION.
    nbOfAppServers : TYPE
        DESCRIPTION.
    WorldMap : TYPE
        DESCRIPTION.
    nbOfConnectionIteration : int
         .

    Returns
    -------
    None.

    """
    WorldMap = WorldMap
    size = Mapsize
    #Generation of join Servers
    nbJoinServers = nbOfJoinServer
    JoinServers = generateJoinServers(nbJoinServers)
    
    JoinEUIAvailable = list()
    for joinServer in JoinServers :
        #print(joinServer.getJoinEUI())
        JoinEUIAvailable.append(joinServer.getJoinEUI())
    
    #We save the DevEUI in a random join server     
    EndDevices,EndDevicesPos = generateRandomEndDevice(nbOfEndDevice, JoinEUIAvailable, WorldMap , size*1000 , SF)
    d = dict() #dictionnary  EndDevice : JoinServer
    for endDevice in EndDevices:
        d[endDevice] = endDevice.getJoinEUI()
    
    #Gateways,GatewaysPos = generateRandomGateway(500 , WorldMap)
    capacity = 28
    Gateways,GatewaysPos = generateSmartGateway(WorldMap,size*1000 , capacity)
    nbGateways = len(Gateways)
    #Generation of Network Servers
    nbNetworkServers = nbOfNetworkServers
    NetworkServers = generateNetworkServers(nbNetworkServers)
    for ns1 in NetworkServers:
        for ns2 in NetworkServers:
            ns1.addnetworkServer(ns2)
    #Generation of Application Servers
    nbAppServers = nbOfAppServers
    AppServers = generateApplicationServers(nbAppServers)
    
    #Ajout du device et du Gateway a une distance de moins de 15km
    for Device in EndDevices:
        WorldMap.addEndDevice(Device)
    for gateway in Gateways:    
        WorldMap.addGateway(gateway)
    
#    f,s = list(),list()
#    for (x,y) in EndDevicesPos :
#        f.append(x)
#        s.append(y)
#    plt.scatter(f,s,c='g',marker='x',s=1/20,label='End-devices')
#    f,s,circles = list(),list(),list()
#    for (x,y) in GatewaysPos :
#        f.append(x)
#        s.append(y)
#        circles.append(plt.Circle((x,y), 15000, color='b',alpha=0.05))
#    plt.scatter(f, s, color = 'b', marker = 'x' , s =3 , label ='Gateways')
     
#    xns = list()
#    yns = list()    
#    for i in range(nbNetworkServers):
#        xns.append(size*1100+5*1000+15000)
#        yns.append((i*((size*1000)/nbNetworkServers))/2)
#    plt.scatter(xns,yns, color = 'r', marker = 's' , s =3, label = 'Network Servers')
    
#    xjs = list()
#    yjs = list()
#    for i in range(nbJoinServers):
#        xjs.append((i*((size*1000)/nbJoinServers))/2 + size*1100 +15000)
#        yjs.append(((size + size/2)/2)*1000 )
#    plt.scatter(xjs,yjs, color = 'y', marker = 'd' , s =3 , label = 'Join Servers')
        
#    xas = list()
#    yas = list()
#    for i in range(nbAppServers):
#        xas.append(2*size*1000 + 15000)
#        yas.append((i*((size*1000)/nbAppServers)))
#    plt.scatter(xas,yas, color = 'k', marker = 'p' , s =3 , label = 'Application Servers')
    
    #On fait un lien aléatoire entre les gateways et les network servers.
    for gateway in Gateways:
        j = randint(1,nbNetworkServers) #We take a random number of network server
        nserversPos =  sample([p for p in range(j)], j)
        for val in nserversPos:
            NetworkServers[val].addGateway(gateway)
            gateway.addNetworkServers(NetworkServers[val])
#            (x1,y1) = gateway.getPosition()
#            (x2,y2) = xns[val],yns[val]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='r')
    
    #On fait un lien aléatoire entre les network servers et les join servers.
    for i in range(nbNetworkServers):
        j = randint(1,nbJoinServers) #We take a random number of join server
        jServerPos =  sample([p for p in range(j)], j)
        for val in jServerPos:
            NetworkServers[i].addJoinServers(JoinServers[val])
            JoinServers[val].addNetworkServers(NetworkServers[i], NwkKey)
#            (x2,y2) = xjs[val],yjs[val]
#            (x1,y1) = xns[i],yns[i]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='y')
    
    #On fait un lien aléatoire entre les join servers et les application servers.
    for i in range(nbJoinServers):
        j = randint(nbAppServers//2,nbAppServers) #We take a random number of join server
        AServersPos =  sample([p for p in range(j)], j)
        for val in AServersPos:
            JoinServers[i].addapplicationServers(AppServers[val], AppKey)        
#            (x2,y2) = xas[val],yas[val]
#            (x1,y1) = xjs[i],yjs[i]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='k')
    
    
    
    #Cette partie du code n'a aucune utilité d'un point de vue code parceque le lien entre les nServers et les AppServers n'est pas implémenté.
#    for i in range(nbNetworkServers):
#        j = randint(nbAppServers//2,nbAppServers) #We take a random number of join server
#        AServersPos =  sample([p for p in range(j)], j)
#        for val in AServersPos:
#            (x2,y2) = xas[val],yas[val]
#            (x1,y1) = xns[i],yns[i]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='k')
    
    
    
    #Ajout du EndDevice dans le joinServer
    for jserver in JoinServers:
        for endDevice in EndDevices:
            jserver.addDevices(endDevice.getDevEUI(), AppKey, AppKey)
    
    
#    plt.legend(title='Legend',title_fontsize=30,loc='center left',bbox_to_anchor=(1, 0.5))
#    plt.title("LoRaWAN Simulator")
    #plt.axis('off')
    
#    for circle in circles:
#        plt.gca().add_patch(circle)
#        plt.gca().get_xaxis().set_visible(False)
#        plt.gca().get_yaxis().set_visible(False)
#    
#    plt.savefig('Img.svg',bbox_inches='tight')
    pres = 0
    connectionTime = dict()
    start = time.time()
    end = dict()
    connectionRate = list()
    nbOfConnectedObjects = list()
    for i in range(nbOfConnectionIteration):
        #NetworkServers[i].deactivation()
        threads = [] 
        for endDevice in EndDevices:
            if(endDevice.isConnected==False):
            #print(endDevice.getDevEUI(),"envoie son message")                
                threads.append(Thread(target = endDevice.joinRequestMessage, args=(434,)))
                #debut = time.time()
                #endDevice.joinRequestMessage(434)
                #fin = time.time()
                #connectionTime.append(fin-debut)

        for x in threads:
            x.start()
    
        for x in threads: #We wait untill all end device has send one join request message
            x.join()
            
        end[i] = time.time()

        cpt = 0
        
        for endDevice in EndDevices:
            if(endDevice.isConnected==True):
                cpt+=1
#            else :
                #endDevice.joinRequestMessage(434)
#                (x,y) = endDevice.getPosition()
#                plt.scatter(x,y,c='r',marker='x',s=1)
        nbOfConnectedObjects.append(cpt)
        #print("Number of connected end-Device : "+ str((cpt/nbOfEndDevice)*100)+"%")
        connectionRate.append((cpt/nbOfEndDevice)*100)
        if(cpt == pres):
            end[i] = end[i-1] #Just to prefent from devices that can't connect them to the network
        pres = cpt
        
    total = list()
    for i in range(nbOfConnectionIteration):
        total.append(end[i] - start)
        connectionTime[i] = 0
    plt.show()        

    d = dict()
    for endDevice in EndDevices:
        if(endDevice.isConnected):
            connectionTime[int(endDevice.DevNonce,2)-1] += endDevice.getConnectionTime()
            if( (int(endDevice.DevNonce,2)-1) in d):
                d[int(endDevice.DevNonce,2)-1] += 1
            else : 
                d[int(endDevice.DevNonce,2)-1] = 1

    for val in d:
        connectionTime[val] = connectionTime[val]/d[val]
        
    return [(cpt/nbOfEndDevice)*100,connectionTime ,total,connectionRate,nbOfConnectedObjects] #ConnectionTime en 2
"""

for SF in ['SF7_DR6' , 'SF7_DR5' ,'SF8_DR4']: # SpreedingFactor:
    liste = list()
    for j in [1000 , 10000 , 100000,1000000]: #, 100000 ]: #, 10000 ]:#, 50000]: # , 1000 , 5000, 10000]:
        nbOfConnectionIteration = 100
        l = list()
        for i in range(10):
            WorldMp = WorldMap()
            #Mapsize,nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers = 150,j,1,1,1
            Mapsize,nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers = 150,j,10,10,1
            val = main(Mapsize , nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers,WorldMp ,nbOfConnectionIteration)
            val.append(j)
            l.append(val)
        

        #Average of the connection rate
        averageTotalConnectionRate = sum([val[0] for val in l])/(len(l))
        
        #Average connection time
        AverageConnectionTime = list()
        for i in range(nbOfConnectionIteration):
            AverageConnectionTime.append((sum([val[1][i] for val in l])/len(l)))
            
        #TotalPerIteration
        p = list()
        for val in l:
            p.append(val[2])
        taille = len(p)
        totalParIteration = list()
        for i in range(nbOfConnectionIteration):
            totalParIteration.append(sum([k[i] for k in p])/len(p))
        #Average number of connected end device
        averageConnectionRate = list()
        for i in range(nbOfConnectionIteration):
            averageConnectionRate.append(sum([val[3][i] for val in l])/len(l))

        #Average number of connected end device
        averagenbOfConnectedObjects = list()
        for i in range(nbOfConnectionIteration):
            averagenbOfConnectedObjects = sum([val[4][i] for val in l])/(len(l))
        liste.append([averageTotalConnectionRate,AverageConnectionTime ,totalParIteration,averageConnectionRate,averagenbOfConnectedObjects,j])    
        
    color = ['r','g','b','c','m','y']
    char = ['-' , '--' , '-.',':']
    #Statistique
    cpt=0
    for val in liste:
        plt.plot([(i+1) for i in range(len(val[3]))] ,[v for v in val[3]],linestyle =char[cpt] ,color=color[cpt],label=str(val[-1])+' devices')
        cpt += 1
    plt.grid()
    plt.title("Connection rate for the Spreading Factor:"+SF)
    plt.legend(loc='lower right')
    plt.show()
    cpt = 0
    for val in liste:
        plt.plot([(i+1) for i in range(len(val[2]))] ,[v for v in val[2]],linestyle =char[cpt] ,color=color[cpt],label=str(val[-1])+' devices')
        cpt += 1
    plt.grid()
    plt.title("Connection time for the Spreading Factor:"+SF)
    plt.legend(loc='upper right')
    plt.show()

"""
#######################################################################
#To measure the resilience of the network, just redone the same main but with different number of network server (from 0 to n)

#######################################################################
#Time detect a fake request. For this one, we are going to generate end device which want to send a request to a join server without being registered before. It's like a DoS Attack to specific join servers
def generateRandomEndDeviceForFakeRequest(nb  , JoinEUIAvailable,WorldMap,size , SF):
    #AppKeys,NwkKeys
    """
    -> They connect them to a random join server
    /!\ Pls manage smartly your AppKey NwkKey. With this function you cannot get those keys. So yes, my example below doesn't work if you want to get the session keys
    """
    AllDevEUI = list()
    EndDevices = list()
    EndDevicesPos = list()
    for i in range(nb):
        DevEUI = get_random_string(8)        
        while DevEUI in AllDevEUI:
            DevEUI = get_random_string(8)        
        JoinEUI = choice(JoinEUIAvailable)
        (x,y) = (randint(0,size) , randint(0,size)) #1000km x 1000km
        EndDevicePos = (x,y)
        SpF = SF #choice(list(SpreedingFactor.keys()))
        endDevice = EndDevice(DevEUI, JoinEUI, AppKey, NwkKey, EndDevicePos, WorldMap,SpF)
        EndDevices.append(endDevice)
        EndDevicesPos.append((x,y))
        AllDevEUI.append(DevEUI)
    return EndDevices,EndDevicesPos

def main(Mapsize ,  nbOfEndDevice, nbOfJoinServer,nbOfNetworkServers,nbOfAppServers,WorldMap,nbOfConnectionIteration):
    """
    

    Parameters
    ----------
    Mapsize : TYPE
        DESCRIPTION.
    nbOfEndDevice : TYPE
        DESCRIPTION.
    nbOfJoinServer : TYPE
        DESCRIPTION.
    nbOfNetworkServers : TYPE
        DESCRIPTION.
    nbOfAppServers : TYPE
        DESCRIPTION.
    WorldMap : TYPE
        DESCRIPTION.
    nbOfConnectionIteration : int
         .

    Returns
    -------
    None.

    """
    WorldMap = WorldMap
    size = Mapsize
    #Generation of join Servers
    nbJoinServers = nbOfJoinServer
    JoinServers = generateJoinServers(nbJoinServers)
    
    JoinEUIAvailable = list()
    for joinServer in JoinServers :
        #print(joinServer.getJoinEUI())
        JoinEUIAvailable.append(joinServer.getJoinEUI())
    
    #We save the DevEUI in a random join server     
    EndDevices,EndDevicesPos = generateRandomEndDeviceForFakeRequest(nbOfEndDevice,JoinEUIAvailable, WorldMap , size*1000 , SF)
    d = dict() #dictionnary  EndDevice : JoinServer
    for endDevice in EndDevices:
        d[endDevice] = endDevice.getJoinEUI()
    
    #Gateways,GatewaysPos = generateRandomGateway(500 , WorldMap)
    capacity = 28
    Gateways,GatewaysPos = generateSmartGateway(WorldMap,size*1000 , capacity)
    nbGateways = len(Gateways)
    #Generation of Network Servers
    nbNetworkServers = nbOfNetworkServers
    NetworkServers = generateNetworkServers(nbNetworkServers)
    for ns1 in NetworkServers:
        for ns2 in NetworkServers:
            ns1.addnetworkServer(ns2)
    #Generation of Application Servers
    nbAppServers = nbOfAppServers
    AppServers = generateApplicationServers(nbAppServers)
    
    #Ajout du device et du Gateway a une distance de moins de 15km
    for Device in EndDevices:
        WorldMap.addEndDevice(Device)
    for gateway in Gateways:    
        WorldMap.addGateway(gateway)
    
#    f,s = list(),list()
#    for (x,y) in EndDevicesPos :
#        f.append(x)
#        s.append(y)
#    plt.scatter(f,s,c='g',marker='x',s=1/20,label='End-devices')
#    f,s,circles = list(),list(),list()
#    for (x,y) in GatewaysPos :
#        f.append(x)
#        s.append(y)
#        circles.append(plt.Circle((x,y), 15000, color='b',alpha=0.05))
#    plt.scatter(f, s, color = 'b', marker = 'x' , s =3 , label ='Gateways')
     
#    xns = list()
#    yns = list()    
#    for i in range(nbNetworkServers):
#        xns.append(size*1100+5*1000+15000)
#        yns.append((i*((size*1000)/nbNetworkServers))/2)
#    plt.scatter(xns,yns, color = 'r', marker = 's' , s =3, label = 'Network Servers')
    
#    xjs = list()
#    yjs = list()
#    for i in range(nbJoinServers):
#        xjs.append((i*((size*1000)/nbJoinServers))/2 + size*1100 +15000)
#        yjs.append(((size + size/2)/2)*1000 )
#    plt.scatter(xjs,yjs, color = 'y', marker = 'd' , s =3 , label = 'Join Servers')
        
#    xas = list()
#    yas = list()
#    for i in range(nbAppServers):
#        xas.append(2*size*1000 + 15000)
#        yas.append((i*((size*1000)/nbAppServers)))
#    plt.scatter(xas,yas, color = 'k', marker = 'p' , s =3 , label = 'Application Servers')
    
    #On fait un lien aléatoire entre les gateways et les network servers.
    for gateway in Gateways:
        j = randint(1,nbNetworkServers) #We take a random number of network server
        nserversPos =  sample([p for p in range(j)], j)
        for val in nserversPos:
            NetworkServers[val].addGateway(gateway)
            gateway.addNetworkServers(NetworkServers[val])
#            (x1,y1) = gateway.getPosition()
#            (x2,y2) = xns[val],yns[val]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='r')
    
    #On fait un lien aléatoire entre les network servers et les join servers.
    for i in range(nbNetworkServers):
        j = randint(1,nbJoinServers) #We take a random number of join server
        jServerPos =  sample([p for p in range(j)], j)
        for val in jServerPos:
            NetworkServers[i].addJoinServers(JoinServers[val])
            JoinServers[val].addNetworkServers(NetworkServers[i], NwkKey)
#            (x2,y2) = xjs[val],yjs[val]
#            (x1,y1) = xns[i],yns[i]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='y')
    
    #On fait un lien aléatoire entre les join servers et les application servers.
    for i in range(nbJoinServers):
        j = randint(nbAppServers//2,nbAppServers) #We take a random number of join server
        AServersPos =  sample([p for p in range(j)], j)
        for val in AServersPos:
            JoinServers[i].addapplicationServers(AppServers[val], AppKey)        
#            (x2,y2) = xas[val],yas[val]
#            (x1,y1) = xjs[i],yjs[i]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='k')
    
    
    
    #Cette partie du code n'a aucune utilité d'un point de vue code parceque le lien entre les nServers et les AppServers n'est pas implémenté.
#    for i in range(nbNetworkServers):
#        j = randint(nbAppServers//2,nbAppServers) #We take a random number of join server
#        AServersPos =  sample([p for p in range(j)], j)
#        for val in AServersPos:
#            (x2,y2) = xas[val],yas[val]
#            (x1,y1) = xns[i],yns[i]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='k')
    
    
    
    #Ajout du EndDevice dans le joinServer
    #for jserver in JoinServers:
        #for endDevice in EndDevices:
            #jserver.addDevices(endDevice.getDevEUI(), AppKey, AppKey)
    
    
#    plt.legend(title='Legend',title_fontsize=30,loc='center left',bbox_to_anchor=(1, 0.5))
#    plt.title("LoRaWAN Simulator")
    #plt.axis('off')
    
#    for circle in circles:
#        plt.gca().add_patch(circle)
#        plt.gca().get_xaxis().set_visible(False)
#        plt.gca().get_yaxis().set_visible(False)
#    
#    plt.savefig('Img.svg',bbox_inches='tight')
    pres = 0
    connectionTime = dict()
    start = time.time()
    end = dict()
    connectionRate = list()
    nbOfConnectedObjects = list()
    tempsParIteration = list()
    nbConnecteParIteration = list()
    for i in range(nbOfConnectionIteration):
        #NetworkServers[i].deactivation()
        threads = [] 
        for endDevice in EndDevices:
            if(endDevice.isConnected==False):
            #print(endDevice.getDevEUI(),"envoie son message")                
                threads.append(Thread(target = endDevice.fakeJoinRequestMessage, args=(434,)))
                #debut = time.time()
                #endDevice.joinRequestMessage(434)
                #fin = time.time()
                #connectionTime.append(fin-debut)

        for x in threads:
            x.start()
    
        for x in threads: #We wait untill all end device has send one join request message
            x.join()
            
        
        tempsParIteration.append(0)
        
        cpt = 0
        for endDevice in EndDevices:
            if(endDevice.fakeRequestTimeDetection != None):
                cpt += 1
                tempsParIteration[i]+= (endDevice.fakeRequestTimeDetection)
                
        nbConnecteParIteration.append(cpt)        
        if(cpt != pres):
            tempsParIteration[i] = tempsParIteration[i]/cpt + tempsParIteration[i-1]
            pres = cpt
        else:
            tempsParIteration[i] = tempsParIteration[i]/cpt + tempsParIteration[i-1]
    return [tempsParIteration , nbConnecteParIteration] #ConnectionTime en 2


for SF in ['SF7_DR6' , 'SF7_DR5' ,'SF8_DR4']: # SpreedingFactor:
    print(SF)
    liste = list()
    for j in [ 50 , 100 , 500 ,1000]: # , 10000 , 100000,1000000]: #, 100000 ]: #, 10000 ]:#, 50000]: # , 1000 , 5000, 10000]:
        nbOfConnectionIteration = 35
        l = list()
        
        for i in range(10):
            WorldMp = WorldMap()
            #Mapsize,nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers = 150,j,1,1,1
            Mapsize,nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers = 15,j,10,10,1
            val = main(Mapsize , nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers,WorldMp ,nbOfConnectionIteration)
            l.append(val)
        
        li = list()    
        for i in range(nbOfConnectionIteration):
            v = 0
            z = 0
            for k in range(4):
                v+= l[k][0][i]
                z+= l[k][1][i] 
            
            v = v/4
            z = z/4
            li.append([v ,(z/j)*100])
        liste.append([li , j])
    color = ['r','g','b','c','m','y']
    char = ['-' , '--' , '-.',':']
    #Statistique
    cpt=0
    for val in liste:
        print(val[-1])
        nb = val[-1]
        val = val[0]
        plt.plot([i[0] for i in val] ,[v[1] for v in val],linestyle =char[cpt] ,color=color[cpt],label=str(nb)+' devices')
        cpt += 1
    plt.grid()
    plt.title("time to detect an unauthorized object SF: "+SF)
    plt.legend(loc='lower right')
    plt.show()


"""

def main(Mapsize ,  nbOfEndDevice, nbOfJoinServer,nbOfNetworkServers,nbOfAppServers,WorldMap,nbOfConnectionIteration):
    
    WorldMap = WorldMap
    size = Mapsize
    #Generation of join Servers
    nbJoinServers = nbOfJoinServer
    JoinServers = generateJoinServers(nbJoinServers)
    
    JoinEUIAvailable = list()
    for joinServer in JoinServers :
        #print(joinServer.getJoinEUI())
        JoinEUIAvailable.append(joinServer.getJoinEUI())
    
    #We save the DevEUI in a random join server     
    EndDevices,EndDevicesPos = generateRandomEndDevice(nbOfEndDevice, JoinEUIAvailable, WorldMap , size*1000 , SF)
    d = dict() #dictionnary  EndDevice : JoinServer
    for endDevice in EndDevices:
        d[endDevice] = endDevice.getJoinEUI()
    
    #Gateways,GatewaysPos = generateRandomGateway(500 , WorldMap)
    capacity = 28
    Gateways,GatewaysPos = generateSmartGateway(WorldMap,size*1000 , capacity)
    nbGateways = len(Gateways)
    #Generation of Network Servers
    nbNetworkServers = nbOfNetworkServers
    NetworkServers = generateNetworkServers(nbNetworkServers)
    #Generation of Application Servers
    nbAppServers = nbOfAppServers
    AppServers = generateApplicationServers(nbAppServers)
    
    #Ajout du device et du Gateway a une distance de moins de 15km
    for Device in EndDevices:
        WorldMap.addEndDevice(Device)
    for gateway in Gateways:    
        WorldMap.addGateway(gateway)
    
#    f,s = list(),list()
#    for (x,y) in EndDevicesPos :
#        f.append(x)
#        s.append(y)
#    plt.scatter(f,s,c='g',marker='x',s=1/20,label='End-devices')
#    f,s,circles = list(),list(),list()
#    for (x,y) in GatewaysPos :
#        f.append(x)
#        s.append(y)
#        circles.append(plt.Circle((x,y), 15000, color='b',alpha=0.05))
#    plt.scatter(f, s, color = 'b', marker = 'x' , s =3 , label ='Gateways')
     
#    xns = list()
#    yns = list()    
#    for i in range(nbNetworkServers):
#        xns.append(size*1100+5*1000+15000)
#        yns.append((i*((size*1000)/nbNetworkServers))/2)
#    plt.scatter(xns,yns, color = 'r', marker = 's' , s =3, label = 'Network Servers')
    
#    xjs = list()
#    yjs = list()
#    for i in range(nbJoinServers):
#        xjs.append((i*((size*1000)/nbJoinServers))/2 + size*1100 +15000)
#        yjs.append(((size + size/2)/2)*1000 )
#    plt.scatter(xjs,yjs, color = 'y', marker = 'd' , s =3 , label = 'Join Servers')
        
#    xas = list()
#    yas = list()
#    for i in range(nbAppServers):
#        xas.append(2*size*1000 + 15000)
#        yas.append((i*((size*1000)/nbAppServers)))
#    plt.scatter(xas,yas, color = 'k', marker = 'p' , s =3 , label = 'Application Servers')
    
    #On fait un lien aléatoire entre les gateways et les network servers.
    for gateway in Gateways:
        j = randint(1,nbNetworkServers) #We take a random number of network server
        nserversPos =  sample([p for p in range(j)], j)
        for val in nserversPos:
            NetworkServers[val].addGateway(gateway)
            gateway.addNetworkServers(NetworkServers[val])
#            (x1,y1) = gateway.getPosition()
#            (x2,y2) = xns[val],yns[val]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='r')
    
    #On fait un lien aléatoire entre les network servers et les join servers.
    for i in range(nbNetworkServers):
        j = randint(1,nbJoinServers) #We take a random number of join server
        jServerPos =  sample([p for p in range(j)], j)
        for val in jServerPos:
            NetworkServers[i].addJoinServers(JoinServers[val])
            JoinServers[val].addNetworkServers(NetworkServers[i], NwkKey)
#            (x2,y2) = xjs[val],yjs[val]
#            (x1,y1) = xns[i],yns[i]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='y')
    
    #On fait un lien aléatoire entre les join servers et les application servers.
    for i in range(nbJoinServers):
        j = randint(nbAppServers//2,nbAppServers) #We take a random number of join server
        AServersPos =  sample([p for p in range(j)], j)
        for val in AServersPos:
            JoinServers[i].addapplicationServers(AppServers[val], AppKey)        
#            (x2,y2) = xas[val],yas[val]
#            (x1,y1) = xjs[i],yjs[i]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='k')
    
    
    
    #Cette partie du code n'a aucune utilité d'un point de vue code parceque le lien entre les nServers et les AppServers n'est pas implémenté.
#    for i in range(nbNetworkServers):
#        j = randint(nbAppServers//2,nbAppServers) #We take a random number of join server
#        AServersPos =  sample([p for p in range(j)], j)
#        for val in AServersPos:
#            (x2,y2) = xas[val],yas[val]
#            (x1,y1) = xns[i],yns[i]
#            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='k')
    
    
    
    #Ajout du EndDevice dans le joinServer
    for jserver in JoinServers:
        for endDevice in EndDevices:
            jserver.addDevices(endDevice.getDevEUI(), AppKey, AppKey)
    
    
#    plt.legend(title='Legend',title_fontsize=30,loc='center left',bbox_to_anchor=(1, 0.5))
#    plt.title("LoRaWAN Simulator")
    #plt.axis('off')
    
#    for circle in circles:
#        plt.gca().add_patch(circle)
#        plt.gca().get_xaxis().set_visible(False)
#        plt.gca().get_yaxis().set_visible(False)
#    
#    plt.savefig('Img.svg',bbox_inches='tight')
    pres = 0
    connectionTime = dict()
    start = time.time()
    end = dict()
    connectionRate = list()
    nbOfConnectedObjects = list()
    for i in range(nbOfConnectionIteration):
        NetworkServers[i].deactivation()
        threads = [] 
        for endDevice in EndDevices:
            if(endDevice.isConnected==False):
            #print(endDevice.getDevEUI(),"envoie son message")                
                threads.append(Thread(target = endDevice.joinRequestMessage, args=(434,)))
                #debut = time.time()
                #endDevice.joinRequestMessage(434)
                #fin = time.time()
                #connectionTime.append(fin-debut)

        for x in threads:
            x.start()
    
        for x in threads: #We wait untill all end device has send one join request message
            x.join()
            
        end[i] = time.time()

        cpt = 0
        
        for endDevice in EndDevices:
            if(endDevice.isConnected==True):
                cpt+=1
#            else :
                #endDevice.joinRequestMessage(434)
#                (x,y) = endDevice.getPosition()
#                plt.scatter(x,y,c='r',marker='x',s=1)
        nbOfConnectedObjects.append(cpt)
        #print("Number of connected end-Device : "+ str((cpt/nbOfEndDevice)*100)+"%")
        connectionRate.append((cpt/nbOfEndDevice)*100)
        if(cpt == pres):
            end[i] = end[i-1] #Just to prefent from devices that can't connect them to the network
        pres = cpt
        
    total = list()
    for i in range(nbOfConnectionIteration):
        total.append(end[i] - start)
        connectionTime[i] = 0
    plt.show()        

    d = dict()
    for endDevice in EndDevices:
        if(endDevice.isConnected):
            connectionTime[int(endDevice.DevNonce,2)-1] += endDevice.getConnectionTime()
            if( (int(endDevice.DevNonce,2)-1) in d):
                d[int(endDevice.DevNonce,2)-1] += 1
            else : 
                d[int(endDevice.DevNonce,2)-1] = 1

    for val in d:
        connectionTime[val] = connectionTime[val]/d[val]
        
    return [(cpt/nbOfEndDevice)*100,connectionTime ,total,connectionRate,nbOfConnectedObjects] #ConnectionTime en 2


for SF in ['SF7_DR6','SF7_DR5' ,'SF8_DR4']: # SpreedingFactor:
    liste = list()
    for j in [50 , 100 , 500 , 1000 ] :#, 10000 ]:#, 50000]: # , 1000 , 5000, 10000]:
        nbOfConnectionIteration = 50
        print(j)
        l = list()
        for i in range(4):
            WorldMp = WorldMap()
            #Mapsize,nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers = 150,j,1,1,1
            Mapsize,nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers = 150,j,10,10,1
            val = main(Mapsize , nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers,WorldMp ,nbOfConnectionIteration)
            val.append(j)
            l.append(val)
        #Average of the connection rate
        averageTotalConnectionRate = sum([val[0] for val in l])/(len(l))
        
        #Average connection time
        AverageConnectionTime = list()
        for i in range(nbOfConnectionIteration):
            AverageConnectionTime.append((sum([val[1][i] for val in l])/len(l)))
            
        #TotalPerIteration
        p = list()
        for val in l:
            p.append(val[2])
        taille = len(p)
        totalParIteration = list()
        for i in range(nbOfConnectionIteration):
            totalParIteration.append(sum([k[i] for k in p])/len(p))
        #Average number of connected end device
        averageConnectionRate = list()
        for i in range(nbOfConnectionIteration):
            averageConnectionRate.append(sum([val[3][i] for val in l])/len(l))

        #Average number of connected end device
        averagenbOfConnectedObjects = list()
        for i in range(nbOfConnectionIteration):
            averagenbOfConnectedObjects = sum([val[4][i] for val in l])/(len(l))
    
        liste.append([averageTotalConnectionRate,AverageConnectionTime ,totalParIteration,averageConnectionRate,averagenbOfConnectedObjects,j])    
        
    color = ['r','g','b','c','m','y']
    char = ['-' , '--' , '-.',':']
    #Statistique
    cpt=0
    for val in liste:
        plt.plot([(i+1) for i in range(len(val[3]))] ,[v for v in val[3]],linestyle =char[cpt] ,color=color[cpt],label=str(val[-1])+' devices')
        cpt += 1
    plt.title("Connection rate for the Spreading Factor:"+SF)
    plt.legend(loc='upper left')
    plt.show()
    cpt = 0
    for val in liste:
        plt.plot([(i+1) for i in range(len(val[2]))] ,[v for v in val[2]],linestyle =char[cpt] ,color=color[cpt],label=str(val[-1])+' devices')
        cpt += 1
    plt.grid()
    plt.title("Connection time for the Spreading Factor:"+SF)
    plt.legend(loc='upper left')
    plt.show()


"""
"""
plt.plot([(i+1) for i in range(len(val[3]))] ,[v for v in val[3]],color='k')
"""
"""
if __name__ == "__main__":
    args = sys.argv[1:]
    if(args[0] == '-i'):
        Mapsize , nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers = int(args[1]),int(args[2]),int(args[3]),int(args[4]),int(args[5])
        WorldMap = WorldMap()
        main(Mapsize , nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers,WorldMap ,1)
"""
"""
#Pour faire des threads
pr = cProfile.Profile()
pr.enable()

my_result = main(100 , 50, 8,10,40,WorlM)

pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats()

with open('test.txt', 'w+') as f:
    f.write(s.getvalue())
    
#Pour faire du thread
Le problème d'un tel simulateur, si on ne fait pas les envoies de requête en parallèle tous les joinrequestmessage seront refusés au bout d'un moment.
Donc pour palier à ce problème on va executer les commande en thread

from threading import Thread

def func1():
    print('Working1')
    for i in range(50):
        print(i)
        
def func2():
    print("Working2")

if __name__ == '__main__':
    func1()
    func2()
    print("###############################")
    Thread(target = func1).start()
    Thread(target = func2).start()
"""