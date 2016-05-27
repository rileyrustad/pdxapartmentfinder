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


def imputables_getter(my_dict):
	imputables = {}
	continuous_features = ['content', 'price', 'feet', 'getphotos','long', 
		'lat']
	discrete_features = ['laundry', 'bed', 'bath', 'housingtype', 'parking']

	imputables = {}

	for variable in continuous_features:
		imputables[variable] = averager(my_dict, variable)

	for variable in discrete_features:
		imputables[variable] = moder(my_dict, variable)
	
	return imputables
imputables = imputables_getter(my_dict)


def imputer(listing, imputables):
	for entry in listing:
		if entry == 'smoking':
			if listing[entry] != 'no smoking':
				listing[entry] = 'smoking'
		if entry == 'wheelchair':
			if listing[entry] != 'wheelchair access':
				listing[entry] = 'no wheelchair access'
		if entry == 'bath':
			if listing[entry] == 'shared' or listing[entry] == 'split':
				listing[entry] = .5 
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


dframe = DataFrame(my_dict).T




dframe = dframe[['content', 'laundry',  'price', 'dog', 'bed', 
'bath', 'feet', 'long', 'parking', 'lat', 'smoking', 'getphotos', 
'cat', 'hasmap', 'wheelchair', 'housingtype']]

dframe = pd.get_dummies(dframe, columns = ['laundry', 'parking', 'smoking', 
	'wheelchair', 'housingtype'])


from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
	dframe.drop('price', axis = 1), dframe.price, test_size=0.33)




from sklearn.ensemble import RandomForestRegressor
reg = RandomForestRegressor()
reg.fit(X_train, y_train)



# processed = open('data/ProcessedDay90ApartmentData.json',"w")
# json.dump(my_dict, processed)
# processed.close()

if __name__ == '__main__':
	run()




