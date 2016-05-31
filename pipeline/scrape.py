# -*- coding: utf-8 -*-
'''python module contains functions built to scrape multnomah county craigslist
apartment listings.
'''
#from future import division, print_function
import requests
from bs4 import BeautifulSoup
import lxml
import parse
import numpy as np
from datetime import date

def numbers(unexplored_id_numbers, my_dict, page):
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
    soup = BeautifulSoup(c, "html.parser")
    summary = soup.find("div",{'class':'content'})
    rows = summary.find_all("p",{'class':'row'})
    today = date.today()
    # Create a list of all available ID numbers
    new_id_numbers = []    
    for i in rows:
        r = str(i)
        new_id_numbers.append(r[25:35])
    
    # Check ID numbers against what has already been scraped
    for number in new_id_numbers:
        if number not in my_dict:
            unexplored_id_numbers.append(number)
        else:
            my_dict[number]['lastseen'] = str(today)

    return unexplored_id_numbers, my_dict

def info(id_number,my_dict):
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
    soup = BeautifulSoup(c,"html.parser")
    
    # Check to see if listing has been deleted since you scraped the ID
    if parse.deleted(soup) == True:
        return my_dict
    
    # Run info functions to gather specific data
    else:
        price = parse.price(soup)     
        bedbathfeet, attributes = parse.attributes(soup)
        cat = parse.cat(attributes)
        dog = parse.dog(attributes)
        laundry = parse.laundry(attributes)
        housingtype = parse.housing_type(attributes)
        furnished = parse.furnished(attributes)
        parking = parse.parking(attributes)
        wheelchair = parse.wheelchair(attributes)
        smoking = parse.smoking(attributes)
        bed, bath, feet = parse.bedbathfeet(bedbathfeet)
        content = parse.content_length(soup)
        lat, lon = parse.lat_lon(soup)
        hasmap = parse.has_map(soup)
        getphotos = parse.photos(soup)
        date, time = parse.time_posted(soup)
        available = parse.available(attributes)
        title = parse.title(soup)
        
    # Add a new entry to my_dict
        my_dict[id_number]={'price':price,'bed':bed,'bath':bath,'cat':cat,
        'dog':dog,'feet':feet,'housingtype':housingtype,'laundry':laundry,
        'parking':parking,'wheelchair':wheelchair,'smoking':smoking,
        'content':content,'lat':lat,'long':lon,'hasmap':hasmap,
        'getphotos':getphotos,'date':date,'time':time,'furnished':furnished,
        'available':available,'title':title}
        #print GetAttributes(soup)  
        return my_dict

if __name__ == '__main__':
    print info('5607570715',{})
