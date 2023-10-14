# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 16:35:06 2022

@author: Lounès Meddahi
"""
import hashlib

class Block(object):
    """
    A class representing a block in a blockchain.

    Attributes:
        data (list): The data contained in the block.
        merkleroot (str): The Merkle root hash of the block's data.
        miner (str): The miner's identifier.
        timestamp (datetime): The timestamp of when the block was created.
        index (int): The index of the block in the blockchain.
        dataProvider: The data provider associated with the block.
        gamma: The gamma value associated with the block.

    Methods:
        getGamma(self): Returns the gamma value associated with the block.
        getDataProvider(self): Returns the data provider associated with the block.
        getMerkleRoot(self): Returns the Merkle root hash of the block's data.
        getTimeStamp(self): Returns the timestamp of the block.
        getIndex(self): Returns the index of the block.
        getMiner(self): Returns the miner's identifier.
        getData(self): Returns the data contained in the block.
        setMerkleRoot(self, data): Sets the Merkle root hash of the block's data.

    Note:
        - The Merkle root hash is calculated based on the block's data.
    """    
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
    """
    A utility class for working with blockchain blocks.

    This class extends the Block class and includes additional methods for calculating the block's hash
    and accessing the previous block.

    Attributes:
        previousBlock (Block): The previous block in the blockchain.
        hash (str): The hash value of the current block.

    Methods:
        getHash(self): Returns the hash value of the block.
        getPreviousBlock(self): Returns the previous block in the blockchain.

    Note:
        - The hash of the block is calculated based on various block attributes.
    """
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
    """
    A specialized class representing the genesis block of a blockchain.

    This class extends the Block class and is specifically designed for the first block in the blockchain.

    Attributes:
        hash (str): The hash value of the genesis block.

    Methods:
        getHash(self): Returns the hash value of the genesis block.

    Note:
        - The hash of the genesis block is calculated based on its attributes.
    """
    def __init__(self, timestamp, miner, data,dataProvider,gamma):
        super().__init__(0, timestamp, miner, data,dataProvider,gamma)
        m = hashlib.sha256()   
        val = str(self.getTimeStamp()).encode()+ str(self.merkleroot).encode()+ str(self.dataProvider).encode()  + str(self.gamma).encode()   
        m.update(val)
        self.hash = m.hexdigest()
    
    def getHash(self):
        return self.hash

        

def sameBlocks(bloc1 , bloc2):
    """
    Check if two blocks are the same based on their hash values.

    Args:
        bloc1 (Block): The first block to compare.
        bloc2 (Block): The second block to compare.

    Returns:
        bool: True if the blocks have the same hash value, False otherwise.
    """
    return (bloc1.getHash() == bloc2.getHash())