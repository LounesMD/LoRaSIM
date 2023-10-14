# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:43:36 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""
import string
import time
import datetime
from os import urandom
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from random import *

class EndDevice(object):    
    def __init__(self,DevEUI, JoinEUI, AppKey, NwkKey,Coo,WorldMap,SpreadingFactor):
        """        

        Parameters
        ----------        
        DevEUI : string (for bytes)
            8 bytes unique end device identifier.
        JoinEUI : string (for bytes)
            8 bytes unique identifier of the join server that will be used by the end device to join the network.
        AppKey : string (for bytes)
            16 bytes application key. Used to generate the AppSKey
        NwkKey : string (for bytes)
            16 bytes network key. Used to generate the NwkSEncKey, SNwkSIntKey, FNwkSIntKey keys.
        Coo : tuple
            position of the EndDevice in the map.
        WorldMap : WorldMap
            Map in wich the end device will be deployed
        SpreadingFactor : string
            Spreading factor of the end device. "Lower spreading factors mean faster chirps and therefore a higher data transmission rate." #ref : https://www.thethingsnetwork.org/docs/lorawan/spreading-factors/
        """
        
        self.SpreadingFactor ={'SF7_DR6' : 0.1844, 'SF7_DR5' : 0.3689, 'SF8_DR4':0.6559, 'SF9_DR3':1.1684, 'SF10_DR2':2.132,'SF11_DR1':4.6735,'SF12_DR0':8.364} #airtime associed to every spread factor
        self.fakeRequestTimeDetection = None #We use this parameter to measure the exact time required to detect if the end device sent a join request to a join server without being registred
        self.SP = SpreadingFactor
        self.isConnected = False # True if the device is connected to the network.
        self.Delay = None #time during which the object can receive a message 
        self.WorldMap = WorldMap
        self.DevEUI = DevEUI
        self.JoinEUI = JoinEUI
        self.AppKey = AppKey
        self.NwkKey = NwkKey
        self.AppSKey = None
        self.NwkEncSKey = None
        self.DevNonce = '0b0000000000000000' #Start from 0 and is incremented at every join request sent
        self.Position = Coo
        self.JoinNonce = None #Nonce to generate the session keys
        self.envoie = None #Time when the object sent the request
        self.retour = None #Time when the object received the request
        self.timeForIdentification = None
        self.isIdent = False
        # please refer to : https://lora-alliance.org/wp-content/uploads/2020/11/lorawantm_specification_-v1.1.pdf

        # MIC :
        # msg = MHDR | JoinEUI | DevEUI| Devnonce
        # cmac = aes128_cmac(AppKey,  msg)
        # MIC = cmac[0..3]        
        # MHDR = MType | RFU | Major
        self.MHDRJoinRequest = '0b00011000'
                
        self.joinAcceptMessage = None
        
    def getJoinEUI(self):
        """
        Return the joinEUI
        """
        return self.JoinEUI 
        
    def disconnectTheEndDevice(self):
        """        
        Disconnect the end device of its current network
        """
        self.isConnected = False
        
    def getMICJoinRequest(self):
        """        
        Returns
        -------
        string
            MIC to use with the joinRequestMessage.
        """
        secret = bytes(self.AppKey , 'UTF-8')
        cobj = CMAC.new(secret, ciphermod=AES)
        msg = self.MHDRJoinRequest[2:]+self.JoinEUI+self.DevEUI+self.DevNonce[2:]
        cobj.update(bytes(msg,'UTF-8'))
        return cobj.hexdigest()[:3]
    
    
    def getPosition(self):
        """
        Return the current position of the end device
        """
        return self.Position
    
    def getDevEUI(self):
        """ 
        Return the DevEUI
        """
        return self.DevEUI
        
    def incrementDevNonce(self):
        """
        Increment the DevNonce (/!\It's a binary number (bits) and not an integer).
        """
        self.DevNonce = bin(int(self.DevNonce , 2)+1)
        
    def joinRequestMessage(self,frequency):
        """
        If the end device is not connected, this method will generate a join request message and send it to the nearest gateways
        Parameters
        ----------
        frequency : float
            frequency on which to send the request.
        """
        if(not self.isConnected):
            self.envoie = time.time()
            request = self.generateJoinRequestMessage()
            time.sleep(self.SpreadingFactor[self.SP])#Time on air for the device
            self.WorldMap.ConnectToAGateway(frequency,request,self.SP)
            self.incrementDevNonce()     
        #else:
            #print("The EndDevice is already connected")

    def JoinAcceptMessage(self,JoinAcceptMessageEncrypted):
        """
        This methode decrypt the join accept message and stock it
        We use obj_encrypt to decrypt the join accept message because the end device only implement the decrypt function. Refer to : https://lora-alliance.org/wp-content/uploads/2020/11/lorawantm_specification_-v1.1.pdf page 56.
        
        Parameters
        ----------
        JoinAcceptMessageEncrypted : list
            Encrypted join accept message.

        Returns
        -------
        None.

        """
        if(self.isConnected == False):
            #The JoinAcceptMessage is encrypted with the NwkKey. So we need the same key to unencrypt the msg
            secret_NwkKey = self.NwkKey
            obj = AES.new(secret_NwkKey.encode(), AES.MODE_ECB)
            # joinAcceptMessage =  JoinNonce	NetID	 DevAddr	DLSettings	RXDelay	MIC
            JoinAcceptMessageEncrypted = JoinAcceptMessageEncrypted[0]
            joinAcceptMessageUnencrypted = obj.encrypt(JoinAcceptMessageEncrypted)
            self.joinAcceptMessage = joinAcceptMessageUnencrypted 
            self.isConnected = True
            self.retour = time.time()
            return #Should be removed
        
    def getConnectionTime(self):
        """        
        Connection time of the end device
        Returns
        -------
        time
        """
        return self.retour - self.envoie        
    
    def DownLink(self , downLink):
        #TODO
        return
    
    def UpLink():
        #TODO
        return
    
    def fakeJoinRequestMessage(self,frequency):
     """
     The same as JoinRequestMessage but use self.gnerateFakeJoinRequestMessage() to generate the request
     Parameters
     ----------
     frequency : float
         frequency on which to send the request.
     """
     if(not self.isConnected):
         self.envoie = time.time()
         request = self.gnerateFakeJoinRequestMessage()
         time.sleep(self.SpreadingFactor[self.SP])#Time on air for the device
         self.WorldMap.ConnectToAGateway(frequency,request,self.SP)
         self.incrementDevNonce() 
            
    def gnerateFakeJoinRequestMessage(self):
        """
        We call it fakeJoinRequestMessage because I used it to send the endDevice with the request to safe the required time to detect this join request message.
        So, to use it, you should not stock this end device in a join server.        
        Returns
        -------
        list
            Fake join request message.
        """
        return [self.JoinEUI,self.DevEUI,self.DevNonce, datetime.datetime.now(), self.getMICJoinRequest(),self] 
        
        
    def generateJoinRequestMessage(self):
        """        
        This methode generate a join request message
        Returns
        -------
        list
            join request message.
        """
        #self.timeForIdentification = time.time()
        return [self.JoinEUI,self.DevEUI,self.DevNonce, datetime.datetime.now(), self.getMICJoinRequest() , self]
    
