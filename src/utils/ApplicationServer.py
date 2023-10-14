# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:57:08 2022

@author: Lounès Meddahi (lounes.meddahi[at]gmail.com)
"""
from utils.Server import Server


class ApplicationServer(Server):
    def __init__(self,Identifiant):
        super().__init__(Identifiant)
        self.id = Identifiant
        self.AppSKey = dict()
        
    def getId(self):
        return self.id
        
    def SaveAppSKey(self, DevEUI, AppSKey):
        self.AppSKey[DevEUI] = AppSKey
        
def generateApplicationServers(nb, AppKey = 'Sixteen byte key'):
    """
    Generate a list of ApplicationServer instances.

    This function creates and returns a list of ApplicationServer instances based on the specified number.
    
    Parameters:
        nb (int): The number of ApplicationServer instances to generate.
        AppKey: The application key to be used for the generated servers.

    Returns:
        list: A list containing the generated ApplicationServer instances.
    """
    ApplicationServers = list()
    nb = nb
    for i in range(nb):
        ApplicationServers.append(ApplicationServer(AppKey))
    return ApplicationServers        