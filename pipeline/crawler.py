# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 10:59:34 2016

@author: Riley Rustad <rileyrustad@gmail.com>

This Script is designed to scrape data from Multnomah County apartment ads 
from Craigslist.

"""
# =============================================================================
# Imports

import numpy as np
import os.path
from bs4 import BeautifulSoup
import requests
import time
import random
import datetime
import json
from pandas import DataFrame
import scrape
import status
from datetime import date, datetime



# =============================================================================
filepath =  'data/MasterApartmentData.json'

# Check if file exists, and if it does, load that data
if os.path.isfile(filepath) == True:
    f = open(filepath)      
    my_dict = json.load(f)
    f.close()
# If the file doesn't exist, create that file.
else:
    f = open(filepath,'w')
    f.close()
    my_dict = {}



print str(len(my_dict) )+" existing scraped listings." 

def merge_two_dicts(x, y):
    '''Merges two dictionaries together'''
    z = x.copy()
    z.update(y)
    return z

unexplored_id_numbers = []
newdict = {}
page_numbers = ['']+["?s='"+str(x+1)+'00' for x in range(24)]

print "Searching for new listings..."
# Collect all of the unexplored ID numbers. 
for it, page in enumerate(page_numbers):     
    unexplored_id_numbers, my_dict = scrape.numbers(unexplored_id_numbers,my_dict,page)
    status.printProgress((it+1), len(page_numbers), 
                         prefix = 'Progress:', suffix = 'Complete', 
                         decimals = 2, barLength = 25)
    # Sleep at random intervals so that craigslist doesn't disconnect    
    time.sleep(random.randrange(1,2)) 


new_numbers = len(unexplored_id_numbers)
print str(new_numbers)+" new listings found"
print ""
print "Scraping info from new listings..."

# Scrape new listings
while len(unexplored_id_numbers)>0:
    id_number = unexplored_id_numbers.pop(-1)
    it = new_numbers - len(unexplored_id_numbers)
    status.printProgress(it, new_numbers, prefix = 'Progress:',
                         suffix = 'Complete', decimals = 2, barLength = 50)
    # Get info for listing
    newdict = scrape.info(id_number,newdict)
    # Sleep at random intervals so that craigslist doesn't disconnect  
    time.sleep(random.randrange(1, 2))
# Save the Data  

print str(len(newdict))+' new listings scraped'

TodayData = open('data/TodaysData/TodaysData'+str(date)+'.json',"w")
MasterData = open('data/MasterApartmentData.json',"w")

json.dump(newdict,TodayData)
my_dict = merge_two_dicts(my_dict,newdict) 
json.dump(my_dict, MasterData)

print "Total number of listings scraped is now "+str(len(my_dict))

TodayData.close()
MasterData.close()

