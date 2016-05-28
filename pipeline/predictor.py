import pickle
from scrape import info
import pandas as pd
from pandas import DataFrame
from processing import imputer, imputables_getter
import json
from modeler import clusterer


def predict(listing, my_dict, path):
	''' Predict the price of an apartment listing.
	Parameters
	----------
	listing: Craigslist ID number for the individual listing.

	my_dict: Dictionary containing data for listings in the last 90 days

	path: pathway to data file from where the commans is called

	Returns
	-------
	pred = prediction price of 


	'''


	# Pull the info for a specific listing.
	my_info1 = info(listing,{})
	my_info = my_info1.copy()
	
	

	reg = pickle.load(open(path+'sklearn-model.pkl',"rb" ))


	# dframe = dframe[dframe.lat > 45.4][dframe.lat < 45.6][dframe.long < -122.0][dframe.long > -123.5]

	imputables = imputables_getter(my_dict)

	# impute any missing data.
	my_info = imputer(my_info[listing], imputables)

	dframe = DataFrame({listing:my_info}).T[['content', 'laundry',  'price', 
	'dog', 'bed', 'bath', 'feet', 'long', 'parking', 'lat', 'smoking', 
	'getphotos', 'cat', 'hasmap', 'wheelchair', 'housingtype']]


	neighborhoods = pickle.load(open(path+'neighborhoodlist.pkl', "rb"))

	# Assign our listing to its closest neighborhood
	dframe['neighborhood'] = clusterer(
		dframe['lat'][listing],dframe['long'][listing],neighborhoods)

	columns = pickle.load(open(path+'columns.pkl', "rb"))

	# Get rid of unused columns
	for row in dframe:
		if row not in columns:
			dframe = dframe.drop(row, axis = 1)
	for column in columns:
		if column not in dframe:
			dframe[column] = 0

	# Standardize the column order for the model
	dframe = dframe[columns]

	price = my_info['price']
	print price

	pred = reg.predict(dframe.drop('price',axis=1))

	print 'Prediction: ' + str(pred[0])
	print 'Actual: ' + str(price)
	print 'Diff: ' + str(pred[0] - float(price))
	return pred, my_info1, my_info

if __name__ == '__main__':
	listing = '5580713155'
	with open('data/Day90ApartmentData.json') as f:
	    my_dict = json.load(f)
	print predict(listing, my_dict, 'data/')

