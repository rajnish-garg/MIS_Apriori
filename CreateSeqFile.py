import csv
import pdb
import collections

fileName = './Data/UserMerchantDateAmountJune1-15.csv'
NewFile = 'LatestmyARFF2Week.arff'
NewFileMerchName = 'LatestmyARFF2WeekMerchantName.txt'

def createMerchantCount():
    
    #Create a dictionary of User and Merchant
    myfile = csv.reader(open(fileName))

    MIS = {}
    Merchant = {}
    myfile.next()
    for line in myfile:

        if(MIS.get(line[0])) is None:
            MIS[line[0]] = []
        
        if(Merchant.get(line[1])) is None:
            Merchant[line[1]] = []
        
        
        #if(line[1] not in MIS[line[0]]):
        MIS[line[0]].append(line[1])
        #pdb.set_trace()

def createARFFFile():
    truaxisMerchant = "abercrombiefitch,aeropostale,allsaints,applebees,bodyshop,brooksbrothers,cache,californiapizzakitchen,cherrymoonfarms,chicos,clairesstoreinc,coldwatercreek,crispers,dermstore,donpablos,drugstorecom,dsw,dunhamssports,dunkindonuts,ebags,footlocker,ftd,golfsmith,guitarcenter,harryanddavid,kmart,kohls,landsend,lanebryant,macys,movieticketscom,off5th,oldnavy,oreillyauto,personalcreations,pizzahut,ponderosasteakhouse,proflowers,redrobin,redbox,redenvelope,reebok,sears,sharisberries,shoebuy,soapcom,thecheesecakefactory,thehomedepot,walgreens,warbyparker"

    TruAxisMerList = set(truaxisMerchant.split(","))
    
    #Create a dictionary of User and Merchant
    myfile = csv.reader(open(fileName))
    #myfile.close()
    MIS = {}
    Merchant = {}
    myfile.next()
    for line in myfile:

        if(MIS.get(line[0])) is None:
            MIS[line[0]] = []
        
        if(Merchant.get(line[1])) is None:
            Merchant[line[1]] = []
        
        
        #if(line[1] not in MIS[line[0]]):
        MIS[line[0]].append(line[1])
        #pdb.set_trace()
    
    
    MISUser = MIS.keys()
    MerchantList = Merchant.keys()

    
    # New file name to save   
    myARFF = open(NewFile,'w+')
    myARFFMerchant = open(NewFileMerchName, 'w+')
    
    myARFF.write('@relation TRUAXIS\n\n\n')

    icount = -1
    for line in MerchantList:
        icount += 1
        line.strip().replace("'","")
        MerchantList[icount] = line



    #sort the merchant data
    MerchantList.sort()

    for line in MerchantList:    
        myARFF.write(str("@attribute "+line+" {false,true}\n"))

    myARFF.write('\n\n@data\n\n')
    #{0 true,3 true,6 true,7 true,8 true,9 true,12 4,15 true}
    #pdb .set_trace()
    for key in MIS:
        #pdb.set_trace()
        line = list(set(MIS[key]))
        
        newLine = "{ "
        if(len(line) <6):
            continue
        
      
        if(len(list(set(line)-(set(line)-TruAxisMerList))) == 0):
            continue
        
        
        #Clean the data
        for i, word in enumerate(line):
            line[i] = (word.strip()).replace("'","")

        line.sort()
            
        for word in line:        
            iIndex = MerchantList.index(word)
            newLine += str(str(iIndex)+" "+"true"+",")

        writeLine = newLine[:-1]
        writeLine += "}\n"
        myARFF.write(writeLine)
        myARFFMerchant.write(str(str(line)+ '\n'))
        #pdb.set_trace()
                        
def createMSAprioriFormatFile():
    truaxisMerchant = "abercrombiefitch,aeropostale,allsaints,applebees,bodyshop,brooksbrothers,cache,californiapizzakitchen,cherrymoonfarms,chicos,clairesstoreinc,coldwatercreek,crispers,dermstore,donpablos,drugstorecom,dsw,dunhamssports,dunkindonuts,ebags,footlocker,ftd,golfsmith,guitarcenter,harryanddavid,kmart,kohls,landsend,lanebryant,macys,movieticketscom,off5th,oldnavy,oreillyauto,personalcreations,pizzahut,ponderosasteakhouse,proflowers,redrobin,redbox,redenvelope,reebok,sears,sharisberries,shoebuy,soapcom,thecheesecakefactory,thehomedepot,walgreens,warbyparker"

    TruAxisMerList = set(truaxisMerchant.split(","))
    MerchantFile = open("MSAprioriMerchantList.txt","wb")

    
    
    #Create a dictionary of User and Merchant
    myfile = csv.reader(open(fileName))
    #myfile.close()
    MIS = {}
    Merchant = {}
    myfile.next()
    for line in myfile:

        line[0] = line[0].strip()
        if(MIS.get(line[0])) is None:
            MIS[line[0]] = []

        line[1] = line[1].strip()
        if(Merchant.get(line[1])) is None:
            Merchant[line[1]] = []
        
        
        #if(line[1] not in MIS[line[0]]):
        MIS[line[0]].append(line[1])
        #pdb.set_trace()
    
    
    MISUser = MIS.keys()
    MerchantList = Merchant.keys()

    
    # New file name to save   
    myARFF = open(NewFile,'w+')
    
    #sort the merchant data
    MerchantList.sort()

    
    for line in MerchantList:    
        MerchantFile.write((line+ "\n"))

  
    for key in MIS:
        #pdb.set_trace()
        line = set(MIS[key])
        
        if(len(line) <8):
            continue
        
      
        if len(line & TruAxisMerList) == 0:
            continue
        
        line = list(line)
        
        #Clean the data
        for i, word in enumerate(line):
            line[i] = (word.strip()).replace("'","")

        line.sort()

        newLine = "" 
        for word in line:
            
            newLine += word+ ','

        writeLine = newLine[:-1]
        myARFF.write((writeLine + "\n"))
        #pdb.set_trace()

createMSAprioriFormatFile()                   
#createARFFFile()
