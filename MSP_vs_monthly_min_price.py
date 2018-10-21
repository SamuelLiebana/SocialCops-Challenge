#Note - run cells in the below order (and do not re-run them individually)
#     - place csv files in the same folder as the jupyter notebook  

import csv #importing required libraries
from collections import defaultdict
import matplotlib.pyplot as plt




with open('deseasonalised_data.csv', newline='') as csvfile: #import monthly deseasonalised data as nested dictionary
    
    APMC = csv.reader(csvfile)
    
    #will only work with raw and trend data, hence we only initialise these two dictionaries
    APMC_raw_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))))))
    
    APMC_trend_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))))))
    
    APMC_district_name_product = set()

    
    i=0
    for row in APMC:
        if i > 0: #do not import first row (they are the names of the columns)
         
            #populate the dictionaries with the appropriate data from the csv files
            
            APMC_district_name_product.add((row[20].lower(),row[0].lower(),row[1].lower()))
            
            #I will only look at the min_price data as this is the most important to compare with the MSP
            
            APMC_raw_data[row[21].lower()][row[20].lower()][row[0].lower()][row[1].lower()][int(row[2])][int(row[3])] = int(row[8])
            
            APMC_trend_data[row[21].lower()][row[20].lower()][row[0].lower()][row[1].lower()][int(row[2])][int(row[3])] = int(float(row[9]))
            
                
        i+=1

#import the minimum support price values 

with open('CMO_MSP_Mandi.csv', newline='') as csvfile:
   
    CMO_MSP = csv.reader(csvfile)
    
    msprice = defaultdict(lambda: defaultdict(lambda: defaultdict(int))) #importing minimum support price data as nested dictionary
    
    MSP_product_year = set() #set containing the commodity, year couples for which we have MSP information
    
    i=0
    for row in CMO_MSP:
        if i > 0: #do not import first row (they are the names of the columns)
            
            
            try:
                a= int(row[3])
            
            except: #assign 0 to missing values
                a=0
            
            msprice[row[0].lower()][int(row[1])] = a
            
            MSP_product_year.add((row[0].lower(),int(row[1])))
                
        i+=1


#To compare the MSP to the monthly data I will compute the mean difference between the MSP and the minimum price for each year 
#for each commodity. In this way the government of Maharashtra can see where they need to intervene to help farmers with their costs.

#initialising average difference dictionaries for the raw and deseasonalised data for min_price
APMC_average_difference_raw = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))))
APMC_average_difference_trend = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))))


#iterate over commodities and years and compute the monthly average of the min_price data (raw and trend) for each year
#subsequently subtract the MSP for that year and commodity to get the average difference

