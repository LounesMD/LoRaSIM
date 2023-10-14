# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 16:35:06 2022

@author: Lounes
"""

import datetime
from Blockchain.Block import *
import time

class Blockchain:    
    """
    A class representing a simple PoI blockchain.

    Attributes:
        blocks (list): A list of blocks in the blockchain.
        gamma (function): A function representing the threshold as a function of time.

    Methods:
        __init__(self, threshold): Initializes a new blockchain with the specified threshold function.
        generateGenesisBlock(self, dataProvider, time): Generates and adds the genesis block to the blockchain.
        addBlock(self, block): Adds a new block to the blockchain if it follows the correct order.
        getBlock(self, index): Retrieves a block at the specified index.
        getBlockChain(self): Retrieves the entire blockchain.
        getBCSize(self): Returns the current size of the blockchain.
        printBlock(self, index): Prints information about a specific block in the blockchain.
    """
    def __init__(self , threshold):
        """
        Initializes a new blockchain.

        Args:
            threshold: A function representing the threshold as a function of time.
        """
        self.blocks = []
        self.gamma = threshold
        #self.generateGenesisBlock()
        
    def generateGenesisBlock(self,dataProvider,time):
        """
        Generates and adds the genesis block to the blockchain.

        Args:
            dataProvider: The data provider for the genesis block.
            time: The current time for the genesis block.
        """
        if(len(self.blocks)==0):
            self.blocks.append(GenesisBlock(datetime.datetime.now(), 'BlockChain', ['Genesis Block'] , dataProvider , self.gamma(time)))
    
    def addBlock(self , block):
        """
        Adds a new block to the blockchain if it follows the correct order.

        Args:
            block: The block to be added to the blockchain.
        """
        if(len(self.blocks)==0): 
            if(block.getIndex()==0):
                self.blocks.append(block)
        elif(block.getPreviousBlock().getHash() == self.blocks[-1].getHash() and block.getIndex()==len(self.blocks)): #We check that the new block reference the good previous block. Because of the previous hash properties (the hash uses the hash of the previous block, we can use only one comparaison)
            self.blocks.append(block)
        else:
            print("the order is not respected")
        
    def getBlock(self , index):
        """
        Retrieves a block at the specified index.

        Args:
            index (int): The index of the block to retrieve.

        Returns:
            Block: The block at the specified index.
        """
        if(0<=index<(len(self.blocks))):
            return self.blocks[index]

    def getBlockChain(self):
        """
        Retrieves the entire blockchain.

        Returns:
            list: A list of all blocks in the blockchain.
        """
        return self.blocks
    
    def getBCSize(self):
        """
        Returns the current size of the blockchain.

        Returns:
            int: The number of blocks in the blockchain.
        """
        return len(self.blocks)
    
    def printBlock(self, index:int):
        """
        Prints information about a specific block in the blockchain.

        Args:
            index (int): The index of the block to print.
        """                        
        if(0<=index<=(len(self.blocks))-1):
            block = self.getBlock(index)
            print(f"In the block {block.getIndex()}, the informations are : \n timestamp : {block.getTimeStamp()} \n index : {block.getIndex()} \n miner : {block.getMiner()} \n data : {block.getData()} \n DataProvider : {block.dataProvider} \n Gamma(t) : {block.getGamma()}")
                                    