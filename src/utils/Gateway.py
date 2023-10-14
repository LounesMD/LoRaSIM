# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 15:13:20 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""
import string
import time
import datetime
from datetime import date
from random import *

class Gateway:
    def __init__(self,pos,Id,WorldMap,Frequencyband,capacity):
        """
        Parameters
        ----------
        pos : tuple
            position of the gateway in the map.
        Id : string
            id of the gateway. Useful when it is unique
        WorldMap : WorldMap
            Map in wich the gateway will be deployed.
        Frequencyband : string
            Frenquency band used. If you need more frequency band that available in EU, change self.Frequencies. Refer To : https://wifivitae.com/2021/06/29/lorawan-freq/
        capacity : int.
            Capacity of the gateway. Normaly millions.
        """
        
        self.Frequencies = {'EU433':[433.05 , 434.79],'EU863 ':[868.1 , 868.5]}  #We use the european bands. 433.05 to 434.79 MHz For EU433 and 868.1 to 868.5 MHz for EU863 
        self.Frequencyband = Frequencyband
        self.WorldMap = WorldMap
        self.id = Id
        self.Position = pos
        self.networkServers= list()
        self.time = time.time()     #To be used to reset the self.managedMessages every second
        self.supportedMessages = capacity #according to https://lora-developers.semtech.com/documentation/tech-papers-and-guides/lora-and-lorawan/, it should be 28
        self.lastUpdate = datetime.datetime.now()
        self.managedMessages = 0 #This paramet is used to limit the number of message per second
        
        
        
    def isAvailable(self):
        """
        Return true if the gateway is available and false else
        
        Returns
        -------
        Boolean
        """
        diff = datetime.datetime.now()-self.lastUpdate    
        if(diff.total_seconds()>1): #The gateway can deals 100000 per day, so 28per seconds. After 1sec we put the counter to 0 and we restart everything
            self.lastUpdate = datetime.datetime.now()
            self.managedMessages = 1
            return True
        else: #We check that the gateway didn't already deals with 100 000 message
            res = ((self.supportedMessages - self.managedMessages)>0)
            self.managedMessages += 1
            return res

    def getId(self):
        """
        Return the ID
        Returns
        -------
        String
        """
        return self.id

    def getAcceptedNetworkServers(self):
        """
        return the network servers with which the gateway is linked
        """
        return self.networkServers

    def addNetworkServers(self,NetworkServer):
        """        
        Add a new network server among those which are linked to the gateway
        Parameters
        ----------
        NetworkServer : NetworkServer
            DESCRIPTION.

        """
        self.networkServers.append(NetworkServer)

    @DeprecationWarning
    def addFrequency(self,freq):
        self.frequencies.append(freq)
    
    def getPosition(self):
        """
        Return the position
        Returns
        -------
            TUPLE
        """
        return self.Position
    
    def acceptedFrequency(self , frequency):
        """
        We check that the end device uses an accepted frequency in EU
        Parameters
        ----------
        frequency : TYPE
            DESCRIPTION.
        """
        return( self.Frequencies[self.Frequencyband][0]<frequency<self.Frequencies[self.Frequencyband][1])

    def forwardJoinRequestMessage(self,request):
        """        
        Parameters
        ----------
        request : list
            Join request message to forward to network servers.
        """
        for networkServer in self.networkServers:
            if(networkServer.isAvailable()):
                networkServer.forwardJoinRequestMessage(request , self)
            #else:
             #   print("Network Server not available")
                
    def forwardJoinAcceptMessage(self,downlink): 
        """        
        Parameters
        ----------
        downlink : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.WorldMap.ConnectToEndDevice(self.id , downlink)

    def ForwardUpLink(self,Message):
        #TODO
        return 
     
    def ForwardDownLink(self,Message):
        #TODO
        return        

def get_random_string(length):
    #https://pynative.com/python-generate-random-string/
    # choose from all lowercase letter
    letters = string.printable 
    result_str = ''.join(choice(letters) for i in range(length))
    return result_str

def generateRandomGateway(nb, WorldMap,size, frequence = 'EU433'):
    """
    Generate random gateways with specified parameters.

    This function generates a specified number of random gateways on a grid represented by a WorldMap.
    
    Parameters:
        nb (int): The number of gateways to generate.
        WorldMap: An instance of the WorldMap class representing the grid.
        size (int): The size of the grid (assumed to be square).

    Returns:
        tuple: A tuple containing two lists:
            - Gateways (list): A list of generated Gateway objects.
            - GatewaysPos (list): A list of positions (x, y) corresponding to the generated gateways.

    Note:
        - It is assumed that all generated gateways will use the 'EU433' frequency by default.
        - Gateway IDs are generated using a random string followed by an index.
    """    
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

def generateSmartGateway(WorldMap,size,capacity,frequence = 'EU433'):
    """
    Generate more optimaly the gateways.

    This function generates gateways on a grid represented by a WorldMap, ensuring one gateway
    every 15 kilometers on the grid.

    Parameters:
        WorldMap: An instance of the WorldMap class representing the grid.
        size (int): The size of the grid (assumed to be square) in meters.
        capacity (int): The capacity of the generated gateways.

    Returns:
        tuple: A tuple containing two lists:
            - Gateways (list): A list of generated Gateway objects.
            - GatewaysPos (list): A list of positions (x, y) corresponding to the generated gateways.

    Note:
        - It is assumed that all generated gateways will use the 'EU433' frequency by default.
        - Gateway IDs are generated using a random string followed by an index.
        - Gateways are generated such that there is one gateway every 15 kilometers on the grid.
          The grid is divided into cells of size 15 kilometers by 15 kilometers, and a gateway is placed
          at the center of each cell.
    """    
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