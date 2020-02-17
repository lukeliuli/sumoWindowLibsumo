# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 22:08:15 2017

@author: ll
"""
import libsumo
from  TrafficManager import *
import random





def runOneStepSUMOSim(TM,stepNum):

    requireStop = 0;
    timeT = libsumo.simulation.getCurrentTime();#当前时间
    vehicles = libsumo.vehicle.getIDList();#当前在道路上的车辆
    curTime = timeT/1000
    #for len(vehicles)>0:
    #    traci.vehicle.setParameter("00001", "carFollowModel.SimpleCACC1", "Hi")


      
    #每隔20秒加入1车队   
    if timeT%20000==0:
        
        tmp3=str(int(curTime/20))
        platoonId1 = tmp3
        for i in range(TM.platoonSize):
            vehichID=TM.DPM.platoons[platoonId1][i] 
            veh = TM.vehDict[vehichID]
            veh.speed = 0
            libsumo.vehicle.addLegacy(vehichID,"r1",-3,veh.position,veh.speed,str(veh.lane),"car1")
            libsumo.vehicle.setLaneChangeMode(vehichID,0)
        
     

        
    libsumo.simulationStep()
    if timeT/1000 >300: #if time is over 200 second stoping the simulation
        requireStop = 1
    



    return TM,stepNum,requireStop

