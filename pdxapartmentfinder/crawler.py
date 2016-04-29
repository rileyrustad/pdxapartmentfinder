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
    '''Merges two dictionaries together
    
    Parameters
    ----------
    x : a dictionary
    
    y : a dictionary
    
    Returns
    -------
    The time a listing was posted.
    '''
    z = x.copy()
    z.update(y)
    return z

unexplored_id_numbers = []
newdict = {}
page_numbers = ['']+["?s='"+str(x+1)+'00' for x in range(24)]

print "Searching for new listings..."
# Collect all of the unexplored ID numbers. 
for it, page in enumerate(page_numbers):     
    unexplored_id_numbers = scrape.numbers(unexplored_id_numbers,my_dict,page)
    status.printProgress(it, len(page_numbers), 
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
date = str(datetime.datetime.now())[:19].replace(' ','_').replace(':','.')
# Save the Data  

print str(len(newdict))+' new listings scraped'


TodayData = open('data/TodaysData/TodaysData'+date+'.json',"w")
TodayMasterData = open('data/TodaysMasterData/MasterApartmentData'+date+'.json'
                        ,"w")
MasterData = open('data/MasterApartmentData.json',"w")
json.dump(newdict,TodayData)
my_dict = merge_two_dicts(my_dict,newdict) 
print "Total number of listings scraped is now "+str(len(my_dict))  
json.dump(my_dict, TodayMasterData)
json.dump(my_dict, MasterData)
TodayData.close()
TodayMasterData.close()
MasterData.close()
'''from future import division, print_function'''
'''add status bar'''

'''Send an email, every time it throws an error. email would tell you when and
where it threw the error, and on which listing, so you can check it out'''
'''In the next iteration, do some NLP on listings. Rate each lisitng by the 
the difference between predicted + actual price. Then see if higher quality
listings use different language.'''
'''what if craigslist reuses numbers? build in back up for that'''
'''find the duplicates'''       
'''what if you added a "date last seen" function. You're already collecting ALL 
the ID's, just add todays date to all of them. I measures how long entries stay up'''
'''have all functions organized by classes'''
'''make a version that saves off 1.just today's entries 2. 
todays updated dict and 3. updates the master file'''         
'''find a way for chekcing duplicate listings with different numbers'''
'''fix bedbath so that it works for everything'''
'''don't forget to put in a separate file for todays date'''
'''make a version that runs automatically every day'''
'''The next interesting thing to collect would be how long a posting stays up for.
    You already have time posted, but since you're already pulling all of the numbers,
    you could update each entry to include "last seen". This would work better if 
    you had continuous collection rather than just once a day.'''
'''notificiation? it let's you know when it doesn't work'''
    
'''FOR WHEN YOU WANT TO USE PANDAS FOR ANALYSIS
dframe = DataFrame.from_dict(my_dict)
dataindex = [['price','bed','bath','cat','dog','feet','housingtype',
'laundry','parking','wheelchair','smoking','content','lat','lon','hasmap','getphotos','date','time']]
dframe2 = dframe.set_index(dataindex)
dframe2.to_csv('practice.csv')'''

''' FOR WHEN YOU WANT EMAIL NOTIFICATIONS, 
        2 functions -> my_dict got longer and my_dict stayed the same
        
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"'''
