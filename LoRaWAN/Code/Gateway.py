# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 15:13:20 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""

import time
import datetime
from datetime import date

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
        a = time.time()
        for networkServer in self.networkServers:
            if(networkServer.isAvailable()and (networkServer.isDown == False)):
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
        
        
        
        
        