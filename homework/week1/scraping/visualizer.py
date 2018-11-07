#!/usr/bin/env python
# Name:
# Student number:
"""
This script visualizes data obtained from a .csv file
"""
import csv
import matplotlib.pyplot as plt


# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018


# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}
average_dict = {}
import csv

with open('movies.csv', newline='') as csvfile:
    # dictreader reads lines in a csv file and can separate values per column
     reader = csv.DictReader(csvfile)
     for row in reader:
         # create variables to put the values of the read row in
         year = row['Year']
         rating = row['Rating']
         # dictionary already exists > append rating to the list specified by key(year)
         data_dict[year].append(rating)


# calculate average rating per year and store values in dictionary
for key in data_dict:
    year = key
    nr_of_ratings = (len(data_dict[year]))
    sum_rating = (sum(float(i) for i in data_dict[year]))
    average = sum_rating / nr_of_ratings
    average_dict[year] = round(average,1)


# create tuples for every item in average_dict
tuples = average_dict.items()
# use * to unpack the values in tuple(or any other iterable thing) into separate values
# zip takes n lists and creates n-tuple pairs from each element from both lists
x, y = zip(*tuples)
plt.plot(x, y, color='c', linewidth=1.0)
plt.xlabel("Year")
plt.ylabel("Average IMDB rating")
plt.show()



if __name__ == "__main__":
    print(data_dict)
