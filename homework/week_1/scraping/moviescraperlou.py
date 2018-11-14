#!/usr/bin/env python
# Name:
# Student number:
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'

# the following list will contain dictionaries for each movie
movies_dict = []

def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """

    # after inspecting the imdb page manually, lister-list was found to be listing all movies
    # in lister-list are 50 lister-items(movies)
    movies_top50 = dom.find_all(class_="lister-item")

    for movie in movies_top50:
        # navigate further through the HTML inspection of imdb
        # create dictionary for every movie
        temp_movie = {}
        title = movie.find(class_="lister-item-header").a.string
        temp_movie['title'] = title

        rating = movie.find("div", class_="inline-block ratings-imdb-rating").strong.string
        temp_movie['rating'] = rating

        release = movie.find(class_="lister-item-year text-muted unbold").string
        if len(release) == 6:
            release = release[1 : 5]
        else:
            release = release[(-1-4) : (-1)]
        temp_movie['release'] = release

        runtime = movie.find(class_="runtime").string
        split_time = runtime.split()
        runtime = split_time[0]
        temp_movie['runtime'] = runtime

        # select specific attribute containing 'something':   $("[title*='hello']")
        stars = movie.select("a[href*='ref_=adv_li_st_']")
        film_actors = []
        for actor in stars:
            actor = actor.string
            film_actors.append(actor)
        string_actors = str(film_actors)
        temp_movie['actors'] = string_actors
        #  add dictionary for this single movie to the list of movies
        movies_dict.append(temp_movie)

    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED MOVIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

    return [movies_dict]   # REPLACE THIS LINE AS WELL IF APPROPRIATE


def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title','Rating', 'Year', 'Actors', 'Runtime'])
    for movie in movies_dict:
        writer.writerow([movie['title'], movie['rating'], movie['release'], movie['actors'], movie['runtime']])
        # movie['title'], movie['rating'], movie['release'], movie['actors'], movie['runtime']

    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE MOVIES TO DISK


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
