# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:16:35 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""
from os import urandom
from Crypto import *
#.Cipher
import random
import string
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
import time
from random import *

from utils.Server import Server

class JoinServer(Server):
    def __init__(self,JoinEUI,capacity):
        super().__init__(JoinEUI)
        #https://www.thethingsnetwork.org/forum/t/lora-specifications-variing-definitions-of-devaddr/33853
        self.NwkId = '#' #We suppose there is a unique network server. 
        self.capacity = capacity
        self.AcceptedDevices = dict() #Pour chaque EndDevice nous avons les clés associées
        self.JoinEUI = JoinEUI #8 bytes identifier
        self.networkServers= dict()
        self.applicationServers = dict()
        self.MHDRJoinAccept = '0b00111000'
        self.Ip = 0
        self.nbCo = 0
      
    def sendDataToTheBlockchain(self):
        data = [elt for elt in self.AcceptedDevices.keys()]
        for ns in self.networkServers:
            ns.addNewBlock(data , self.JoinEUI)
        
    def isAlreadyConnected(self,DevEUI,DevNonce):
        return self.AcceptedDevices[DevEUI]['DevNonce']==DevNonce  #We are sure that the DevEUI is in the JoinServer because we check that before using this methode
    
    def getAcceptedDevices(self):
        return self.AcceptedDevices
    
    def addapplicationServers(self,ApplicationServer,AppKey):
        self.applicationServers[ApplicationServer] = AppKey

    def processJoinRequestMessage(self, request):
        #if(request[1] in self.getAcceptedDevices()): # This methode is useless because the identification is made in the network servers.
        self.keysGeneration(request) #     
        self.nbCo += 1
        return self.sendJoinAcceptMessage(request) #
        #else:
         #   request[5].fakeRequestTimeDetection = time.time() - request[5].envoie
        
    
    def sendJoinAcceptMessage(self,request):
        #1 Keys for the Application Servers
        for AppServer in self.applicationServers:
            AppServer.SaveAppSKey(request[1],self.AcceptedDevices[request[1]]['AppSKey'])
        #2 Keys for the networks servers
        for networkServer in self.networkServers:
            NwkSEncKey,FNwkSIntKey, SNwkSIntKey =self.AcceptedDevices[request[1]]['NwkSEncKey'],self.AcceptedDevices[request[1]]['FNwkSIntKey'],self.AcceptedDevices[request[1]]['SNwkSIntKey']
            networkServer.SaveNwkSEncKey(request[1],NwkSEncKey,FNwkSIntKey, SNwkSIntKey)        
        #3 JoinAcceptMessage for the End devices
        downlink = self.joinAcceptMessage(request) #On suppose un AppNonce aléatoire)
        for networkServer in self.networkServers:
            networkServer.forwardDownlink(downlink)

    def GetAppKeys(self,request):
        return [self.AcceptedDevices[request[1]]['AppSKey']] #Message pour la ApplicationServer avec : AppSKey

        
    def joinAcceptMessage(self , request):
        NetID = self.NwkId
        DevAddr = self.AcceptedDevices[request[1]]['DevAddr']
        DLSettings = '0' #Initialized at 0
        RXDelay = '0' #We suppose the RXDelay is 0
        #We encrypt the informations with aes128_ecb using the AppKey
        secret_AppKey = self.AcceptedDevices[request[1]]['AppKey']
        obj = AES.new(secret_AppKey.encode(), AES.MODE_ECB)
        msg = self.AcceptedDevices[request[1]]['JoinNonce'] + self.AcceptedDevices[request[1]]['NetID'] + DevAddr + DLSettings + RXDelay #10bytes
        msg = msg+(6*'0')
        return [obj.decrypt(msg.encode()) , request[1]] #TODO Remove the devEUI and use the MIC
    
        
    def addNetworkServers(self,NetworkServer,NwkKey):
        self.networkServers[NetworkServer] = NwkKey

    def getNetworkServers(self):
        return self.networkServers

    def getJoinEUI(self):
        return self.JoinEUI
    
    def addDevices(self,deviceEUI,NwkKey,AppKey):
        self.AcceptedDevices[deviceEUI] = dict()
        self.AcceptedDevices[deviceEUI]['NwkKey']  = NwkKey
        self.AcceptedDevices[deviceEUI]['AppKey']  = AppKey
        self.AcceptedDevices[deviceEUI]['DevNonce']  = '-0b0000000000000000' #To change if you want to be able to add a new Device with a DevNonce not equals to '0b0000000000000000'


        
    def isACorroectDevice(self,request):
        return (request[1] in self.AcceptedDevices)
    
    def randomIp(self):        
        v = f'{self.Ip:b}'
        self.Ip+=1
        return ('0'*(25-len(v)))+v
        
    def randomNwkAddr(self,length):
        result_str = ''.join(random.choice(string.printable) for i in range(length))
        return result_str 
    
    def randomNetID2Bytes(self):
        result_str = ''.join(random.choice(string.printable) for i in range(2))
        return result_str 


    def keysGeneration(self,request):
        # DevAddr = NwkId | NwkAddr on suppose un unique réseau donc unique NwkId, NwkAddr l'adresse réseau du EndDevice peut être définit de manière arbitraire, 
        DevAddr = self.NwkId + self.randomNwkAddr(3)
        self.AcceptedDevices[request[1]]['DevAddr'] = DevAddr #4bytes

        JoinNonce = get_random_byte(1) #On suppose un JoinNonce aléatoire
        self.AcceptedDevices[request[1]]['JoinNonce'] = JoinNonce
        NetID = self.NwkId + self.randomNetID2Bytes()#3bytes network id
        self.AcceptedDevices[request[1]]['NetID'] = NetID
        CFList = []
        
        #NwkSEncKey = aes128_encrypt(NwkKey, 0x04 | JoinNonce | JoinEUI | DevNonce | pad16)
        secret_NwkKey = self.AcceptedDevices[request[1]]['NwkKey']
        obj = AES.new(secret_NwkKey.encode(), AES.MODE_ECB)
        msg = '0x04'+JoinNonce+self.JoinEUI+request[2]+('0'*(32-len('0x04'+JoinNonce+self.JoinEUI+request[2]))) #J'ajoute un zéro pour avoir un message de 32bytes
        #print("LAAAAAAAAAAAAAAAAAA" , msg , len(msg))
        self.AcceptedDevices[request[1]]['NwkSEncKey' ] = obj.encrypt(msg.encode())
        
        #AppSKey = aes128_encrypt(AppKey, 0x02 | JoinNonce | JoinEUI | DevNonce | pad16)
        secret_AppKey = self.AcceptedDevices[request[1]]['AppKey']
        obj = AES.new(secret_AppKey.encode(), AES.MODE_ECB)
        msg = '0x02'+JoinNonce+self.JoinEUI+request[2]+('0'*(32-len('0x02'+JoinNonce+self.JoinEUI+request[2])))
        self.AcceptedDevices[request[1]]['AppSKey'] = obj.encrypt(msg.encode())

        #FNwkSIntKey = aes128_encrypt(NwkKey, 0x02 | JoinNonce | JoinEUI | DevNonce | pad16)
        msg = '0x01'+JoinNonce+self.JoinEUI+request[2]+('0'*(32-len('0x01'+JoinNonce+self.JoinEUI+request[2])))
        obj = AES.new(secret_NwkKey.encode(), AES.MODE_ECB)
        self.AcceptedDevices[request[1]]['FNwkSIntKey'] = obj.encrypt(msg.encode())

        #SNwkSIntKey = aes128_encrypt(NwkKey, 0x02 | JoinNonce | JoinEUI | DevNonce | pad16)
        msg = '0x02'+JoinNonce+self.JoinEUI+request[2]+('0'*(32-len('0x02'+JoinNonce+self.JoinEUI+request[2])))
        obj = AES.new(secret_NwkKey.encode(), AES.MODE_ECB)
        self.AcceptedDevices[request[1]]['SNwkSIntKey'] = obj.encrypt(msg.encode())

