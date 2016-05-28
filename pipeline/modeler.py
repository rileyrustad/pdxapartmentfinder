from __future__ import division
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json
import pickle

def clusterer(X, Y,neighborhoods):
    neighbors = []
    for i in neighborhoods:
        distance = ((i[0]-float(X))**2 + (i[1]-float(Y))**2)
        neighbors.append(distance)
    closest = min(neighbors)
    return neighbors.index(closest)

if __name__ == '__main__':
	with open('data/MasterApartmentData.json') as f:
	    my_dict = json.load(f)
	dframe = DataFrame(my_dict)

	dframe = dframe.T

	dframe = dframe[['content', 'laundry',  'price', 'dog', 'bed', 
	'bath', 'feet', 'long', 'parking', 'lat', 'smoking', 'getphotos', 
	'cat', 'hasmap', 'wheelchair', 'housingtype']]

	#save number of data points that we started with
	og = dframe.shape[0]

	#replace shared bathrooms with "half" of a bathroom
	dframe.bath = dframe.bath.replace('shared',0.5)
	dframe.bath = dframe.bath.replace('split',0.5)

	# We only want to model 
	dframe = dframe[dframe.lat > 45.4][dframe.lat < 45.6][dframe.long < -122.0][dframe.long > -123.5]

	aftermap = dframe.shape[0]

	print og - aftermap

	data = [[dframe['lat'][i],dframe['long'][i]] for i in dframe.index]

	from sklearn.cluster import KMeans
	km = KMeans(n_clusters=40)
	km.fit(data)
	neighborhoods = km.cluster_centers_
	neighborhoods = neighborhoods.tolist()
	for i in enumerate(neighborhoods):
	    i[1].append(i[0])

	pickle.dump(neighborhoods, open('data/neighborhoodlist.pkl','wb'))






	 

	neighborhoodlist = []
	for i in dframe.index:
	    neighborhoodlist.append(clusterer(dframe['lat'][i],dframe['long'][i],neighborhoods))
	dframe['neighborhood'] = neighborhoodlist


	dframe = pd.get_dummies(dframe, columns = ['laundry', 'parking', 'smoking', 
		'wheelchair', 'housingtype','neighborhood'])

	df2 = dframe[dframe.price < 10000].dropna()


	from sklearn.cross_validation import train_test_split
	features_train, features_test, price_train, price_test = train_test_split(df2.drop('price',axis=1), df2.price, test_size=0.33, random_state=42)

	from sklearn.ensemble import RandomForestRegressor
	from sklearn.metrics import r2_score
	reg = RandomForestRegressor()
	reg = reg.fit(features_train, price_train)

	forest_pred = reg.predict(features_test)
	forest_pred = np.array([[item] for item in forest_pred])

	print r2_score(forest_pred, price_test)

	import pickle

	print len(list(df2.columns.values))

	pickle.dump(list(df2.columns.values), open('data/columns.pkl','wb'))

	pickle.dump(reg, open('data/sklearn-model.pkl','wb'))

	for _,i in enumerate(forest_pred[:10]):
		print price_test[_], i







