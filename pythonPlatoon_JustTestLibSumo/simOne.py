# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 21:14:55 2017

@author: ll
"""
import libsumo

from  TrafficManager import *
from  simOneStep import *
import os,sys
import random

def simOne(simTimes,TM):
    print(str(simTimes)+"\n")
    lateralResolution = 0.01 
   
    path = os.getcwd()
    path2 = path+"\sumoCfg\my1LaneMap1NoVeh-server.sumocfg"
    sumoBinary = "sumo-gui.exe"
    sumoBinary = "sumo.exe"

    
    libsumo.start([sumoBinary,"-c", path2])

    TM.scenarioLoaded()

    # traci.vehicle.add(str,'r1',-3,0,3,0,'EBus');
   # %'routeID','depart','pos','speed','lane','typeID''for

    #for i in range(len(TM.vehQue)):
    #    veh = TM.vehQue[i]
    #    veh.speed = 0
    #    traci.vehicle.addLegacy(str(veh.id),"r1",-3,veh.position,veh.speed,veh.lane,"EBUS")

    stepNum = 0
    requireStop = 0
    while requireStop == 0 : 
        stepNum += 1
        [TM,stepNum,requireStop] = runOneStepSUMOSim(TM,stepNum)
       
    libsumo.close()
    
    srcFile = path+"\sumoCfg"+"\edge_N1.xml"
    destFile = path+"\sumoCfg"+"\edge_N1_"+str(simTimes)+"_"+str(TM.isSplit)+"_"+str(TM.isSC)+ ".xml"
    os.rename(srcFile, destFile)

    srcFile = path+"\sumoCfg"+"\edge_N1_FuelEmiss.xml"
    destFile = path+"\sumoCfg"+"\edge_N1_FuelEmiss_"+str(simTimes)+"_"+str(TM.isSplit)+"_"+str(TM.isSC)+ ".xml"
    os.rename(srcFile,  destFile)


    srcFile = path+"\sumoCfg"+"\summary.xml"
    destFile = path+"\sumoCfg"+"\summary_"+str(simTimes)+"_"+str(TM.isSplit)+"_"+str(TM.isSC)+ ".xml"
    os.rename(srcFile, destFile)

    return