class ClassA(EndDevice):
    """
    Class A device
    """
    def __init__(self, DevEUI, JoinEUI, AppKey, NwkKey, Coo):
        super().__init__(DevEUI, JoinEUI, AppKey, NwkKey, Coo)


def get_random_string(length):
    #https://pynative.com/python-generate-random-string/
    # choose from all lowercase letter
    letters = string.printable 
    result_str = ''.join(choice(letters) for i in range(length))
    return result_str


def generateRandomEndDevice(nb , JoinServerAvailable , WorldMap,size , SF, AppKey = 'Sixteen byte key', NwkKey = 'Sixteen byte key'):
    """
    Generate random end devices and connect them to random join servers.

    This function generates a specified number of random end devices and connects them to random join servers.
    
    Parameters:
        nb (int): The number of end devices to generate.
        JoinServerAvailable (list): A list of available JoinServer instances for connecting end devices.
        WorldMap: An instance of the WorldMap class representing the grid.
        size (int): The size of the grid (assumed to be square) in meters.
        SF (int): The spreading factor for the generated end devices.
        AppKey (string): Application networks key
        NwkKey (string): Network servers key
    Returns:
        tuple: A tuple containing two lists:
            - EndDevices (list): A list of generated EndDevice instances.
            - EndDevicesPos (list): A list of positions (x, y) corresponding to the generated end devices.

    Note:
        - Each end device is assigned a unique DevEUI.
        - End devices are connected to random join servers from the provided list.
        - The AppKey and NwkKey are not generated within this function; they should be provided elsewhere.
        - The Spreading Factor (SF) is specified for all generated end devices.
        - End devices are placed randomly within the specified grid.
    """
    AllDevEUI = list()
    EndDevices = list()
    EndDevicesPos = list()
    for i in range(nb):
        DevEUI = get_random_string(8)        
        while DevEUI in AllDevEUI:
            DevEUI = get_random_string(8) 
            
        JoinServer = choice(JoinServerAvailable)
        JoinEUI = JoinServer.getJoinEUI()
        JoinServer.addDevices(DevEUI , AppKey , NwkKey)
        
        (x,y) = (randint(0,size) , randint(0,size)) #1000km x 1000km
        EndDevicePos = (x,y)
        SpF = SF #choice(list(SpreedingFactor.keys()))
        endDevice = EndDevice(DevEUI, JoinEUI, AppKey, NwkKey, EndDevicePos, WorldMap,SpF)
        EndDevices.append(endDevice)
        EndDevicesPos.append((x,y))
        AllDevEUI.append(DevEUI)
    return EndDevices,EndDevicesPos
