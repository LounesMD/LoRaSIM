# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 16:35:06 2022

@author: Lounès Meddahi
"""
import hashlib

 
    

class Block(object):
    
    def __init__(self, index, timestamp, miner, data, dataProvider , gamma):
        self.data = data
        self.merkleroot = self.setMerkleRoot(data)
        self.miner = miner 
        self.timestamp = timestamp
        self.index = index        
        self.dataProvider = dataProvider
        self.gamma =  gamma
    
    def getGamma(self):
        return self.gamma
    
    def getDataProvider(self):
        return self.dataProvider
    
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
                    for i in range(0 , len(merkleTree)-1, 2):                        
                        m.update(str(merkleTree[i]).encode() + str(merkleTree[i+1]).encode())
                        val[i//2] = m.hexdigest()      
                    val.append(merkleTree[-1])
                merkleTree = val.copy()
        return merkleTree
                
                
class BlockUtil(Block):
    def __init__(self, index, timestamp, miner, previousBlock, data,dataProvider , gamma):
        super().__init__(index, timestamp, miner, data,dataProvider,gamma)
        self.previousBlock = previousBlock #index-1 if index>0
        m = hashlib.sha256()   
    
        val = str(self.previousBlock.getHash()).encode() + str(self.getTimeStamp()).encode()+ str(self.merkleroot).encode() + str(self.dataProvider).encode() + str(self.gamma).encode()  
        m.update(val)
        self.hash = m.hexdigest()
    
    def getHash(self):
        return self.hash

    def getPreviousBlock(self):
        return self.previousBlock

                
class GenesisBlock(Block):
    def __init__(self, timestamp, miner, data,dataProvider,gamma):
        super().__init__(0, timestamp, miner, data,dataProvider,gamma)
        m = hashlib.sha256()   
        val = str(self.getTimeStamp()).encode()+ str(self.merkleroot).encode()+ str(self.dataProvider).encode()  + str(self.gamma).encode()   
        m.update(val)
        self.hash = m.hexdigest()
    
    def getHash(self):
        return self.hash

        

def sameBlocks(bloc1 , bloc2):
    return (bloc1.getHash() == bloc2.getHash())