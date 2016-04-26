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

# =============================================================================
    
def GetMasterApartmentData():
    '''Loads previous data, or creates a new file to hold data.
    
    Returns
    -------
    
    my_dict : dictionary of dictionaries containing all scraped data.   
    '''
    # Checks if we have a data file saved as a python dictionary in a JSON file
    if os.path.isfile('data/MasterApartmentData.json'
                    ) == True:
        f = open('data/MasterApartmentData.json')      
        my_dict = json.load(f)
        f.close()
        return my_dict
    # If the file doesn't exist, create that file.
    else:
        f = open('data/MasterApartmentData.json','w')
        f.close()
        my_dict = {}
        return my_dict

def NumberGetter(unexplored_id_numbers, my_dict, page):
    '''A Craigslist Apartment ID number scraper.
    
    This scaper gets the newest apartment entries and appends them to our 
    existing list of unexplored ID numbers
     
    Parameters
    ----------   
    unexplored_id_numbers : List of craigslist ID numbers that haven't been
    explored yet, or an empty list.
    
    my_dict : See description in main() function.
    
    page : string added to base url that tells which page to scrape for ID
    numbers.
    
    Returns
    -------
    unexplored_id_numbers : A list of ID numbers stored as strings
    '''
    # Assign page to scrape for Cragslist ID numbers, and get html content.
    # There are 25 pages available, with 100 entries per page.
    url = 'http://portland.craigslist.org/search/mlt/apa'+page
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c,'lxml')
    summary = soup.find("div",{'class':'content'})
    rows = summary.find_all("p",{'class':'row'})
    
    # Create a list of all available ID numbers
    new_id_numbers = []    
    for i in rows:
        r = str(i)
        new_id_numbers.append(r[25:35])
    
    # Check ID numbers against what has already been scraped
    for number in new_id_numbers:
        if number not in my_dict:
            unexplored_id_numbers.append(number)

    return unexplored_id_numbers 


def InfoGetter(id_number,my_dict):
    '''Scrape data from each craigslist ad.
    
    I scraped specific tags of HTML. These tags were consistant across all 
    listings. Most were from drop down options when setting up the listing.
    
    Parameters
    ----------
    id_number : string that contains the url ID number from Craigslist to 
        Scrape.
    
    my_dict : See description in main() function.
    
    Returns
    -------
    my_dict : and updated dictionary
    '''

    # Scrape page for listing
    url = 'https://portland.craigslist.org/mlt/apa/'+id_number+'.html'
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c,'lxml')
    
    # Check to see if listing has been deleted since you scraped the ID
    if Deleted(soup) == True:
        return my_dict
    
    # Run info functions to gather specific data
    else:
        price = GetPrice(soup)     
        bedbathfeet, attributes = GetAttributes(soup)
        cat = Cat(attributes)
        dog = Dog(attributes)
        laundry = Laundry(attributes)
        housingtype = HousingType(attributes)
        parking = Parking(attributes)
        wheelchair = WheelChair(attributes)
        smoking = Smoking(attributes)
        bed, bath, feet = BedBathFeet(bedbathfeet)
        content = ContentLength(soup)
        lat, lon = LatLon(soup)
        hasmap = HasMap(soup)
        getphotos = GetPhotos(soup)
        date, time = TimePosted(soup)
        
    # Add a new entry to my_dict
        my_dict[id_number]={'price':price,'bed':bed,'bath':bath,'cat':cat,
        'dog':dog,'feet':feet,'housingtype':housingtype,'laundry':laundry,
        'parking':parking,'wheelchair':wheelchair,'smoking':smoking,
        'content':content,'lat':lat,'long':lon,'hasmap':hasmap,
        'getphotos':getphotos,'date':date,'time':time}
        #print GetAttributes(soup)  
        return my_dict
    
def GetPrice(soup):
    '''Finds price of a listing.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    price : int of listing price.
    '''
    # Parse down to just the price HTML tag
    summary = soup.find("span",{'class':'price'})

    # Check to see if listing has a price.
    if summary == None:
        return np.nan
        
    # Return the price.
    else: 
        text = summary.find(text=True)
        price = int(str(text)[1:])
        return price

       
