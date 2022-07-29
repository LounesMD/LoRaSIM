# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:57:08 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""
import Server

class ApplicationServer(Server):
    def __init__(self,Identifiant):
        super().__init__(Identifiant)
        self.id = Identifiant
        self.AppSKey = dict()
        
    def getId(self):
        return self.id
        
    def SaveAppSKey(self, DevEUI, AppSKey):
        self.AppSKey[DevEUI] = AppSKey
        