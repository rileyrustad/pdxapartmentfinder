import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json
from collections import Counter
import operator

#========================================================

#open the data from the last 90 days
with open('data/Day90ApartmentData.json') as f:
    my_dict = json.load(f)


def averager(my_dict, key):
	temp = []
	for entry in my_dict:
		if my_dict[entry][key] < 10000:
			temp.append(float(my_dict[entry][key]))
	return np.nanmean(temp)

def moder(my_dict, key):
	temp = []
	for entry in my_dict:
		temp.append(my_dict[entry][key])

	temp = Counter(temp)
	mode = max(temp.iteritems(), key=operator.itemgetter(1))[0]
	try:
		if np.isnan(mode):
			del temp[mode]
		mode = max(temp.iteritems(), key=operator.itemgetter(1))[0]
		return mode

	except TypeError:
		return mode


"""All of the variables in the dictionary are:
u'available', u'content', u'laundry', u'furnished', u'price',
u'time', u'dog', u'bed', u'bath', u'feet', u'date', u'long', u'parking',
u'lat', u'smoking', u'getphotos', u'cat', u'hasmap', u'wheelchair', 
u'housingtype', u'lastseen']"""

"""All variables used: u'content', u'laundry',  u'price', u'dog', u'bed', 
u'bath', u'feet', u'long', u'parking', u'lat', u'smoking', u'getphotos', 
u'cat', u'hasmap', u'wheelchair', u'housingtype'
"""

#go back and adjust the gis variables
continuous_features = ['content', 'price', 'feet', 'getphotos','long', 'lat']
discrete_features = ['laundry', 'bed', 'bath', 'housingtype', 'parking']

imputables = {}

for variable in continuous_features:
	imputables[variable] = averager(my_dict, variable)

for variable in discrete_features:
	imputables[variable] = moder(my_dict, variable)



def imputer(listing, imputables):
	for entry in listing:
		if entry == 'smoking':
			if listing[entry] != 'no smoking':
				listing[entry] = 'smoking'
		if entry == 'wheelchair':
			if listing[entry] != 'wheelchair access':
				listing[entry] = 'no wheelchair access'
		try:
			if np.isnan(listing[entry]):
				listing[entry]=imputables[entry]
		except TypeError:
			continue
		except KeyError:
			continue
	return listing

for listing in my_dict:
	my_dict[listing] = imputer(my_dict[listing],imputables)


processed = open('data/ProcessedDay90ApartmentData.json',"w")
json.dump(my_dict, processed)
processed.close()

#print imputer(my_dict['5467011165'],imputables)

# def processor(my_dict, entry):
# 	print my_dict[entry].keys()


# print processor(my_dict,'5590856490')


