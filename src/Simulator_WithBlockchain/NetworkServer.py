# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 15:55:07 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""

import datetime
from Server import *
import time
import random
import string
from Block import *
from Blockchain import*

class NetworkServer(Server):
        
    def __init__(self , bc):
        self.id = random.choice(string.printable)
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
        self.blockchain = bc
        self.nbOfIdent = 0
        self.isDown = False
        
    def validateData(self , block):
        joinServer = block.getDataProvider
        if(joinServer in self.joinServers):
            for elt in block.data:
                if(elt not in self.joinServers[joinServer].AcceptedDevices):
                    return False
            return True
        else:
            return False
        
    def initBlockchain(self , data , JoinEUI, timestamp, miner , time):
        #bc = Blockchain(threshold)
        self.blockchain.addBlock(GenesisBlock(timestamp, miner, data,JoinEUI,time))        
        #self.blockchain = bc
        self.shareTheBlockchain()
        
    def updateBlockchain(self , bc):
        self.blockchain = bc
    
    def changeBlockchain(self , bc):
        if(self.blockchain.getBCSize() < bc.getBCSize()):
            self.blockchain = bc
            
    def getBlockchain(self):
        return self.blockchain
    
    def shareTheBlockchain(self):
        for ns in self.networkServers:
            ns.blockchain = self.blockchain #Here, we change the blockchain of each network server because we are in a safe environnement. If not, you just have to implement the rules you want for your blockchain network..

    
    def addNewBlock(self , data , JoinEUI):
        nb = len(data)                      
        while(nb > 0):
            if(self.blockchain.getBCSize() == 0):
                self.initBlockchain(data[0:min(nb ,1000)] , JoinEUI, time.time(), self.id , time.time())
            elif(self.blockchain.getBCSize() != 0):
                previousBlock = self.blockchain.getBlock(self.blockchain.getBCSize()-1)
                block = BlockUtil(self.blockchain.getBCSize(), time.time(), self.id, previousBlock, data[0:min(nb ,1000)],JoinEUI,self.blockchain.gamma(time.time()))
                self.blockchain.addBlock(block)        
            self.shareTheBlockchain()
            del data [0:min(nb ,1000)]
            nb = len(data)

        
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
        if((self.isDown == False) and self.acceptabledevNonce(request)):
                Bool = True
                if((request[1] not in self.joinRequestAlreadyProccessed) or (self.joinRequestAlreadyProccessed[request[1]] != request[2])):
                    isFake = True
                    cpt = 0
                    prez = False
                    avant = time.time()
                    for block in self.blockchain.blocks: #We make the identification                         
                        if(request[0] == block.getDataProvider()):
                            cpt += 1
                            v = request[0] in self.joinServers and request[1] in block.getData()
                            prez = prez or (request[1] in block.getData())

                            if(v):
                                if(request[5].timeForIdentification == None):
                                    request[5].timeForIdentification =  time.time() - request[5].envoie
                                request[5].isIdent = True

                                #Checking to send the join request to the good join server 
                                #print(request[5].timeForIdentification)
                                #print("ident ",self.nbOfIdent)
                                time.sleep(0.5) #Time to sent the message to the join server
                                #self.joinRequestAlreadyProccessed[request[1]] = request[2]
                                self.nearestGateway[request[1]] = gatewayId
                                #self.shareTheInformationJoinRequest(request[1] , request[2])
                                self.joinServers[request[0]].processJoinRequestMessage(request)
                    if(request[5].isIdent == False):
                        if(request[5].fakeRequestTimeDetection == None):
                            request[5].fakeRequestTimeDetection = time.time() - request[5].envoie                                 

                
                
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
        return (minutes[0]*60 + minutes[1]) # Nous faisons un cas où nous somme sûr d'avoir des temps < heures donc on regarde que les secondes (et minutes)
    
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