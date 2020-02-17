class RingTrafficManager:
    
    platoonSize =0
    nPlatoons =0
    injectedCars = 0
    injectedPlatoons = 0

    # number of lanes
    nLanes =0
    # insert distance
    platoonInsertDistance=0
    # insert headway
    platoonInsertHeadway=0
    # headway for leader vehicles
    platoonLeaderHeadway=0
   # sumo vehicle type of platooning cars
    platooningVType = 0
    platoonInsertSpeed = 0;
    vehTypeId = 0;

    lengths ={}
    platoons={}
    vehQue = [];
    DPM =[];
    def __init__(self):
        self.platoonSize =8
        self.nPlatoons =8
        self.injectedCars = 0
        self.injectedPlatoons  = 0
        self.nLanes =  1
        self.platoonInsertDistance=  1
        self.platoonInsertHeadway =  1
        self.platoonLeaderHeadway =  10
        self.platooningVType = 0
        self.platoonInsertSpeed = 40/3.6
        self.DPM =DynamicPositionManager();

    def scenarioLoaded(self):
    

        for l in range(self.nLanes):
            self.lengths[l] = 0
            self.platoons[l] = []

        l = 0
        for  p in range(self.nPlatoons):
            platoon = Platoon()
            platoon.size = self.platoonSize
            platoon.speed =self.platoonInsertSpeed
            platoon.distanceToFront =self.platoonLeaderHeadway * platoon.speed
        # compute the length of the platoon. assume a hardcoded vehicle length value of 
            platoon.length = platoon.size * 4 + (platoon.size - 1) * (self.platoonInsertDistance + self.platoonInsertHeadway * platoon.speed);
        # add the length of this platoon to the platoons of this lane
            self.lengths[l] = self.lengths[l]+ platoon.length + platoon.distanceToFront;
            self.platoons[l].append(platoon)
            l = (l+1 )% self.nLanes

        for l in range(self.nLanes):

            totalLength = self.lengths[l]
            ps = self.platoons[l]
            for p in range(len(ps)):
                
                totalLength -= self.platoonLeaderHeadway * ps[p].speed;
                for v in range(len(ps)):
                    veh = Vehicle()
                    veh.speed = ps[p].speed
                    veh.position = totalLength;
                    veh.lane = 0;
                    veh.id = str(self.injectedCars);
                    self.vehQue.append(veh);
                    self.DPM.addVehicleToPlatoon(str(self.injectedCars), v, str(self.injectedPlatoons))
                    self.injectedCars+=1

                    if v < ps[p].size-1:
                       totalLength -= (4 + self.platoonInsertDistance + self.platoonInsertHeadway * veh.speed);
                    else:
                       totalLength -= 4
                self.injectedPlatoons+=1
  
        