def GetAttributes(soup):
    '''Parses HTML down to just the attributes of a listing.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    bedbathfeet : HTML that contains just the bedroom, bathroom, and square
    footage data.
    
    attributes : HTML that contains the additional attributes.
    '''

    # mapAndAttrs HTML tag has all of the uniform attributes 
    summary = soup.find("div",{'class':'mapAndAttrs'})
    summary2 = summary.find_all("span")
    summary3 = summary.find_all("b")
    bedbathfeet = []
    attributes = []
    
    # All bolded attributes are number of baths, beds, or square feet
    for i in summary3:
        text = i.find(text=True)
        if text != 'open house dates':
            bedbathfeet.append(text)

    # The unbolded attributes are saved in a separate list
    for i in summary2:
        text = i.find(text=True)
        if text not in bedbathfeet:
            attributes.append(text)
            
    return bedbathfeet, attributes

def BedBathFeet(bedbathfeet):
    '''Find number of bedrooms, bathrooms, and square feet.
    
    Parameters
    ----------
    bedbathfeet : List containing number of bedrooms, bathrooms, and square 
    footage. See GetAttributes
    
    Returns
    -------
    bedbathfeet : list with available in the format[# beds, # baths, 
                                                    square feet]
    '''
    # Test to see if all intergers or if it contains a string
    try:
        # It has no strings
        bedbathfeet = [int(i) for i in bedbathfeet]
        if len(bedbathfeet) == 3:
            return bedbathfeet[0],bedbathfeet[1],bedbathfeet[2]
    
        elif len(bedbathfeet) == 2:
            # No entries have greater than 10 bedrooms, so we can infer that
            # that the larger value is square footage.
            if max(bedbathfeet) > 10:
                return bedbathfeet[0],np.nan,bedbathfeet[1]
            else:
                return bedbathfeet[0],bedbathfeet[1],np.nan
        elif len(bedbathfeet) == 1:
            if bedbathfeet[0] > 10:
                return np.nan,np.nan,bedbathfeet[0]
            else:
                return bedbathfeet[0],np.nan,np.nan
        elif len(bedbathfeet) == 0:
            return np.nan,np.nan,np.nan
    except ValueError:
        if len(bedbathfeet) == 3:
            return int(bedbathfeet[0]),str(bedbathfeet[1]),int(bedbathfeet[2])
        elif len(bedbathfeet) == 2:
            bath = bedbathfeet.pop(bedbathfeet.index(max(bedbathfeet)))
            if max(bedbathfeet) > 10:
                return np.nan,bath,bedbathfeet[0]
            else:
                return bedbathfeet[0],bath,np.nan
        elif len(bedbathfeet) == 1:
            return np.nan,bedbathfeet[0],np.nan
        elif len(bedbathfeet) == 0:
            return np.nan,np.nan,np.nan


def Smoking(attributes):
    '''Finds if a listing allows smoking.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    smoking : string of 'no smoking' or NaN value if none listed.
    '''
    x=[]    
    for i in attributes:
        if str(i) == 'no smoking':
            x.append(str(i))
    if len(x)>0:
        smoking = str(x[0])
        return smoking
    else:
        return np.nan

def Furnished(attributes):
    '''Finds if a listing is furnished.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    smoking : string of 'furnished' or NaN value if none listed.
    '''
    x=[]    
    for i in attributes:
        if str(i) == 'furnished':
            x.append(str(i))
    if len(x)>0:
        furnished =  str(x[0])
        return furnished
    else:
        return np.nan
        
def WheelChair(attributes):
    '''Finds if a listing is wheelchair accessible.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    smoking : string of 'furnished' or NaN value if none listed.
    '''
    x=[]    
    for i in attributes:
        if str(i) == 'wheelchair accessible':
            x.append(str(i))
    if len(x)>0:
        wheelchair = str(x[0])
        return wheelchair
    else:
        return np.nan
        
