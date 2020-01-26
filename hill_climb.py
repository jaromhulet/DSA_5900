import nbr_hood as nbr
import random
import pandas as pd
import numpy as np

#create class for hill climb algorithms
class hillClimb(nbr.nbrHood):
    
    def __init__(self,df,numGroups,nbrhoodsize):
        
        super().__init__(df,numGroups)
        self.nbrhoodsize = nbrhoodsize
        
    
    def runHillClimb(self,selectMethod,restarts,aggMethod,distMetric,startMetric=1,randStart='Y',seed=1920,power=1):
        #start random seed
        
        #random.seed(seed)
        obs = 0
        
        #create a starting solution
        startSolution = self.startSol(randStart=randStart,startMetric=startMetric)
        
        #conditionally execute hill climb with best accept
        if selectMethod == 'BEST ACCEPT':
        
            globalBestNbr = startSolution
            globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
            
            for j in range(0,restarts):
                
            
                currentSolution = startSolution
            
                done = 0
            
                while done == 0:
                    
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    
                    for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                        obs = obs + 1
                        if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                            bestNbr = i
                            bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                            print(bestDist)
                            
                    if currentSolution == bestNbr:
                        done = 1
                    else:
                        currentSolution = bestNbr 
                        
                        
                print("restart")
                
                if bestDist < globalBestDist:
                    globalBestNbr = bestNbr
                    globalBestDist = self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                    print("New Global Best = %s" % globalBestDist)
                    
                    
            #put the globals back into the locals so the return statement returns the global bests
            #bestNbr = globalBestNbr
            #bestDist = globalBestDist
            
            print("done")        
        

        
        #implement first accept method
        elif selectMethod == 'HILL CLIMB':
            
            currentSolution = startSolution
            
            done = 0
            
            while done == 0:
                
                bestNbr = currentSolution
                bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                
                for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                    obs = obs + 1
                    if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                        bestNbr = i
                        bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                        print(bestDist)
                        
                if currentSolution == bestNbr:
                    done = 1
                else:
                    currentSolution = bestNbr
                    
        
        
        elif selectMethod == 'FIRST ACCEPT':
            
            globalBestNbr = startSolution
            globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
            
            for j in range(0,restarts):
                
            
                currentSolution = startSolution
            
                done = 0
            
                while done == 0:
                    
                    bestNbr = currentSolution
                    
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    

                    for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                        
                        obs = obs + 1
                        if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                            bestNbr = i
                            bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                            print(bestDist)
                            #add break to make it first accept
                            break
                            
                    if currentSolution == bestNbr:
                        done = 1
                    else:
                        currentSolution = bestNbr 
                        
                        
                print("restart")
                
                if bestDist < globalBestDist:
                    globalBestNbr = bestNbr
                    globalBestDist = self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                    print("New Global Best = %s" % globalBestDist)
                    
                    
            #put the globals back into the locals so the return statement returns the global bests
            #bestNbr = globalBestNbr
            #bestDist = globalBestDist
            
            print("done")
            
        #conditionally execute random walk with best accept
        
        #I haven't actually coded the random walk yet.  Below is just Best Accept.
        #make necessary changes to make below code random walk.
        if selectMethod == 'RANDOM WALK':
            
            #create method to find random walked solution
            def rand_find(prob_list,rand_num):
                
                pos = -1
                
                for i in prob_list:
                    pos = pos + 1
                    if i > rand_num:
                        return pos            
        
            globalBestNbr = startSolution
            globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
            
            for j in range(0,restarts):
                
            
                currentSolution = startSolution
            
                done = 0
            
                while done == 0:
                    
                    temp_nbr_df = pd.DataFrame(columns=['nbr','dist'])
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    
                    #make a list of nbr distances
                    for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                        obs = obs + 1
                        
                        temp_nbr_df = temp_nbr_df.append({'nbr':i,'dist':self.totalDist(self.groupMetrics(i,aggMethod),distMetric)},ignore_index=True)
                    
                    #if none of the new neighbors are better than current solution, stop
                    dists = temp_nbr_df['dist']
                    if min(dists) > bestDist:
                        done = 1
                        break
                
                    temp_nbr_df = temp_nbr_df.sort_values(by='dist')
                    
                    temp_array = temp_nbr_df['dist'].values
                    
                    temp_array = np.power(temp_array,power)
                    
                    #flip array so lowest values have highest probability of selection
                    temp_array = np.flip(temp_array)
                    
                    temp_array_sum = np.sum(temp_array)
                    
                    temp_array = temp_array/temp_array_sum
                    
                    #create cumulative array to go into rand_find function
                    temp_array_cum = np.cumsum(temp_array)
                    
                    #find index of randomly selected nbr
                    index_num = rand_find(temp_array_cum,random.uniform(0,1))
                    
                    
                    bestNbr = temp_nbr_df['nbr'][index_num]
                    
                    
                      
                    currentSolution = bestNbr 
                    
                    print(self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric))
                        
                        
                print("restart")
                
                if bestDist < globalBestDist:
                    globalBestNbr = bestNbr
                    globalBestDist = self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                    print("New Global Best = %s" % globalBestDist)
                    
                    
            #put the globals back into the locals so the return statement returns the global bests
            #bestNbr = globalBestNbr
            #bestDist = globalBestDist
            
            print("done")  
                    
                
        obs_statement = ("%s Solutions Examined" % obs)
    
        #return solution metric and solution
        return [self.groupMetrics(globalBestNbr,aggMethod),globalBestNbr,globalBestDist,obs_statement]
    
    #when a new global minimum is found, expand search to 2 swap, maybe even 3 swap?
    def runVNS(self,VNS_type,restarts,aggMethod,distMetric,startMetric=1,randStart='Y',expandFactor=2,nSwaps=2):
        
        #VNS_type has 3 options -- EXPAND, 2SWAP, 3SWAP. EXPAND increases nbrhood size by a specified factor when a minimum is found,
                                   #2SWAP changes nbrhood to 2 swap when min is found
                                   #3SWAP changes nbrhood to 3 swap when min is found
        
        obs = 0
        
        startSolution = self.startSol(randStart=randStart,startMetric=startMetric)
        
        #conditionally execute hill climb with EXPAND
        if VNS_type == 'EXPAND':
        
            globalBestNbr = startSolution
            globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
            
            for j in range(0,restarts):
                
            
                currentSolution = startSolution
            
                done = 0
            
                while done == 0:
                    
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    
                    for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                        obs = obs + 1
                        if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                            bestNbr = i
                            bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                            print(bestDist)
                            
                    if currentSolution == bestNbr:
                        done = 1
                    else:
                        currentSolution = bestNbr 
                        
                        
                print("restart")
                
                if bestDist < globalBestDist:
                    globalBestNbr = bestNbr
                    globalBestDist = self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                    print("New Global Best = %s" % globalBestDist)
                    print("Start Expanded Search")
                    
                    best_nbr = 0
                
                    while best_nbr == 0:
                        
                        bestNbr = currentSolution
                        bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                        
                        for i in self.createNbrhood(currentSolution,int(round(self.nbrhoodsize*expandFactor,0))):
                            obs = obs + 1
                            if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                                bestNbr = i
                                bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                                
                                
                                
                        if currentSolution == bestNbr:
                            best_nbr = 1
                            globalBestNbr = bestNbr
                            print("Global Best = %s" % globalBestDist)                            
                        else:
                            currentSolution = bestNbr       
                    print("End expanded search")
                
                obs_statement = ("%s Solutions Examined" % obs)
                print("done")                       
                    
                    
            
        #conditionally execute hill climb with EXPAND
        elif VNS_type == 'NSWAP':
            
            globalBestNbr = startSolution
            globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
                
            for j in range(0,restarts):
                    
                
                currentSolution = startSolution
                
                done = 0
                
                while done == 0:
                        
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                        
                    for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                        obs = obs + 1
                        if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                            bestNbr = i
                            bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                            print(bestDist)
                                
                    if currentSolution == bestNbr:
                        done = 1
                    else:
                        currentSolution = bestNbr 
                            
                            
                print("restart")
                    
                if bestDist < globalBestDist:
                    globalBestNbr = bestNbr
                    globalBestDist = self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                    print("New Global Best = %s" % globalBestDist)
                    print("Start %s Swap Search" % nSwaps)
                        
                    best_nbr = 0
                    
                    while best_nbr == 0:
                            
                        bestNbr = currentSolution
                        bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                            
                        for i in self.createNbrhood(currentSolution,self.nbrhoodsize,numSwaps=nSwaps):
                            obs = obs + 1
                            if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                                bestNbr = i
                                bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                                    
                                    
                                    
                        if currentSolution == bestNbr:
                            best_nbr = 1
                            globalBestNbr = bestNbr
                            print("Global Best = %s" % globalBestDist)                            
                        else:
                            currentSolution = bestNbr       
                    print("End expanded search")
                        
                        
                    
            obs_statement = ("%s Solutions Examined" % obs)
            print("done")              
            
        #return solution metric and solution
        return [self.groupMetrics(globalBestNbr,aggMethod),globalBestNbr,globalBestDist,obs_statement]            
        
        
        
        
        
        
        
        