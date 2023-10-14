# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 13:47:49 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""
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
from Simulator_WithBlockchain.utils.NetworkServer import generateNetworkServers
from utils.JoinServer import generateJoinServers
import numpy as np
import matplotlib.pyplot as plt

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
    

AppKey = 'Sixteen byte key'
NwkKey = 'Sixteen byte key'

#Main For Time Connection and Connection Rate
def main(Mapsize ,  nbOfEndDevice, nbOfJoinServer,nbOfNetworkServers,nbOfAppServers,WorldMap,nbOfConnectionIteration , nbOfDownServer):
    """    
    Parameters
    ----------
    Mapsize : Integer
        Size in km of the map.
    nbOfEndDevice : Integer
        Number of generated devices.
    nbOfJoinServer : Integer
        Number of generated JoinServers.
    nbOfNetworkServers : Integer
        Number of generated NetworkServers.
    nbOfAppServers : Integer
        Number of generated AppServers.
    WorldMap : WorldMap
        Use to link the en devices and the gateways.
    nbOfConnectionIteration : Integer
         Maximum number of requests an end device can send to connect to the network.
    nbOfDownServer : Integer
        Number of network servers down. With this parameter, the experience will be made nbOfDownServer times (with 0,...,nbOfDownServer network servers down)
"""

    WorldMap = WorldMap
    size = Mapsize
    
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



    for ns1 in NetworkServers:
        for ns2 in NetworkServers:
            ns1.addnetworkServer(ns2)
    #Generation of Application Servers
    nbAppServers = nbOfAppServers
    AppServers = generateApplicationServers(nbAppServers)
    
    for Device in EndDevices:
        WorldMap.addEndDevice(Device)
    for gateway in Gateways:    
        WorldMap.addGateway(gateway)
    
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
     
    xns = list()
    yns = list()    
    for i in range(nbNetworkServers):
        xns.append(size*1100+5*1000+15000)
        yns.append((i*((size*1000)/nbNetworkServers))/2)
    plt.scatter(xns,yns, color = 'r', marker = 's' , s =3, label = 'Network Servers')
    
    xjs = list()
    yjs = list()
    for i in range(nbJoinServers):
        xjs.append((i*((size*1000)/nbJoinServers))/2 + size*1100 +15000)
        yjs.append(((size + size/2)/2)*1000 )
    plt.scatter(xjs,yjs, color = 'y', marker = 'd' , s =3 , label = 'Join Servers')
        
    xas = list()
    yas = list()
    for i in range(nbAppServers):
        xas.append(2*size*1000 + 15000)
        yas.append((i*((size*1000)/nbAppServers)))
    plt.scatter(xas,yas, color = 'k', marker = 'p' , s =3 , label = 'Application Servers')
    
    #Random link between gatways and network servers.
    for gateway in Gateways:
        j = 3 #randint(1,nbNetworkServers) #We take a random number of network server
        nserversPos =  sample([p for p in range(nbNetworkServers)], j)
        for val in nserversPos:
            NetworkServers[val].addGateway(gateway)
            gateway.addNetworkServers(NetworkServers[val])
            (x1,y1) = gateway.getPosition()
            (x2,y2) = xns[val],yns[val]
            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='r')
    
    #Random link between network servers and join servers.
    for i in range(nbNetworkServers):
        j = 3 #randint(1,nbJoinServers) #We take a random number of join server
        jServerPos =  sample([p for p in range(nbJoinServers)], j)
        for val in jServerPos:
            NetworkServers[i].addJoinServers(JoinServers[val])
            JoinServers[val].addNetworkServers(NetworkServers[i], NwkKey)
            (x2,y2) = xjs[val],yjs[val]
            (x1,y1) = xns[i],yns[i]
            plt.plot([x1,x2] , [y1,y2],linewidth=0.05,color='y')
    
    for ed in EndDevices:
        gtw = choice(ed.WorldMap.matriceAdjacenceVersGateway[ed.getDevEUI()])
        ns = choice([i for i in gtw.networkServers])
        js = choice([i for i in ns.joinServers.values()])
        ed.JoinEUI = js.getJoinEUI()
        js.addDevices(ed.getDevEUI() , ed.NwkKey , ed.AppKey)
    
    
    for js in JoinServers:
        js.sendDataToTheBlockchain()
        
    #for i in range(10):
       # NetworkServers[0].getBlockchain().printBlock(i)
       
        
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
    
    for circle in circles:
        plt.gca().add_patch(circle)
        plt.gca().get_xaxis().set_visible(False)
        plt.gca().get_yaxis().set_visible(False)