def Laundry(attributes):
    '''Finds the laundry type a listing has.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    a string of the type of laundry available or NaN value if none listed.
    '''
    x=[]    
    for i in attributes:
        if str(i) == 'w/d in unit':
            x.append(str(i))
        elif str(i) == 'laundry in bldg':
            x.append(str(i))
        elif str(i) == 'laundry on site':
            x.append(str(i))
        elif str(i) == 'w/d hookups':
            x.append(str(i))
        elif str(i) == 'no laundry on site':
            x.append(str(i))
    if len(x)>0:
        return str(x[0])
    else:
        return np.nan


def HousingType(attributes):
    '''Finds the housing type a listing has.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    a string of the type of housing available or NaN value if none listed.
    '''
    x=[]    
    for i in attributes:
        if str(i) == 'apartment':
            x.append(str(i))
        elif str(i) == 'condo':
            x.append(str(i))
        elif str(i) == 'cottage/cabin':
            x.append(str(i))
        elif str(i) == 'duplex':
            x.append(str(i))
        elif str(i) == 'flat':
            x.append(str(i))
        elif str(i) == 'house':
            x.append(str(i))
        elif str(i) == 'in-law':
            x.append(str(i))
        elif str(i) == 'loft':
            x.append(str(i))
        elif str(i) == 'townhouse':
            x.append(str(i))
        elif str(i) == 'manufactured':
            x.append(str(i))
        elif str(i) == 'assisted living':
            x.append(str(i))
        elif str(i) == 'land':
            x.append(str(i))
    if len(x)>0:
        return str(x[0])
    else:
        return np.nan

def Parking(attributes):
    '''Finds the parking type a listing has.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    a string of the type of parking available or NaN value if none listed.
    '''
    x=[]    
    for i in attributes:
        if str(i) == 'carport':
            x.append(str(i))
        elif str(i) == 'attached garage':
            x.append(str(i))
        elif str(i) == 'detached garage':
            x.append(str(i))
        elif str(i) == 'off-street parking':
            x.append(str(i))
        elif str(i) == 'street parking':
            x.append(str(i))
        elif str(i) == 'valet parking':
            x.append(str(i))
        elif str(i) == 'no parking':
            x.append(str(i))
    if len(x)>0:
        return str(x[0])
    else:
        return np.nan
    

def Available(attributes):
    '''Finds the date a listing is available.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    a string of the date a listing is available.
    '''
    x = []    
    for i in attributes:
        if "available" in i:
            x.append(i)
    if len(x) > 0:
        return str(x[0])[10:]
    else:
        return np.nan
            
def Cat(attributes):
    '''Finds whether a listing allows cats.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    1 if the listing allows cats and a 0 if it doesn't
    '''
    if u'cats are OK - purrr' in attributes:
         return 1
    else:
        return 0
        
def Dog(attributes):
    '''Finds whether a listing allows dogs.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    1 if the listing allows dogs and a 0 if it doesn't
    '''
    
    if u'dogs are OK - wooof' in attributes:
        return 1
    else:
        return 0
           
def Deleted(soup):
    '''Finds whether a listing has been deleted since it's ID was scraped.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    If the listing has been removed, return false, or else return true.
    '''
    summary = soup.find("div",{'class':"removed"}) 
    if summary == None:
        return False
    else:
        return True

def ContentLength(soup):
    '''Finds the number of characters in a listings content
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    The length of listings content
    '''
    summary = soup.find("section",{'id':'postingbody'})
    if summary == None:
        return np.nan
    else:
        summary2 = "".join(str(summary))
        return len(summary2)
    
