# -*- coding: utf-8 -*-
'''python module contains functions built to parse multnomah county craigslist apartment html
'''
#from future import division, print_function
import numpy as np

def attributes(soup):
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
    #try:   
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

def bedbathfeet(bedbathfeet):
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

def price(soup):
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

def smoking(attributes):
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



def furnished(attributes):
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
        
def wheelchair(attributes):
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
        
def laundry(attributes):
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


def housing_type(attributes):
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

def parking(attributes):
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
    

def available(attributes):
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
            
def cat(attributes):
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
        
def dog(attributes):
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
           
def deleted(soup):
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

def content_length(soup):
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
    
def lat_lon(soup):
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
        x = []
        for _,i in enumerate(str(summary)):
            if i == '"':
                x.append(_)

        lat = str(summary)[x[4]+1:x[5]]
        lon = str(summary)[x[6]+1:x[7]]
        if len(lat) > 0 and len(lon) > 0:
            return lat, lon
        else:
            return np.nan, np.nan

    return LatLon(soup)
        
def has_map(soup):
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
        
def photos(soup):
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

def time_posted(soup):
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



