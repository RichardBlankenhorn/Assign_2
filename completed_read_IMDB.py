__author__ = 'Richard'

import urllib2
from bs4 import BeautifulSoup
import json
import completed_util_imdb as util
import csv

m_per_page = 50 # by default, imdb return 50 movies page url.

def read_m_by_rating(first_year, last_year, top_number):

    startNumber = 1
    global m_per_page
    item_per_page = m_per_page
    urlList = []
    if top_number > (m_per_page):
        while (top_number - item_per_page) > 0:
            desired_url = 'http://www.imdb.com/search/title?at=0&sort=user_rating&start=' + str(startNumber) + '&title_type=feature&year=' + str(first_year) + ',' + str(last_year)
            urlList.append(desired_url)
            startNumber += m_per_page
            item_per_page += m_per_page
        urlList.append('http://www.imdb.com/search/title?at=0&sort=user_rating&start=' + str(startNumber) + '&title_type=feature&year=' + str(first_year) + ',' + str(last_year))
    else:
        urlList.append('http://www.imdb.com/search/title?at=0&sort=user_rating&start=' + str(startNumber) + '&title_type=feature&year=' + str(first_year) + ',' + str(last_year))

    complete_movie_list = []
    for item in urlList:
        if item == urlList[len(urlList) - 1]:
            if (top_number % m_per_page) == 0:
                movies = read_m_from_url(item)
                for movie in movies:
                    complete_movie_list.append(movie)
            else:
                num_of_m_needed = (top_number % m_per_page)
                movies = read_m_from_url(item, num_of_m_needed)
                for movie in movies:
                    complete_movie_list.append(movie)
        else:
            movies = read_m_from_url(item)
            for movie in movies:
                complete_movie_list.append(movie)

    return complete_movie_list


def test_read_m_by_rating():

    print read_m_by_rating(2005,2015,61)

def read_m_from_url(url, num_of_m=50):
    #this function, read a number of movies from a url. That's say you set num_of_m=25, you want to read 25 movies from the page. The default value is 50
    #html_string = util.read_html(url) # given a url you need to read the hmtl file as a string.
    # create a soup object
    #soup = BeautifulSoup(html_string, "html.parser")
    # Fetching a table that includes all the movies. In our lecture, we talked about find and find_all functions.
    # for example, find_all('table') will give you all tables on the page. Actually, this find or find_all function can have two parameters,
    # in the code below 'table' is the tag name and 'results' is an attribute value of the tag. You can also do
    # movie_table = soup.find('table', {'class':'result'}). Here you explicitly say: I want to find a table with attribute class = 'result'.
    # Since on each imdb page, there's only one table with class = 'results', we can use find rather than find_all. Find_all will return a list of table tags, while
    # find() will return only one table
    #movie_table = soup.find('table', 'results') # equivalent to  movie_table = soup.find('table', {'class':'result'})
    #list_movies = [] # initialize the return value, a list of movies
    # Using count track the number of movies processed. now it's 0 - No movie has been processed yet.
    #count = 0

    html_string = util.read_html(url)
    soup = BeautifulSoup(html_string, "html.parser")
    movie_table = soup.find_all('table', 'results')
    table = movie_table[0]
    trs = table.find_all('tr')
    movieCount = 0
    list_movies = []

    for tr in trs:
        rank = tr.find_all('td', 'number')
        year = tr.find_all('span', 'year_type')
        rating = tr.find_all('span', 'value')
        genre = tr.find_all('span', 'genre')
        title = tr.find_all('td', 'title')
        runtime = tr.find_all('span', 'runtime')
        movie_list = {}
        if movieCount <= num_of_m:
            for a in title:
                some_title = a.find_all('a')
                a_target_title = some_title[0].get_text().encode('ascii', 'ignore').replace("*","")
                movie_list['title'] = util.process_str_with_comma(a_target_title)
            for number in rank:
                the_number = number.get_text().encode('ascii', 'ignore').replace("*","").replace(".","")
                movie_list['rank'] = the_number
            for value in year:
                the_value = value.get_text().encode('ascii', 'ignore').replace("*","").replace("(", "").replace(")","").replace(" Short Film", "")
                movie_list['year'] = the_value
            for rate in rating:
                the_rating = rate.get_text().encode('ascii', 'ignore').replace("*","")
                movie_list['rating'] = the_rating
            for gen in genre:
                genre_list = []
                spec_genre = gen.find_all('a')
                for attr in spec_genre:
                    the_specific_genre = attr.get_text().encode('ascii', 'ignore').replace("*","")
                    genre_list.append(the_specific_genre)
                    movie_list['genre'] = genre_list
            for time in runtime:
                the_run_time = time.get_text().encode('ascii', 'ignore').replace("*","").replace(" mins.","")
                movie_list['runtime'] = the_run_time
            if 'runtime' not in movie_list.keys():
                movie_list['runtime'] = ''
            if 'genre' not in movie_list.keys():
                movie_list['genre'] = ''
            if 'rating' not in movie_list.keys():
                movie_list['rating'] = ''
            list_movies.append(movie_list)
        movieCount += 1

    del list_movies[0]

    return list_movies


def test_read_m_from_url():

    url = "http://www.imdb.com/search/title?at=0&sort=user_rating&start=51&title_type=feature&year=2005,2014"
    print read_m_from_url(url, 21)


def write_movies_json(final_list, filename):
    f = open(filename,"w")
    json.dump(final_list, f, indent=4, separators=(",",": "))
    f.close()
    return

def test_write_movies_json(): # output of the test is in "movies.json"
    li = read_m_by_rating(2005, 2016, 251)
    write_movies_json(li,'MovieFile.json')

def write_movies_csv(final_list, filename):

    lis = []
    genre_list = []
    for mov in final_list:
        movie_genre = mov['genre']
        for genre in movie_genre:
            if genre not in genre_list:
                genre_list.append(genre)

    header = ['Rank', 'Title', 'Year', 'Rating', 'Runtime']
    total_header = header + genre_list
    lis.append(total_header)
    for movie in final_list:
        the_final_movie_list = []
        genre_string = "".join(map(str, util.create_dummy_values(movie['genre'],list(genre_list))))
        the_final_movie_list.append(movie['rank'])
        the_final_movie_list.append(movie['title'])
        the_final_movie_list.append(movie['year'])
        the_final_movie_list.append(movie['rating'])
        the_final_movie_list.append(movie['runtime'])
        for value in genre_string:
            the_final_movie_list.append(value)
        lis.append(the_final_movie_list)

    result_file = open(filename, "wb")

    wr = csv.writer(result_file, dialect='excel')

    for item in lis:
        wr.writerow(item)
    result_file.close()


def test_write_movies_csv(): # output of the test method is in "movies.csv"
    li = read_m_by_rating(2005, 2016, 100)
    write_movies_csv(li, 'MovieBook.csv')

def main():
    the_final_list = read_m_by_rating(2005, 2016, 15)
    write_movies_csv(the_final_list, 'MovieBook.csv')
    write_movies_json(the_final_list, 'MovieFile.json')
    return

if __name__ == '__main__':
    main()