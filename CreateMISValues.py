import pdb
import csv

#Find the Minimum Item Support From the Data by given Lambda

Lambda = 0.8 #It should be b/w 0<Lambda<1
FileName = './Data/LatestmyARFF2Week.txt'
MISFile = './Data/MIS_Input.txt'
MerchantList = './Data/MSAprioriMerchantList.txt'
truaxisMerchant = "abercrombiefitch,aeropostale,allsaints,applebees,bodyshop,brooksbrothers,cache,californiapizzakitchen,cherrymoonfarms,chicos,clairesstoreinc,coldwatercreek,crispers,dermstore,donpablos,drugstorecom,dsw,dunhamssports,dunkindonuts,ebags,footlocker,ftd,golfsmith,guitarcenter,harryanddavid,kmart,kohls,landsend,lanebryant,macys,movieticketscom,off5th,oldnavy,oreillyauto,personalcreations,pizzahut,ponderosasteakhouse,proflowers,redrobin,redbox,redenvelope,reebok,sears,sharisberries,shoebuy,soapcom,thecheesecakefactory,thehomedepot,walgreens,warbyparker"


truaxisMerchant = truaxisMerchant.split(",")
#Global Variable
ItemSupport = {}
Total = 0
#Open the file
myFile = csv.reader(open(FileName,'rb')) #Input file
misFile = open(MISFile,'w+')#output file
truaxisMerchantList = open(MerchantList,"rb")

MerchantList = []
for item in truaxisMerchantList:
    MerchantList.append(item)


#Calcualte Support/Frequency for each item
for line in myFile:

    Total += 1 #To count Total number of lines
    for item in line:
        #pdb.set_trace()
        item = item.strip()
        item = item.replace("'","")
        #For each item add it into dictionary count it
        if(ItemSupport.has_key(item)):
            ItemSupport[item] += 1
        else:
            ItemSupport[item] = 1


"""
Assign a MIS value to each item according to its actual support/
frequency in the data set T. For example, if the actual support of
item i in T is sup(i), then the MIS value for i may be computed with
sup(i)
"""
#frequency = Support/ Total
for key in ItemSupport:
    #pdb.set_trace()
    ItemSupport[key] = (float(ItemSupport[key])/ Total) *  Lambda
	
    misFile.write(str(key)+ " "+ str(ItemSupport[key]) + '\n')
	
		
    """
    if((MerchantList[int(key)].strip()) in truaxisMerchant):
        misFile.write(str(key)+ " "+ str(ItemSupport[key]) + '\n')
    else:
        misFile.write(str(key)+ " "+ str("1.1") + '\n')
    """
	
#close the file connections
misFile.close()
    

