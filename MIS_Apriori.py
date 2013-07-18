#MSApriori Algorithms
#Get the data from the input file


import csv
import pdb
import operator
import collections
import itertools
import os




class MSApriori:



    def __init__(self):
        self.MIS = collections.OrderedDict()
        self.CandSet = collections.OrderedDict() #C
        self.SupCount = collections.OrderedDict() #L
        self.FreqSet = collections.OrderedDict() #F
        self.Total = 0
        self.minSup = 0.02
        self.myInput = "./Data/LatestmyARFF2Week.txt"
        self.MISInput = "./Data/MIS_Input.txt"
        self.RESULT = "./Data/RESULT.txt"
        self.truaxisMerchant = "abercrombiefitch,aeropostale,allsaints,applebees,bodyshop,brooksbrothers,cache,californiapizzakitchen,cherrymoonfarms,chicos,clairesstoreinc,coldwatercreek,crispers,dermstore,donpablos,drugstorecom,dsw,dunhamssports,dunkindonuts,ebags,footlocker,ftd,golfsmith,guitarcenter,harryanddavid,kmart,kohls,landsend,lanebryant,macys,movieticketscom,off5th,oldnavy,oreillyauto,personalcreations,pizzahut,ponderosasteakhouse,proflowers,redrobin,redbox,redenvelope,reebok,sears,sharisberries,shoebuy,soapcom,thecheesecakefactory,thehomedepot,walgreens,warbyparker"
        self.truaxisMerchant = set(self.truaxisMerchant.split(","))
        
        
        ## if file exists, delete it ##
        #if os.path.isfile(self.RESULT):
        #     os.remove(self.RESULT)

        self.resultData = open(self.RESULT,'w+')


        self.inputData = csv.reader(open(self.myInput,"rb"))
        self.MISData = open(self.MISInput,"rb")

    def getMISData(self,MIS_file):
        #Convert the data into Structure format
        #To get the Sorted MIS values

        
        for line in MIS_file:
            line = line.strip()
            line = line.split(" ")
            self.MIS[line[0]] = float(line[1])
            #Sort the MIS
            self.MIS = collections.OrderedDict(sorted(self.MIS.items(), key=lambda t: t[1]))
        return self.MIS

    def initialPass(self):

        
        #SupCount is a OrderedDict, So we are sorting adding elements in this List by Sorted MIS
        #Intialize the SupCount
        #only call this function after getting MIS data

        
        for item in self.MIS:
            self.SupCount[item] = 0 #Intialize the support Count, Here assumption is that we have list of all the items in the MIS file

        totalItem = len(self.SupCount)
        
        print "Lenght of MIS: ",len(self.MIS.keys())

        self.inputData = csv.reader(open(self.myInput,"rb"))
        #Intial pass over the data
        for line in self.inputData:
            self.Total += 1 #Count the # of rows in the Transaction
            for item in line:
                #For this algorithm we have unique item for each row
                self.SupCount[item.strip()] += 1 #increment
        print "After Initial Pass items, SupCount size is: ", len(self.SupCount)



    
    def Level2CandidateGen(self):
        #input: SupCount, minSup
        
        #pdb.set_trace()
        
        iterComb = itertools.combinations(self.SupCount.keys(), 2)
        
        for comb in iterComb:
            #print comb
            #pdb.set_trace()
            item1,item2 = comb[0],comb[1]
            if(self.SupCount[item1] >= self.MIS[item1] and self.SupCount[item2] >= self.MIS[item1] and(self.SupCount[item2]-self.SupCount[item1]  <= self.minSup)):
                self.CandSet[comb] = 0
        print "After Level2, Total Candidate are: ",len(self.CandSet.keys())
        self.SupCount = None #Empty this
        return self.CandSet
  

    def CalFrequentItemSets(self):

        #input:Total,inputData, CandSet, MIS

        #output: FrequentSet

        #Here we will traverse each trasaction and will calculate the count for each pair
        #Intial pass over the data
        self.inputData = csv.reader(open(self.myInput,"rb"))
        count = 0
        
        for line in self.inputData:
            count += 1
            #pdb.set_trace()
            line = frozenset([item.strip() for item in line])

            for freqSet in self.CandSet:
                #if the canidate is existed in the transaction then
                if(frozenset(freqSet) <= line):
                   self.CandSet[freqSet] += 1
            #print count     
            if(count % 200 == 0):
                print "Processed ",count," records"
        
        print "-----------------"
        #Calculate percentage and remove items that don't satisfy the MIS 
        for freqSet in self.CandSet.keys():
            self.CandSet[freqSet] = float(self.CandSet[freqSet])/self.Total
            
            if(self.CandSet[freqSet] < self.MIS[freqSet[0]]): #freqSet[0] - First item in the Frequent set
                del self.CandSet[freqSet]
       
        return self.CandSet #it's a frequent itemset  (F)
        

    def MScandidateGen(self):
        #input:MIS
        #output: NewCandSet

        NewCandSet = collections.OrderedDict()
        #pdb.set_trace()
        iterComb = itertools.combinations(self.FreqSet.keys(), 2)

        for freqItem in iterComb:
            pair1, pair2 = freqItem[0], freqItem[1]
            if (pair1[0:len(pair1)-1] == pair2[0:len(pair2)-1] and (abs(self.MIS[pair1[-1]]- self.MIS[pair2[-1]]) <= self.minSup)):
                #pdb.set_trace()
                
                newPair = pair1 + (pair2[-1],)  #I assumed here that MIS value of last value of second pair is greter than last element of first pair
                NewCandSet[newPair] = 0

        self.FreqSet = None
        return NewCandSet



    def getMinMIS(self):

        # We will check if the support is less than the minimum MIS value

        for item,value in self.MIS.iteritems():
            MinMIS = value
            return MinMIS

    def calL1FrequentItems(self):    

        #Calculate the percentage of each Support Item
        for key in self.SupCount.keys():
            value = self.SupCount[key]
            self.SupCount[key] = float(value)/self.Total
            MinMIS = self.getMinMIS()
            if(self.SupCount[key] < MinMIS):
                del self.SupCount[key]
            """
            #Generate the F1 Set
            for key,value in self.SupCount.iteritems():

                if value >= self.MIS[key]:
                    self.FreqSet[key] =1
                    
            print "Len of F1: ",len(self.FreqSet)
            """


        print "Length of L1: ",len(self.SupCount.keys())

    def writeOutput(self,FreqSet):

        self.resultData.write("Frequent itemsets:"+"\n")
                              
        for pair in FreqSet:
            self.resultData.write(str(pair) + "\n")

    def filterCandidateSets(self,CandSet,truaxisMerchant):

        for freq in CandSet.keys():
            if not(len(set(freq) & truaxisMerchant) > 0):
                del CandSet[freq]

        print "Length after removing non-truaxis merchant seq",len(CandSet)

        return CandSet
                
            
    def run(self):

        MISData = self.getMISData(self.MISData)
        self.initialPass()
        
        self.calL1FrequentItems()
        
        K = 2
        #pdb.set_trace()
        while(1):
            
            #Calculate the Pairs
            if(K ==2):
                self.CandSet = self.Level2CandidateGen()
            else:
                self.CandSet = self.MScandidateGen()
            
            self.CandSet = self.filterCandidateSets(self.CandSet,self.truaxisMerchant)
            
            #Calculate the Frequent Itemsets in the pair
            self.FreqSet = self.CalFrequentItemSets()
            #pdb.set_trace()
            

            if(len(self.CandSet)  < 2):
                break
                              
            self.writeOutput(self.FreqSet)
            print "# of Frequent ItemsSet for Level: ",K,": ",len(self.FreqSet.keys())

            K += 1
            

if __name__ == "__main__":
    
    MSApriori = MSApriori()
    MSApriori.run()








