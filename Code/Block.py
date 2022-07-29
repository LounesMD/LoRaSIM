# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 16:35:06 2022

@author: Lounes
"""
import hashlib

 
    

class Block(object):
    
    def __init__(self, index, timestamp, miner, data):
        self.data = data
        self.merkleroot = self.setMerkleRoot(data)
        self.miner = miner 
        self.timestamp = timestamp
        self.index = index         
        self.ProofOfIdentification #TODO
        
    def getMerkleRoot(self):
        return self.merkleroot
        
    def getTimeStamp(self):
        return self.timestamp
    
    def getIndex(self):
        return self.index
        
    def getMiner(self):
        return self.miner
    
    def getData(self):
        return self.data
        
    def setMerkleRoot(self,data:list):
        merkleTree = data.copy()
        if(len(merkleTree) == 1):
            m = hashlib.sha256()   
            m.update(str(merkleTree[0]).encode())
            merkleTree[0] = m.hexdigest()
        else:            
            while(len(merkleTree) !=1): #We suppose that there is always at least on transaction in the data list
                m = hashlib.sha256()   
                val = list()
                if(len(merkleTree)%2 == 0):
                    val = [0 for i in range(len(merkleTree)//2)]
                    for i in range(0 , len(merkleTree), 2):
                        m.update(str(merkleTree[i]).encode() + str(merkleTree[i+1]).encode())
                        val[i//2] = m.hexdigest()
                else:
                    val = [0 for i in range((len(merkleTree)-1)//2)]
                    for i in range(0 , len(merkleTree), 2):
                        m.update(str(merkleTree[i]).encode() + str(merkleTree[i+1]).encode())
                        val[i//2] = m.hexdigest()      
                    val.append(merkleTree[-1])
                merkleTree = val.copy()
        return merkleTree
                
                
class BlockUtil(Block):
    def __init__(self, index, timestamp, miner, previousBlock, data):
        super().__init__(index, timestamp, miner, data)
        self.previousBlock = previousBlock #index-1 if index>0
        m = hashlib.sha256()   
        val = str(self.previousBlock.getHash()).encode() + str(self.getTimeStamp()).encode()+ str(self.merkleroot).encode() 
        m.update(val)
        self.hash = m.hexdigest()
    
    def getHash(self):
        return self.hash

    def getPreviousBlock(self):
        return self.previousBlock

                
class GenesisBlock(Block):
    def __init__(self, index, timestamp, miner, data):
        super().__init__(index, timestamp, miner, data)
        m = hashlib.sha256()   
        val = str(self.getTimeStamp()).encode()+ str(self.merkleroot).encode() 
        m.update(val)
        self.hash = m.hexdigest()
    
    def getHash(self):
        return self.hash

        

def sameBlocks(bloc1 , bloc2):
    return (bloc1.getTimeStamp() == bloc2.getTimeStamp() and
            bloc1.getMiner()==bloc2.getMiner() and
            bloc1.data == bloc2.data and
            sameBlocks( bloc1.previousBlock() , bloc2.previousBlock()))