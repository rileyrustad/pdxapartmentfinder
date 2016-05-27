import pickle
from scrape import info
import pandas as pd
from pandas import DataFrame
from processing import imputer, imputables_getter
import json

listing = '5580713155'
def predict(listing):
	with open('data/Day90ApartmentData.json') as f:
	    my_dict = json.load(f)

	reg = pickle.load( open( 'data/sklearn-model.pkl', "rb" ) )

	my_info = info(listing,{})

	dframe = DataFrame(my_info)

	dframe = dframe.T


	dframe = dframe[['content', 'laundry',  'price', 'dog', 'bed', 
	'bath', 'feet', 'long', 'parking', 'lat', 'smoking', 'getphotos', 
	'cat', 'hasmap', 'wheelchair', 'housingtype']]

	dframe.bath = dframe.bath.replace('shared',0.5)
	dframe.bath = dframe.bath.replace('split',0.5)

	# dframe = dframe[dframe.lat > 45.4][dframe.lat < 45.6][dframe.long < -122.0][dframe.long > -123.5]

	imputables = imputables_getter(my_dict)

	my_info = imputer(my_info[listing], imputables)




	dframe = DataFrame({listing:my_info}).T


	neighborhoods = pickle.load( open( 'data/neighborhoodlist.pkl', "rb" ) )

	def clusterer(X, Y,neighborhoods):
	    neighbors = []
	    for i in neighborhoods:
	        distance = ((i[0]-float(X))**2 + (i[1]-float(Y))**2)
	        neighbors.append(distance)
	    closest = min(neighbors)
	    return neighbors.index(closest)


	dframe['neighborhood'] = clusterer(dframe['lat'][listing],dframe['long'][listing],neighborhoods)



	columns = pickle.load( open( 'data/columns.pkl', "rb" ) )

	for row in dframe:
		if row not in columns:
			dframe = dframe.drop(row, axis = 1)
	for column in columns:
		if column not in dframe:
			dframe[column] = 0
	dframe = dframe[columns]

	price = my_info['price']
	print price

	pred = reg.predict(dframe.drop('price',axis=1))

	print 'Prediction: ' + str(pred[0])
	print 'Actual: ' + str(price)
	print 'Diff: ' + str(pred[0] - float(price))