#    
#    plt.savefig('Img.svg',bbox_inches='tight')
    plt.show()
    
    di = dict()
    
    for k in range(nbOfDownServer):
        for ed in EndDevices:
            ed.isIdent = False
            ed.timeForIdentification = None
            ed.isConnected = False
        for ns in NetworkServers:
            ns.nbOfIdent = 0
            ns.checkDevNonce = dict()
            ns.joinRequestAlreadyProccessed = dict()
            ns.joinAcceptAlreadyProccessed = dict()
            ns.isDown = False
            
        for j in range(k):
            NetworkServers[j].isDown = True

        t = 0
        for ns in NetworkServers:
            if(ns.isDown):
                t += 1
            
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
                    threads.append(Thread(target = endDevice.joinRequestMessage, args=(434,)))
    
            for x in threads:
                x.start()
        
            for x in threads: #We wait untill all end device has send one join request message
                x.join()
    
            cpt = 0                        
            for endDevice in EndDevices:
                if(endDevice.isConnected==True):
                    cpt+=1
                    
        for ns in NetworkServers:
            cpt = 0
            if(ns.isDown ):
                cpt += 1

        nbId = 0                    
        cpt1 = 0    
        temps = 0
        for ed in EndDevices:
            if(ed.isIdent):
                cpt1 += 1
                temps += ed.timeForIdentification
        for ed in EndDevices:
            if(ed.isIdent):
                nbId+= 1
        if(cpt1 > 0):
            temps = temps/cpt1
        else:
            temps = 0
        
        di[k] = [nbId,temps , cpt]
    return di 


for SF in ['SF7_DR6']: # SpreedingFactor:
    d1 = dict()
    d2 = dict()
    liste = list()
    pd11 = list()
    pd12 = list()
    nbDevice = [5000 , 10000] 
    for j in nbDevice:
        d1[j] = []
        d2[j] = []
        nbOfServerDown = 10
        nbOfConnectionIteration = 30
        nbOfExper = 1
        print(j)
        l = list()
        val = 0
        val2 = 0
        pd1 = dict()
        pd2 = dict()
        p = list()
        for i in range(nbOfExper):
            print(i)
            WorldMp = WorldMap()
            #Mapsize,nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers = 150,j,1,1,1
            Mapsize,nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers,nbOfDownServer = 150,j,10,10,1,nbOfServerDown
            p.append(main(Mapsize , nbOfEndDevice,nbOfJoinServer, nbOfNetworkServers,nbOfAppServers,WorldMp ,nbOfConnectionIteration , nbOfDownServer))
        
        
        for k in range(nbOfServerDown):
            pd1[k] = 0
            for i in range(nbOfExper):
                pd1[k] += p[i][k][0]
            pd1[k] = pd1[k]/nbOfExper

        for k in range(nbOfServerDown):
            pd2[k] = 0
            for i in range(nbOfExper):
                pd2[k] += p[i][k][1]
            pd2[k] = pd2[k]/nbOfExper

        pd11.append(pd1)
        pd12.append(pd2)
    color = ['r','g','b','c','m','y']
    char = ['-' , '--' , '-.',':']
    #Statistique
    cpt=0
    for pd1 in pd11:
        plt.plot([i for i in range(nbOfServerDown)] ,[((v*100)/nbDevice[cpt]) for v in pd1.values()],linestyle =char[cpt] ,color=color[cpt],label=str(nbDevice[cpt])+' devices')
        cpt+=1
    plt.grid()
    plt.title("Identification success (With blockchain)")
    plt.legend(loc='lower right')
    titre = "Identification success (With blockchain)"
    plt.savefig(titre)
    plt.show()  
    cpt=0

    for pd2 in pd12:
        plt.plot([i for i in range(nbOfServerDown)] ,[v for v in pd2.values()],linestyle =char[cpt] ,color=color[cpt],label=str(nbDevice[cpt])+' devices')
        cpt+=1
    plt.grid()
    plt.title("Identification Delay (With blockchain)")
    plt.legend(loc='lower right')
    titre = "Identification Delay (With blockchain)"
    plt.savefig(titre)
    plt.show()    