# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:07:46 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""

import math
import time
from threading import Thread

class WorldMap():
    """
    Class to represent the mapping of end devices, gateways, and servers in a LoRaWAN network.

    Attributes:
        EndDevices (dict): A dictionary of end devices with DevEUIs as keys.
        Gateway (dict): A dictionary of gateways with identifiers as keys.
        NetworkServers (list): A list of network servers in the network.
        JoinServers (list): A list of join servers in the network.
        matriceAdjacenceVersGateway (dict): A dictionary representing the adjacency matrix from end devices to gateways.
        matriceAdjacenceVersEndDevices (dict): A dictionary representing the adjacency matrix from gateways to end devices.

    Methods:
        getGateways(self): Returns the dictionary of gateways.
        getmatriceAdjacenceVersEndDevices(self): Returns the adjacency matrix from gateways to end devices.
        getmatriceAdjacenceVersGateway(self): Returns the adjacency matrix from end devices to gateways.
        AjoutmatriceAdjacenceVersGateway(self, EndDevice): Updates the adjacency matrix from end devices to gateways.
        AjoutmatriceAdjacenceVersEndDevices(self, gateway): Updates the adjacency matrix from gateways to end devices.
        addEndDevice(self, EndDevice): Adds an end device to the map and updates the adjacency matrices.
        addGateway(self, gateway): Adds a gateway to the map and updates the adjacency matrices.
        addNetworkServers(self, NetworkServer): Adds a network server to the list.
        addJoinServers(self, JoinServer): Adds a join server to the list.
        ConnectToAGateway(self, frequency, request, DataRate): Connects an end device to a gateway for a given request.
        ConnectToEndDevice(self, Id, downlink): Connects to an end device for a downlink message.

    Note:
        - The WorldMap class represents the spatial relationships between end devices and gateways in the LoRaWAN network.
    """    
    def __init__(self):
        self.EndDevices = dict()
        self.Gateway = dict()
        self.NetworkServers= list()
        self.JoinServers = list()
        self.matriceAdjacenceVersGateway = dict()
        self.matriceAdjacenceVersEndDevices = dict()
    
    def getGateways(self):
        return self.Gateway       
    def getmatriceAdjacenceVersEndDevices(self):
        return self.matriceAdjacenceVersEndDevices

    def getmatriceAdjacenceVersGateway(self):
        return self.matriceAdjacenceVersGateway

    def AjoutmatriceAdjacenceVersGateway(self, EndDevice):
        cpt = 0 #This cpt is used to know if the end device was added or not. It prevents from not getting every end device in the matrix, even those which are connected to any gateway
        for gateway in self.Gateway.values():
            #We suppose that the range of an end device is 15km
            if(math.sqrt((EndDevice.getPosition()[0]-gateway.getPosition()[0])**2
                         + (EndDevice.getPosition()[1]-gateway.getPosition()[1])**2)<15000):
                cpt +=1
                if((EndDevice.getDevEUI() in self.matriceAdjacenceVersGateway) and (not gateway in self.matriceAdjacenceVersGateway[EndDevice.getDevEUI()])):
                    #if((not gateway in self.matriceAdjacenceVersGateway[EndDevice.getDevEUI()])):
                        self.matriceAdjacenceVersGateway[EndDevice.getDevEUI()].append(gateway)
                else:
                    self.matriceAdjacenceVersGateway[EndDevice.getDevEUI()] = list()
                    self.matriceAdjacenceVersGateway[EndDevice.getDevEUI()].append(gateway)
        if(cpt == 0):
            self.matriceAdjacenceVersGateway[EndDevice.getDevEUI()] = list()
                    
                    
    def AjoutmatriceAdjacenceVersEndDevices(self,gateway):
        cpt = 0 #This cpt is used to know if the gateway was added or not. It prevents from not getting every gatewat in the matrix, even those which are connected to any end device
        for EndDevice in self.EndDevices.values():
            if( math.sqrt((EndDevice.getPosition()[0]-gateway.getPosition()[0])**2
                         + (EndDevice.getPosition()[1]-gateway.getPosition()[1])**2)<15000):
                cpt +=1 
                if((gateway.getId()  in self.matriceAdjacenceVersEndDevices) and (not EndDevice in self.matriceAdjacenceVersEndDevices[gateway.getId()])):    
                    #if((not EndDevice in self.matriceAdjacenceVersEndDevices[gateway.getId()])):
                        self.matriceAdjacenceVersEndDevices[gateway.getId()].append(EndDevice)
                else:
                    self.matriceAdjacenceVersEndDevices[gateway.getId()] = list()
                    self.matriceAdjacenceVersEndDevices[gateway.getId()].append(EndDevice)
        if(cpt == 0):
            self.matriceAdjacenceVersEndDevices[gateway.getId()] = list()      
        
    def addEndDevice(self,EndDevice):
        self.EndDevices[EndDevice.getDevEUI()] = EndDevice
        self.AjoutmatriceAdjacenceVersGateway(EndDevice)
        for gateway in self.Gateway.values():
            self.AjoutmatriceAdjacenceVersEndDevices(gateway)

    def addGateway(self,gateway):
        self.Gateway[gateway.getId()] = gateway
        self.AjoutmatriceAdjacenceVersEndDevices(gateway)
        for endDevice in self.EndDevices.values():
            self.AjoutmatriceAdjacenceVersGateway(endDevice)
        

    def addNetworkServers(self,NetworkServer):
        self.NetworkServers.append(NetworkServer)     
        
    def addJoinServers(self,JoinServer):
        self.JoinServers.append(JoinServer)     

    def ConnectToAGateway(self,frequency,request,DataRate):
        #Thread(target = time.sleep, args=(self.SpreadFactor[DataRate],)).start() #Time on air for the device
        for gateway in self.matriceAdjacenceVersGateway[request[1]]:
            if(gateway.acceptedFrequency(frequency)):
                #We check that the gateway can support the message
                if(gateway.isAvailable() ):
                    #Thread(target = gateway.forwardJoinRequestMessage, args=(request,)).start()
                    gateway.forwardJoinRequestMessage(request)
                #else:
                 #   print("Gateway not available")
            else:
                print("Not an accepted frequency")

                
    def ConnectToEndDevice(self, Id , downlink):
        for endDevice in self.matriceAdjacenceVersEndDevices[Id]:            
            if(endDevice.getDevEUI() == downlink[1]):
                endDevice.JoinAcceptMessage(downlink)

    
        