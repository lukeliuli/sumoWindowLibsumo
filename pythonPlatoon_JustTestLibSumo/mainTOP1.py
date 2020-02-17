# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 20:24:18 2017

@author: ll
"""
import os, sys

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:   
     sys.exit("please declare environment variable 'SUMO_HOME'")
     
# sys.path.append(os.path.join('c:', os.sep, 'whatever', 'path', 'to', 'sumo', 'tools'))




import simOne 
from  TrafficManager import *
TM = PlatoonTrafficManager()

for i in range(4,21):
    TM = PlatoonTrafficManager()
   
    TM.platoonSize = i
    TM.isSplit = 0
    TM.isSC = 0
    
    TM.scenarioLoaded()
    simOne.simOne(i,TM)
    

