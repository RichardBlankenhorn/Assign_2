__author__ = 'Richard'
import urllib2

# Given a list of categories, we create dummies for these categories
# For example, in our assignment, we have a categorical variable called 'genre', 
# which takes values including 'Mystery','Romance','Sport','Sci-Fi','Family','Adventure','Horror'.
# When we do data mining, we need to convert this variable 'genre' into a list of dummy variables ['Mystery','Romance','Sport','Sci-Fi','Family','Adventure','Horror'].
# For an individual movie, if its genre is romance, sport and family, then we will represent its genre as [0, 1, 1, 0, 1, 0, 0], where 0 represents 'no' and 1 'yes'
# [0, 1, 1, 0, 1, 0, 0] means the genre of the movie is not 'Mystery', is 'Romance', is 'Sport', is not 'Sci-Fi', is 'Family', is not 'Adventure', and is not 'Horror'
# 
def create_dummy_values(small_list, large_list):
    result = []
    for item in large_list:
        if item in small_list:
            result.append(1)
        else:
            result.append(0)
    return result

def test_create_dummy_values():
    large_list = ['Mystery','Romance','Sport','Sci-Fi','Family','Adventure','Horror']
    small_list = ['Romance','Sport','Family']
    print create_dummy_values(small_list,large_list)# output:[0, 1, 1, 0, 1, 0, 0]


# read url and output the html file as a string
def read_html(url):
    test_url = urllib2.urlopen(url)
    readHtml = test_url.read()
    return readHtml

def test_read_html():
    print read_html('http://www.imdb.com/search/title?at=0&sort=user_rating&start=1&title_type=feature&year=2005,2015')

# if a string contains comma, use "" to enclose the string
def process_str_with_comma(string):
    if ',' in string:
        new_string = '"' + string + '"'
    else:
        new_string = string
    return new_string

def test_process_str_with_comma():
    """output:
    string: it is a string
    string: "it is a string, right"
    """
    string = 'it is a string'
    print "string: " + process_str_with_comma(string)
    string = 'it is a string, right'
    print "string: " + process_str_with_comma(string)

def main():
    test_create_dummy_values()
    test_read_html()
    test_process_str_with_comma()

    return

if __name__ == '__main__':
    main()