# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 15:55:07 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""

import datetime
import time

from utils.Server import Server

class NetworkServer(Server):
    """
    A class representing a network server in a LoRaWAN network.

    Attributes:
        supportedMessages (int): The maximum number of supported messages by the network server.
        gateways (list): A list of gateways connected to the network server.
        joinServers (dict): A dictionary of join servers with JoinEUI as keys.
        checkDevNonce (dict): A dictionary to check DevNonce for preventing replay attacks.
        NwkSEncKey (dict): A dictionary to store NwkSEncKey, FNwkSIntKey, and SNwkSIntKey keys for DevEUIs.
        lastUpdate (datetime): The timestamp of the last update for managing supported messages.
        managedMessages (int): The number of managed messages.
        appServers (dict): A dictionary of application servers with identifiers as keys.
        HS (bool): Indicates whether the network server is in a high-security mode.
        networkServers (list): A list of network servers connected to this network server.
        joinAcceptAlreadyProccessed (dict): A dictionary to track processed join accept messages.
        nearestGateway (dict): A dictionary to store the nearest gateway for each device.
        joinRequestAlreadyProccessed (dict): A dictionary to track processed join request messages.
        isDown (bool): Indicates whether the network server is down.

    Methods:
        addnetworkServer(self, ns): Adds a network server to the list of connected network servers.
        deactivation(self): Deactivates the network server.
        isAvailable(self): Checks if the network server is available for message processing.
        SaveNwkSEncKey(self, DevEUI, NwkSEncKey, FNwkSIntKey, SNwkSIntKey): Saves security keys for a DevEUI.
        addJoinServers(self, joinServer): Adds a join server to the network server.
        addGateway(self, gateway): Adds a gateway to the network server.
        forwardJoinRequestMessage(self, request, gatewayId): Forwards a join request message to the appropriate join server.
        shareTheInformationJoinRequest(self, devEUI, DevNonce): Shares information about a join request with other network servers.
        shareTheInformationJoinAccepte(self, devEUI, gatewayId): Shares information about a join accept with other network servers.
        forwardDownlink(self, downlink): Forwards a downlink message to the nearest gateway.
        isATimeoutRequest(self, request): Checks if a request is a timeout message based on timestamp.
        acceptabledevNonce(self, request): Checks if DevNonce is acceptable for preventing replay attacks.
        addApplicationServer(self, appServer): Adds an application server to the network server.
        forwardUpLink(self, uplink): Forwards an uplink message (not implemented yet).

    Note:
        - The NetworkServer class is a part of a LoRaWAN network and interacts with gateways, join servers,
          application servers, and other network servers.
        - Some methods and attributes are specific to LoRaWAN network management and security.
    """
    def __init__(self):
        self.supportedMessages = 1000000 #According to https://lora-developers.semtech.com/documentation/tech-papers-and-guides/lora-and-lorawan/
        self.gateways = list()
        self.joinServers= dict()
        self.checkDevNonce = dict() #{DevEUI : DevNonce}  To check if we are not subjed to a replay attack
        self.NwkSEncKey = dict() #Stock the NwkSEncKey,FNwkSIntKey, SNwkSIntKey keys associated to a specific DevEUI
        self.lastUpdate = datetime.datetime.now() #Used in order to process only self.supportedMessages per second
        self.managedMessages = 0
        self.appServers = dict()
        self.HS = False
        self.networkServers = list()
        self.joinAcceptAlreadyProccessed = dict()
        self.nearestGateway = dict()
        self.joinRequestAlreadyProccessed = dict()
        self.isDown = False
        
    def addnetworkServer(self , ns):
        self.networkServers.append(ns)
    
    def deactivation(self):
        self.HS = True

    def isAvailable(self):
        """
        Return true it the network is available and false else
        """
        if (not self.HS):
            diff = datetime.datetime.now()-self.lastUpdate    
            if(diff.total_seconds()>1): #The gateway can deals 100000 per day, so 28per seconds. After 1sec we put the counter to 0 and we restart everything
                self.lastUpdate = datetime.datetime.now()
                self.managedMessages = 1
                return True
            else: #We check that the gateway didn't already deals with 100 000 message
                res = ((self.supportedMessages - self.managedMessages)>0)
                self.managedMessages += 1
                return res
        else:
            return True
            
    def SaveNwkSEncKey(self, DevEUI, NwkSEncKey,FNwkSIntKey, SNwkSIntKey):
        self.NwkSEncKey[DevEUI] = (NwkSEncKey,FNwkSIntKey, SNwkSIntKey)        
        
        
    def addJoinServers(self,joinServer):
        if(joinServer.getJoinEUI() not in self.joinServers.values()):
            self.joinServers[joinServer.getJoinEUI()] = joinServer
                
    def addGateway(self,gateway):
        self.gateways.append(gateway)        
    
    def forwardJoinRequestMessage(self,request,gatewayId):    
        if(self.acceptabledevNonce(request) and (request[0] in self.joinServers)):
            #self.joinRequestAlreadyProccessed[request[1]] = request[2]
            self.nearestGateway[request[1]] = gatewayId
            #self.shareTheInformationJoinRequest(request[1] , request[2])
            time.sleep(0.5)#Time to sent the message to the join server
            self.joinServers[request[0]].processJoinRequestMessage(request)
                
    def shareTheInformationJoinRequest(self , devEUI, DevNonce):
        """
        This method share information to others network server.
        We make the hypothesis that every network servers are connected. But if not, just modify it the spread the information to those you want
        """
        for ns in self.networkServers:
            ns.joinRequestAlreadyProccessed[devEUI] = DevNonce

    def shareTheInformationJoinAccepte(self , devEUI, gatewayId):
        for ns in self.networkServers:
            ns.joinAcceptAlreadyProccessed[devEUI] = gatewayId


    def forwardDownlink(self, downlink):
        if(downlink[1] in self.nearestGateway):
            if(self.nearestGateway[downlink[1]].isAvailable()):
                if(downlink[1] not in self.joinAcceptAlreadyProccessed):
                    #self.joinAcceptAlreadyProccessed[downlink[1]] = True
                    #self.shareTheInformationJoinAccepte(downlink[1], self.nearestGateway[downlink[1]].getId())
                    self.nearestGateway[downlink[1]].forwardJoinAcceptMessage(downlink)
        
    def isATimeoutRequest(self, request):
        a = request[3]
        b = datetime.datetime.now()
        c = b-a
        minutes = divmod(c.total_seconds(), 60)
        return (minutes[0]*60 + minutes[1])
    
    def acceptabledevNonce(self,request):
        """
        return True if it is the first time that the endDevice uses the DevNonce and not a timeout message
        """
        timeout = self.isATimeoutRequest(request)
        if(timeout < 15):
            if((request[1] not in self.checkDevNonce) ):
                self.checkDevNonce[request[1]] = request[2]
                return True
            return (request[2] not in self.checkDevNonce[request[1]])
        print("TimeoutMessage")
        return False
        
    
    def addApplicationServer(self,appServer):
        self.appServers[appServer.getid()] = appServer
        
    def forwardUpLink(self , uplink):
        #TODO
        return
    

def generateNetworkServers(nb):
    """
    Generate a list of NetworkServer instances.

    Parameters:
        nb (int): The number of NetworkServer instances to generate.

    Returns:
        list: A list containing the generated NetworkServer instances.
    """
    networkServers = list()
    for i in range(nb):
        networkServers.append(NetworkServer())
    return networkServers