def LatLon(soup):
    '''Finds the lattitute and longitude coordinates for a listing
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    lat : a listings lattitude
    
    lon: a listings longitude
    '''
    
    summary = soup.find("div",{'class':'viewposting'})
    if summary == None:
        return np.nan, np.nan
    else:
        summarystring = str(summary)
        if summarystring[58:60] == '""' or summarystring[57:59] == '""':
            return np.nan, np.nan
        
        if summarystring[58] == '"':
            if summarystring[96] == '"':
                lat = summarystring[59:68]
                lon = summarystring[86:96]
                return float(lat), float(lon)
            else:
                lat = summarystring[59:68]
                lon = summarystring[86:97]
                return float(lat), float(lon)
        else:
            if summarystring[95] == '"':
                lat = summarystring[58:67]
                lon = summarystring[85:95]
                return float(lat), float(lon)
            else:
                lat = summarystring[58:67]
                lon = summarystring[85:96]
                return float(lat), float(lon)
        
def HasMap(soup):
    '''Determines if a listing has a map.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    1 if it has a map, 0 if it doesn't
    '''
    summary = soup.find("div",{'class':'mapbox'})
    if summary == None:
        return 0
    else:
        return 1
        
def GetPhotos(soup):
    '''Counts the number of photos a listing has.
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    Number of photos posted on the listing
    '''
    summary = soup.find("div",{'id':'thumbs'})
    if summary == None:
        return 0
    else:
        summary2 = summary.find_all("a")
    return len(summary2)

def TimePosted(soup):
    '''Determines when a posting was listed
    
    Parameters
    ----------
    soup : Scraped HTML parsed down to just the content of the page.
    
    Returns
    -------
    The time a listing was posted.
    '''
    summary = soup.find("time",{'class':'timeago'})
    date = str(summary)[32:42]
    time = str(summary)[43:51]
    return date, time

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

def dump(my_dict, fil):
    '''Saves data to a file.
    
    Parameters
    ----------
    my_dict : See main() for description
    
    fil = file where you want to save your data.
    '''
    dframe = DataFrame.from_dict(my_dict)
    dframe.to_csv(fil)
    fil.close()
    

def main():
    '''Adds all unscraped listings data to existing data files
    
    my_dict : Dictionary of dictionaries containing all scraped listings.
        It's structured like this:
            {'id_number':{variable_1: value_1,
                          variable_2: value_2}
               }
    Outputs
    -------
    TodayData : Only data collected from today.
    
    TodayMasterData : New data combined with old data. Saved so we can 
                      reference it later 
    
    MasterData: ongoing updated data file.
    
    '''
    # Create dictionary from previous data.
    my_dict = GetMasterApartmentData()
    print 'length of my_dict is '+str(len(my_dict))
    unexplored_id_numbers = []
    newdict = {}
    counter = 0
    page_numbers = ['']+["?s='"+str(x+1)+'00' for x in range(24)]
    
    # Collect all of the unexplored ID numbers. 
    for page in page_numbers:
        print str(page)        
        unexplored_id_numbers = NumberGetter(unexplored_id_numbers,my_dict,page)
        # Sleep at random intervals so that craigslist doesn't disconnect    
        time.sleep(random.randrange(3,6)) 
    print unexplored_id_numbers
    print len(unexplored_id_numbers)
    while len(unexplored_id_numbers)>0:
        for i in enumerate(unexplored_id_numbers):
            id_number = unexplored_id_numbers.pop(-1)
            # Check if listing info has already been collected
            if id_number not in my_dict or newdict:
                print str(id_number)+' '+ str(counter)
                # Get info for listing
                newdict = InfoGetter(id_number,newdict)
                time.sleep(random.randrange(2, 3))
                counter += 1
    date = str(datetime.datetime.now())[:19].replace(' ','_').replace(':','.')
    # Save the Data  
    TodayData = open('data/TodaysData/TodaysData'+date+'.json',"w")
    TodayMasterData = open('data/TodaysMasterData/MasterApartmentData'+date+'.json',"w")
    MasterData = open('data/MasterApartmentData.json',"w")
    json.dump(newdict,TodayData)
    my_dict = merge_two_dicts(my_dict,newdict)   
    json.dump(my_dict, TodayMasterData)
    json.dump(my_dict, MasterData)

    
if __name__ == '__main__':
    main()
 
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
