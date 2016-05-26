# -*- coding: utf-8 -*-
'''python module contains functions built to scrape multnomah county craigslist
apartment listings.
'''
#from future import division, print_function


import sys 

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        print("\n")

# 
# Sample Usage
# 

# items = ["a", "b", "c", "d", "e"]
# i     = 0
# l     = len(items)

# # Initial call to print 0% progress
# printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
# for item in items:
#     # Do stuff...
#     # Update Progress Bar
#     i += 1
#     printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)