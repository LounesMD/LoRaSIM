# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 16:35:06 2022

@author: Lounes
"""
import Block
import datetime
from Block import *
import time

class Blockchain:    
    def __init__(self , threshold):
        self.blocks = []
        self.gamma = threshold #une fonction du temps
        #self.generateGenesisBlock()
        
    def generateGenesisBlock(self,dataProvider,time):
        if(len(self.blocks)==0):
            self.blocks.append(GenesisBlock(datetime.datetime.now(), 'BlockChain', ['Genesis Block'] , dataProvider , self.gamma(time)))
    
    def addBlock(self , block):
        if(len(self.blocks)==0): 
            if(block.getIndex()==0):
                self.blocks.append(block)
        elif(block.getPreviousBlock().getHash() == self.blocks[-1].getHash() and block.getIndex()==len(self.blocks)): #We check that the new block reference the good previous block. Because of the previous hash properties (the hash uses the hash of the previous block, we can use only one comparaison)
            self.blocks.append(block)
        else:
            print("the order is not respected")
        
    def getBlock(self , index):
        if(0<=index<(len(self.blocks))):
            return self.blocks[index]

    def getBlockChain(self):
        return self.blocks
    
    def getBCSize(self):
        return len(self.blocks)
    
    def printBlock(self, index:int):
            if(0<=index<=(len(self.blocks))-1):
                block = self.getBlock(index)
                print(f"In the block {block.getIndex()}, the informations are : \n timestamp : {block.getTimeStamp()} \n index : {block.getIndex()} \n miner : {block.getMiner()} \n data : {block.getData()} \n DataProvider : {block.dataProvider} \n Gamma(t) : {block.getGamma()}")
                
                
                
                
                
                
                
                
                
                