class PlatoonTrafficManager:
    
    platoonSize =0
    nPlatoons =0
    injectedCars = 0
    injectedPlatoons = 0

    # number of lanes
    nLanes =0
    # insert distance
    platoonInsertDistance=0
    # insert headway
    platoonInsertHeadway=0
    # headway for leader vehicles
    platoonLeaderHeadway=0
   # sumo vehicle type of platooning cars
    platooningVType = 0
    platoonInsertSpeed = 0;
    vehTypeId = 0;

    lengths ={}
    platoons={}
    vehQue = [];
    vehDict ={};
    DPM =[];
    isSplit =0;
    isSC = 0  # perform CACC 2 ACC
    def __init__(self):
        self.platoonSize =10
        self.nPlatoons =80
        self.injectedCars = 0
        self.injectedPlatoons  = 0
        self.nLanes =  2
        self.platoonInsertDistance=  1
        self.platoonInsertHeadway =  1
        self.platoonLeaderHeadway =  3
        self.platooningVType = 0
        self.platoonInsertSpeed = 40/3.6
        self.DPM =DynamicPositionManager();
        self.isSplit =0;
        self.isSC =0;
    def scenarioLoaded(self):
       #将所有车队安排到lane0
       #将所有车队随机安排到lane0或者lane1
    
       
        self.lengths = 0
        self.platoons = []
        
        for  p in range(self.nPlatoons):
            platoon = Platoon()
            platoon.size = self.platoonSize
            platoon.speed =self.platoonInsertSpeed
            platoon.distanceToFront =self.platoonLeaderHeadway * platoon.speed
        # compute the length of the platoon. assume a hardcoded vehicle length value of 
            platoon.length = platoon.size * 4 + (platoon.size - 1) * (self.platoonInsertDistance + self.platoonInsertHeadway * platoon.speed);
        # add the length of this platoon to the platoons of this lane
            self.platoons.append(platoon)
            

    

       
        ps = self.platoons
        for p in range(len(ps)):
                
            totalLength = ps[p].length
            for v in range( self.platoonSize):
                veh = Vehicle()
                veh.speed = ps[p].speed
                veh.position = totalLength;
                veh.lane = self.injectedPlatoons%2;
                veh.id = str(self.injectedCars);
                self.vehQue.append(veh);
                self.vehDict[veh.id] =veh;
                self.DPM.addVehicleToPlatoon(str(self.injectedCars), v, str(self.injectedPlatoons))
                self.injectedCars+=1

                if v < ps[p].size-1:
                    totalLength -= (4 + self.platoonInsertDistance + self.platoonInsertHeadway * veh.speed);
                else:
                    totalLength -= 4
            self.injectedPlatoons+=1
        



class Platoon:
      size =0
      speed=0
      length=0
      distanceToFront=0
      def __init__(self):
        self.size  =8
        self.speed =40
        self.length = 0.1
        self.distanceToFront = 0

class Vehicle:
      id =0
      speed=0
      length=0
      position = 0
      lane = 0
      def __init__(self):
        self.id  =0
        self.speed =40/3.6
        self.length = 4
        self.lane = 0
        self.position = 0

class DynamicPositionManager:

    #// map from position within the platoon to vehicle id
    platoon ={};
    #// map from platoon id to platoon structure
    platoons ={};
    # // map from vehicle id to own platoon id
    vehToPlatoons ={};
    #// map from position to vehicle id.有问题，应该是from vehicle id to position
    position ={};

    #// map from platoon id to platoon structure
    platoons ={}
    #// map from platoon id to positions
    positions ={}

    maxPlatoonNum = 10000
    maxPlatoonSize = 20

    def __init__(self):

        #// map from platoon id to vehInPlatoon_Pos->vehicle_id structure,then from  position within the platoon to vehicle id
        for i in range(self.maxPlatoonNum):
            self.platoons[str(i)] ={}
        #// map from platoon id to vehicle-positions,from vehicle id to position
        for i in range(self.maxPlatoonNum):
            self.positions[str(i)] ={}

   

    def addVehicleToPlatoon(self,vehicleId1, position1, platoonId1):
        self.platoons[platoonId1][position1] = vehicleId1
        self.positions[platoonId1][vehicleId1] = position1
        self.vehToPlatoons[vehicleId1] = platoonId1

    def removeVehicleFromPlatoon(self,vehicleId):

        platoonId= self.vehToPlatoons[vehicleId]
        pos = self.positions[platoonId][vehicleId];

        self.positions[platoonId].pop(vehicleId)
        self.platoons[platoonId].pop(pos)
        self.vehToPlatoons.pop(vehicleId)
        

    def splittPlatoon(self,abnormalVehicleID):

        platoonID = self.vehToPlatoons[abnormalVehicleID];
        vehList = self.platoons[platoonID];
        pos = self.positions[platoonID][abnormalVehicleID];
        platoonID2 = str(int(self.maxPlatoonNum/2+int(platoonID)));

        for i in range(pos+1,len(vehList)):
           
           vehT = self.platoons[platoonID][i];
           self.positions[platoonID].pop(vehT)
           self.platoons[platoonID].pop(i)
           self.vehToPlatoons.pop(vehT)

           iT = i-pos-1
           self.platoons[platoonID2][iT] = vehT
           self.positions[platoonID2][iT] = vehT
           self.vehToPlatoons[vehT] = platoonID2
           