from bs4 import BeautifulSoup
import requests
import networkx as nx
import time
import string

def get_info(G, movie_link, rows_deep, count, movies_visited, parent_node):
    '''
    This is the recursive function that goes into the different movies. it gets called on each movie.
    :param G: A graph object.
    :param movie_link: A beautiful soup object.
    :param rows_deep: the number of levels to go into. Note that As this becomes higher, the run time increases exponentially.
    :param count: the number of rows deep already visited.
    :param movies_visited: a list object of movie's tt_codes that have already been visited so that they are not visited again.
    :param parent_node: the parent node to the movies being visited. part of the Graph Object.
    :return: void. this function builds the graph object.
    '''

    #  base case
    if(count == rows_deep):
        return

    movies = {}
    tt_code_list = []

    for links in movie_link.find_all("div", class_="rec_overview"):
        # find link
        link = links.find('a')  # relative hyperlink

        # get ttcode
        tt_code = link.get('href').split('/')[2]
        #creates list of all ttCode of recommended movies
        tt_code_list.append(tt_code)

        # find title
        title = link.next_element['alt']

        # find rating
        div = links.find('div', class_='rating rating-list')
        rating = float(div.attrs['id'].split('|')[2])

        # find votes
        temp = div.attrs['title']

        # finds number between parentheses, replaces the ',' with '' and then turns the number into an int
        votes = int(temp[temp.find('(') + 1:temp.find(' ', temp.find('('))].replace(',', ''))

        #adds information to a dictionary
        movies[votes] = [title, tt_code, rating]

    sorted_movies = sorted(movies)  # sorts movies, returns list of movie keys in sorted order

    topThree = {}

    visit = 0
    index = len(sorted_movies) - 1
    while visit < 3 and index > 0:  # visit 3 movies or the whole movies list, whichever comes first.
        if movies[sorted_movies[index]][1] not in movies_visited:

            # adding movies to top three list
            topThree[sorted_movies[index]] = movies[sorted_movies[index]]

            #adding new top three movies to list of movies already seen
            movies_visited.append(topThree[sorted_movies[index]][1])

            #visit only 3 movies
            visit += 1
        else:
            #if already in movies_visited list, then print. this is mostly a log function and will be removed later
            print('{} already visited'.format(movies[sorted_movies[index]][0]), end=', ')

            # still want to create connection even if its been visited before
            G.add_edge(parent_node, movies[sorted_movies[index]][1])

        #  go backwards through the sorted movies to find top three
        index -= 1
    print('')

    #logging
    print('topThree:', topThree)

    count += 1  # increment count for recursive function

    #  going through top three
    for key, movie_specs in topThree.items():
        r1 = requests.get("http://www.imdb.com/title/" + movie_specs[1])
        movie = BeautifulSoup(r1.content, "lxml")
        if count != 3:  # logging
            print('visiting {}'.format(movie_specs))

        # build node
        G.add_node(movie_specs[1], title=movie_specs[0], votes=key, rating=movie_specs[2])
        #attach node to graph
        G.add_edge(parent_node, movie_specs[1])

        # call recursive function
        get_info(G, movie, rows_deep, count, movies_visited, movie_specs[1])  # passing in the tt_code as the parent_node

def create_parent_node(G, soup):
    '''
    This finds and creates the central, parent node and associates it with the graph
    :param G: networkx Graph object
    :param soup: beautiful_soup object
    :return: node_key (str)
    '''
    # insert actual web scraping for parent node
    G.add_node('tt3501632', title='Top Gun', votes=123456, imdb_score=7.9)
    return 'tt3501632'

# keep for testing:
def scraper(hyperlink):
    G = nx.Graph()

    user_movie = hyperlink.replace(" ", "+")
    temp_movie = "iron+man"
    print(user_movie)
    movie_link = get_hyperlink(user_movie)

    r = requests.get(movie_link)
    soup = BeautifulSoup(r.content, "lxml")
    rows_deep = 4
    count = 0

    #  need to create a parent node
    #  Node(tt028365, 'title': 'original_title', 'votes', 123445, 'score', 7.0)
    user_movie = "iron+man"
    get_hyperlink(user_movie)
    parent_node_key = create_parent_node(G, soup)

    movies_visited = []
    get_info(G, soup, rows_deep, count, movies_visited, parent_node_key)

    return G

def get_hyperlink(movie_name):
    # need to fix exit code later
    try:
        # user_movie = "acyeiouncu"
        temp_r = requests.get("http://www.imdb.com/find?ref_=nv_sr_fn&q=" + movie_name + "&s=all")
        temp_soup = BeautifulSoup(temp_r.content, "lxml")

        link = temp_soup.find("td", class_="result_text")
        link = link.find('a')
        link = link.get("href")
        link = "http://www.imdb.com" + link
        print(link)
        return link

    except:
        print("Error : Movie was not found.")
        exit(0)
'''
if __name__ == "__main__":
    scraper(hyperlink)
'''








