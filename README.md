==================
# pdxapartmentfinder
==================

Find an apartment in portland!

CLCrawler is a set of tools designed to collect apartment data in the Portland/Multnomah County area, visualize and explore the data, model and interpret that data, and attempt to predict the pricing of additional listings in the same area.

Originally inspired by [this blog post](http://www.racketracer.com/2014/12/23/a-week-of-seattles-craigslist-apartment-pricing/) I decided that I wanted to give it a try, and add my own twist to it. 

This project is primarily a tool for me to learn, and experience a full stack data project of collecting, cleaning, interpreting, visualizing, modeling, and making predictions with data in python. If the code doesn't make sense, or if there are glaring formating mistakes, please take it with a grain of salt. I'm still learning, and am very open to suggestions!

### Requirements
* python 2.7
* ipython notebooks

Specific Libraries Used:
* numpy, os, pandas, bs4, requests, time, time, random, datetime, json, seaborn

I used the anaconda distribution of python libraries

### Sections
There is the scraper, the data visualization, and Modeling so far. 

###Future
Eventually I want to create a web app that tells you whether an apatment listing is over/under-priced, and by how much, as well as a recommender system that can recommend appartments similar to the one you're asking about.

#### Notes to Riley for ways to improve in the future

* Find and delete duplicate listings
	* Incorporate that checking in the crawler itself
* Update data into database hosted on my server at bluehost
* Add "date last seen" function to see how long listings stay up. I already collect all the id numbers, might as well just update todays date, and the difference in time between when it was posted and the last time it was seen.
* Make the crawler its own class. and create the functions within that class. I'm not sure if this makes sense, but I need the practice with classes.
* Find a way to get this to run every day. AWS? Bluehost Server?
* Send an email any time it throws an error, or wasn't able to collect the data.