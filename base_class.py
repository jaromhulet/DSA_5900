import pandas as pd
from sklearn.preprocessing import StandardScaler
from itertools import combinations
import math
from matplotlib import pyplot as plt
import numpy as np
from numpy import percentile


class baseHeuristic:
    def __init__(self,df):
        
        #df = input dataframe ==> first column must be text identifier, the rest must be numeric
        #distCalc = Type of distance calculation to be used ==> 'euc' = Euclidean, 'man' = Manhattan, 'cos' = cosine
        #aggrMethod = list as long as the columns of df-1, that dictates what kind of aggregation should be done
        #             on a group level ==> 'sum' = add columns by group, 'avg' = get average of columns by group
        
        
        #user input parameters
        self.df = df

        #method created parameters
        self.stdDf = None
        self.aggrDf = None

        #simple calculated parameters
        self.df_len = len(df)
        self.col_ct = len(df.columns)
        self.col_types = self.df.dtypes

        #data validation for df input (dataframe check)
        if isinstance(self.df, pd.DataFrame) == False:
            raise Exception("Input Error: Parameter df must be a pandas dataframe")

        #data validation for df input (check that first column is char and all others are numeric)

        #data validation for distCalc input
        #if self.distCalc not in ['euc','man','cos']:
            #raise Exception("Input Error: Parameter distCalc must be 'euc','man', or 'cos'.")
    
    
        #create a standardized data set when the instance is created
        temp_df = self.df.iloc[:,1:self.col_ct]
        scaler = StandardScaler()
        scaler = scaler.fit_transform(temp_df)
        temp_df = pd.DataFrame(scaler)
        
        #combine standardized data back to label column
        self.stdDf = pd.concat([self.df.iloc[:,0],temp_df],axis=1)
        
        
        #method to create starting solution
    def startSol(self,randStart='Y',startMetric=1,seed=1920):
        
        #conditionally create a random or deterministic starting solution
        if randStart == 'Y':
            
            #set random seed
            #random.seed(seed)
            
            #create label list to hold all lables 
            label_list = list(self.df.iloc[:,0])
            
            #instantiate grouping list
            grouping = []

            #initiate first element in each group
            for i in range(0,self.numGroups):
                rand_num = random.randint(0,len(label_list)-1)
                grouping.append([label_list[rand_num]])
                label_list.pop(rand_num)
                
            #loop through each group and add a random element to it until no more elements are left
            while len(label_list) > 1:
                for j in range(0,self.numGroups):
                    #exit loop if label_list becomes too short to avoid out of range errors generated by rand_num
                    if len(label_list) == 1:
                        break
                    rand_num = random.randint(0,len(label_list)-1)
                    grouping[j].append(label_list[rand_num])
                    label_list.pop(rand_num)
                    temp_j = j
            
            #put the last remaining value to the grouping
            grouping[temp_j + 1].append(label_list[0])
                    
                             
        #if not a random starting place, 
        elif randStart == 'N':
            #sort dataframe by startMetric column
            sorted_df = self.df.sort_values(self.startMetric)

            #convert label column in df to list to access .pop() method
            label_list = list(sorted_df.iloc[:,0])
            
            
            #put each element recursively in a group
            grouping = []
            #manually do first iteration to instantiate the appropriate sized list
            for h in range(0,self.numGroups):
                grouping.append([label_list[h]])
            
            #remove elements that were added to grouping in the previous loop
            label_list = label_list[self.numGroups:len(label_list)]

                
            #now that the grouping list is instantiated w/ approprate dimensions, put the rest of the elements into groups
            switch_dir = 1
            
            while len(label_list) > 0:
                if switch_dir == 0:
                
                    #create a varable for looping based on length of lable_list and self.numGroups
                    if len(label_list) < self.numGroups:
                        loop_count = len(label_list)
                    else:
                        loop_count = self.numGroups
                    
                    
                    for i in range(0,loop_count):
                        
                        grouping[i].append(label_list[i])
                        
                    #remove all elements that were just added to the grouping list
                    label_list = label_list[loop_count:len(label_list)]
                            
                    #set switch_dir to 1, so it will loop the opposite direction next while iteration
                    switch_dir = 1
                    print(grouping)
                    
                elif switch_dir == 1:

                    
                    for j in range(self.numGroups-1,-1,-1):
                        print(j)
                        
                        #exit loops if label_list is empty
                        if len(label_list) == 0:
                            break
                            
                        grouping[j].append(label_list[0])
                        label_list.pop(0)
                    
                    
                    #set switch_dir to 0, so it will loop the opposite direction next while iteration
                    switch_dir = 0
                    print(grouping)
        return grouping
    
    
    #standardize elements in df
    def standardize(self):
        
        temp_df = self.df.iloc[:,1:self.col_ct]
        scaler = StandardScaler()
        scaler = scaler.fit_transform(temp_df)
        temp_df = pd.DataFrame(scaler)
        
        #combine standardized data back to label column
        self.stdDf = pd.concat([self.df.iloc[:,0],temp_df],axis=1)
        
        return self.stdDf
            
        
    #calculate distance between just two records
    def pairDist(self,a,b,distCalc,):
        
        #convert pandas series to list
        if isinstance(a,pd.core.series.Series) == True:
            a = a.tolist()
        if isinstance(b,pd.core.series.Series) == True:
            b = b.tolist()
        
        #set up variables for the execution of the calculation
        list_len = len(a)
        dist_sum = 0
        temp_dist = 0
        
        #calculate distance based on user self.distCalc (exclude first element in list)
        #Euclidean distance
        if distCalc == 'euc':
            
            for i in range(1,list_len):
                
                temp_dist = (a[i]-b[i])**2
                dist_sum = dist_sum + temp_dist
                
            euc_dist = math.sqrt(dist_sum)
            return euc_dist
                
        #manhattan distance    
        elif distCalc == 'man':
            
            for i in range(1,list_len):
                temp_dist = abs(a[i]-b[i])
                dist_sum = dist_sum + temp_dist
            
            man_dist = dist_sum
            
            return man_dist
        
        #cosine distance
        elif distCalc == 'cos':
            
            #convert to np array
            a = np.asarray(a[:][1:])
            b = np.asarray(b[:][1:])
            
            #calculate dot product
            dot_prod = np.dot(a,b)
            
            #calculate magnitudes
            a_mag = np.linalg.norm(a)
            b_mag = np.linalg.norm(b)
            
            #calculate cosine distance
            cos_dist = dot_prod/(a_mag*b_mag)
            
            return cos_dist
    
    #calculate aggregated metrics by input groups
    def groupMetrics(self,groups,aggMethod):
        #Instantiate master list to hold aggregated metrics by group
        master_list = []
        
        #iterate through all groups -- groups will come from the hueristic portion of the programming
        for i in range(0,len(groups)):
            temp_group = groups[i]
            temp_df = self.stdDf[self.stdDf.iloc[:,0].isin(temp_group)]

            #start temp_list with group number
            temp_list = [i]
            #iterate through columns at a group level
            for j in range(0,(len(self.stdDf.columns)-1)):

                #if user input list of aggregation types is 'sum', then execute
                if aggMethod == 'sum':
                    #calculate column sum
                    temp_aggr = temp_df.iloc[:,j+1].sum()
                    #append summed value to list
                    temp_list.append(temp_aggr)

                #if user input list of aggregation types is 'avg', then execute
                elif aggMethod == 'avg':
                    #calculate column mean
                    temp_aggr = temp_df.iloc[:,j+1].mean()
                    #append mean value to list
                    temp_list.append(temp_aggr)
                #put temp_list in master_list once all columns for the group have been aggregated
            master_list.append(temp_list)

            #convert master list into dataframe
            master_df = pd.DataFrame(master_list)
            
            #set self.aggrDf attribute equal to the aggregated group dataframe
            self.aggrDf = master_df
            
        return master_df

    #add up all of the pairwise distances using pairDist method
    def totalDist(self,groups,dist):
        
        row_num = len(groups)
        combins = list(combinations(list(range(0,row_num)),2))

        #instantiac variable to hold total distance
        total_dist = 0
        
        for i in range(0,len(combins)):

            temp_dist_df = groups[groups.iloc[:,0].isin(combins[i])]
            
            #Get pairwise distance between two groups at a time, using self.pairDist
            temp_dist = self.pairDist(groups.iloc[0,:],groups.iloc[1,:],dist)
            
            #add to total_dist
            total_dist = total_dist + temp_dist
        
        return total_dist
    
    
    #create a function to make a histogram of random position values
    def sample_hist(self,sample_size,aggMethod,distMetric):
        
        sample_dists = []
        
        for i in range(0,sample_size):
            temp_solution = self.startSol()
            
            temp_dist = self.totalDist(self.groupMetrics(temp_solution,aggMethod),distMetric)
        
            sample_dists.append(temp_dist)
            
        plt.hist(sample_dists,bins=30)
        
        
        
        #convert to numpy array
        sample_dists_np = np.array(sample_dists)
        
        quartiles = percentile(sample_dists_np, [25,50,75])
        data_min, data_max = sample_dists_np.min(), sample_dists_np.max()
        
        five_num_summary = [data_min,quartiles[0],quartiles[1],quartiles[2],data_max]
        
        print(five_num_summary)
        
        plt.show()
        
        return five_num_summary