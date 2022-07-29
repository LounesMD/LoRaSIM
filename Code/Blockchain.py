# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 16:35:06 2022

@author: Lounes
"""
import Block
import datetime
from Block import *

class Blockchain:
    
    def __init__(self):
        self.blocks = []
        self.generateGenesisBlock()
        
    def generateGenesisBlock(self):
        if(len(self.blocks)==0):
            self.blocks.append(Block(0 , datetime.datetime.now(), 'BlockChain', ['Genesis Block']))
    
    def addBlock(self , block):
        if(block.getPreviousBlock().getHash() == self.blocks[-1].getHash()): #We check that the new block reference the good previous block. Because of the previous hash properties (the hash uses the hash of the previous block, we can use only one comparaison)
            self.blocks.append(block)
        print("the order is not respected")
        
    def getBlock(self , index):
        if(0<=index<(len(self.blocks))):
            return self.blocks[index]

    def getBlockChain(self):
        return self.blocks
    
    def printBlock(self, index:int):
            if(0<=index<=(len(self.blocks))):
                block = self.getBlock(index)
                print(f"In the block {block.getIndex()}, the informations are : \n timestamp : {block.getTimeStamp()} \n index : {block.getIndex()} \n miner : {block.getMiner()} \n data : {block.getData()}")
                
                
                
                
                
                
                
                
                
                