import string
    
def get_random_byte(length):
    result_str = ''.join(random.choice(string.printable) for i in range(length))
    return result_str

def get_random_string(length):
    #https://pynative.com/python-generate-random-string/
    # choose from all lowercase letter
    letters = string.printable 
    result_str = ''.join(choice(letters) for i in range(length))
    return result_str

def generateJoinServers(nb):
    """
    Class representing a Join Server in a LoRaWAN network.

    Attributes:
        JoinEUI (str): An 8-byte identifier for the Join Server.
        capacity (int): The maximum capacity of the Join Server.
        AcceptedDevices (dict): A dictionary of accepted devices with DevEUIs as keys.
        NwkId (str): A network identifier.
        networkServers (dict): A dictionary of network servers in the network.
        applicationServers (dict): A dictionary of application servers.
        MHDRJoinAccept (str): MHDR field value for Join Accept messages.
        Ip (int): An IP address.
        isUSed (bool): A flag indicating if the Join Server has been used.
        nbIdent (int): The number of identifications.

    Methods:
        isAlreadyConnected(self, DevEUI, DevNonce): Checks if a device with the given DevEUI and DevNonce is already connected.
        getAcceptedDevices(self): Returns the dictionary of accepted devices.
        addapplicationServers(self, ApplicationServer, AppKey): Adds an application server to the dictionary.
        processJoinRequestMessage(self, request): Processes a Join Request message.
        sendJoinAcceptMessage(self, request): Sends a Join Accept message to an end device.
        GetAppKeys(self, request): Returns the application keys for a request.
        joinAcceptMessage(self, request): Generates a Join Accept message.
        addNetworkServers(self, NetworkServer, NwkKey): Adds a network server to the dictionary.
        getNetworkServers(self): Returns the dictionary of network servers.
        getJoinEUI(self): Returns the JoinEUI.
        addDevices(self, deviceEUI, NwkKey, AppKey): Adds a device to the accepted devices dictionary.
        isACorroectDevice(self, request): Checks if a device is in the accepted devices.
        randomIp(self): Generates a random IP address.
        randomNwkAddr(self, length): Generates a random network address.
        randomNetID2Bytes(self): Generates random network ID bytes.
        keysGeneration(self, request): Generates keys for a device request.

    Note:
        - The JoinServer class represents the functionality and attributes of a Join Server in a LoRaWAN network.
    """
    AllJoinEUI = list()
    joinServers = list()
    for i in range(nb):
        JoinEUI = get_random_string(8)        
        while JoinEUI in AllJoinEUI:
            JoinEUI = get_random_string(8)        
        AllJoinEUI.append(JoinEUI)
        joinServers.append(JoinServer(JoinEUI , 0))
    return joinServers