for dist_name_prod in APMC_district_name_product:
    
    years = list(APMC_raw_data['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]].keys())
    
    for year in sorted(years):
        
        #only compute the average difference if we have a value for the MSP of that commodity
        
        if msprice[dist_name_prod[2]][year] !=0 and (dist_name_prod[2], year) in MSP_product_year:
            
            
            
            months = list(APMC_raw_data['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]][year].keys())
            
            var_raw = 0
            
            var_trend = 0
            
            for month in sorted(months):
                
                #accumulate monthly figures to compute the yearly mean of min_price raw and trend
                var_raw += APMC_raw_data['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]][year][month]
                var_trend += APMC_trend_data['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]][year][month]
                
            #compute the mean difference
            APMC_average_difference_raw['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]][year] = var_raw/len(months) - msprice[dist_name_prod[2]][year]
            APMC_average_difference_trend['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]][year] = var_trend/len(months) - msprice[dist_name_prod[2]][year]
            
            
        #if we don't have a value for the MSP of that commodity then label the average difference as invalid with the string 'NO MSP'
        else:
            
            APMC_average_difference_raw['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]][year] = 'NO MSP'
            APMC_average_difference_trend['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]][year] = 'NO MSP'
            

#write the mean differences to a new csv file named 'msp_comparison.csv' 
with open('msp_comparison.csv', mode='w', newline='') as clean_data:
    
    clean_data_writer = csv.writer(clean_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
    
    #first row contains the titles of the columns
    clean_data_writer.writerow(['APMC', 'Commodity','year','Average Difference Raw','Average Difference Deseasonalised','district_name', 'state_name'])
    
    #iterate over commodities and years
    for dist_name_prod in APMC_district_name_product:
        
        years = list(APMC_raw_data['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]].keys())
        
        for year in sorted(years):
            
            #write the data follwowing the structure dictated by the titles in the first row
            clean_data_writer.writerow([dist_name_prod[1], dist_name_prod[2], year, APMC_average_difference_raw['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]][year], APMC_average_difference_trend['maharashtra'][dist_name_prod[0]][dist_name_prod[1]][dist_name_prod[2]][year], dist_name_prod[0], 'maharashtra'])
            
            
#plotting time series to show the MSP with respect to the minimum price


#e.g. Split Black Gram in Mumbai

x1=[]
x2=[]


    
months = list(APMC_raw_data['maharashtra']['mumbai']['mumbai']['split black gram'][2016].keys())
        
    
for month in sorted(months):
            
    x1.append(APMC_raw_data['maharashtra']['mumbai']['mumbai']['split black gram'][2016][month])
    x2.append(APMC_trend_data['maharashtra']['mumbai']['mumbai']['split black gram'][2016][month])

        
#plot interactive figures where the MSP can be changed by the government 
#to ensure that it is always below the minimum market price
 
def plot_func1(correction1):
    plt.figure(1)
    plt.plot(x1)
    plt.axhline(y= msprice['split black gram'][2016] + correction1 , color='r', linestyle='-')
    plt.title('Minimum Price (raw) compared to MSP: ALWAYS ABOVE')
    plt.xlabel('Months since January 2016')
    plt.ylabel('Price')

interact(plot_func1, correction1 = widgets.FloatSlider(value=0,
                                               min=-max(x1),
                                               max=max(x1),
                                               step=2*max(x1)/1000))


def plot_func2(correction2):
    plt.figure(2)
    plt.plot(x2)
    plt.axhline(y= msprice['split black gram'][2016] + correction2, color='r', linestyle='-')
    plt.title('Minimum Price (trend) compared to MSP: ALWAYS ABOVE')
    plt.xlabel('Months since January 2016')
    plt.ylabel('Price')
    

interact(plot_func2, correction2 = widgets.FloatSlider(value=0,
                                               min=-max(x2),
                                               max=max(x2),
                                               step=2*max(x2)/1000))


#plotting time series to show the MSP with respect to the minimum price

#e.g. Maize in Bhokardan

y1=[]
y2=[]


    
months = list(APMC_raw_data['maharashtra']['jalna']['bhokardan']['maize'][2016].keys())
        
    
for month in sorted(months):
            
    y1.append(APMC_raw_data['maharashtra']['jalna']['bhokardan']['maize'][2016][month])
    y2.append(APMC_trend_data['maharashtra']['jalna']['bhokardan']['maize'][2016][month])

        
#plot interactive figures where the MSP can be changed by the government 
#to ensure that it is always below the minimum market price

def plot_func3(correction3):
    plt.figure(3)
    plt.plot(y1)
    plt.axhline(y= msprice['maize'][2016] +correction3, color='r', linestyle='-')
    plt.title('Minimum Price (raw) compared to MSP: CROSSING')
    plt.xlabel('Months since January 2016')
    plt.ylabel('Price')

interact(plot_func3, correction3 = widgets.FloatSlider(value=0,
                                               min=-max(y1),
                                               max=max(y1),
                                               step=2*max(y1)/1000))


def plot_func4(correction4):
    plt.figure(4)
    plt.plot(y2)
    plt.axhline(y= msprice['maize'][2016] + correction4 , color='r', linestyle='-')
    plt.title('Minimum Price (trend) compared to MSP: CROSSING')
    plt.xlabel('Months since January 2016')
    plt.ylabel('Price')
    
interact(plot_func4, correction4 = widgets.FloatSlider(value=0,
                                               min=-max(y2),
                                               max=max(y2),
                                               step=2*max(y2)/1000))

