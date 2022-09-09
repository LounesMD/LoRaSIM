# LoRaSim Simulator
## LoRaSim Simulator
This package provides a simulator of the LoRaWAN 1.1 protocol and a simulator of the LoRaWAN protocol using the PoI-based blockchain for identification.

This simulator generates a LoRaWAN topology where end devices can join the network by performing a join procedure.
<p align="center">
  <img src="./Images/SimulatorLoRaWAN.PNG" />
</p>

Main contact: Lounès Meddahi (lounes.meddahi@gmail.com)

## Overview
The PoI-based blockchain LoRaWAN architecture aims to process the join procedure in the network servers instead of the join servers. For this, the join servers send their data (DevEUI associated to end devices authorized to connect the network) to the network servers wich create blocks to compose the blockchain.
<p align="center">
  <img src="./Images/ArchitectureLoRaWANWithWithoutBlockchain.png" />
</p>


## Implementation 
To implement the LoRaWAN simulator we have provided an object-oriented implementation in python.
<p align="center">
  <img src="./Images/SimulatorUML.svg" />
</p>

The blockchain can be fin in the [Block4PoId](https://github.com/LounesMD/Block4PoId) repository.