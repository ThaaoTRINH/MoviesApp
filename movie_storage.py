import requests
import json
import statistics
import random
from collections import OrderedDict
from operator import getitem


file_source = "data.json"

def get_data():
    with open(file_source, "r") as handle:
        datas = json.loads(handle.read())
    return datas

def save_to_json(movies):
    new_data = json.dumps(movies)
    with open("data.json", "w") as handle:
        handle.write(new_data)

def list_movies():

    datas = get_data()

    i = 1
    print(f'There are {len(datas)} in the list:')
    for key, value in datas.items():
        print(f'{i}. {key} (Rating: {datas[key]["rating"]})')
        i += 1

def add_movie():
    """
    Adds a movie to the movies-database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """

    def input_movie():

        movie_title = input("Add a movie: ")
        movie_year = int(input("Enter a year of the movie release: "))
        movie_rating = float(input("add the rating: "))
        return movie_title, movie_year, movie_rating

    title, year, rating = input_movie()
    movies = get_data()

    if title in movies:
        print(f'Movie {title} already exist')
        return input_movie()
    else:
        movies[title] = {
            "year": year,
            "rating": rating
        }
# save new data to JSON file
    save_to_json(movies)

    print(f'Movie {title} successfully added')
    print("-----------------")

def delete_movie():
    """
    Deletes a movie from the movies-database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_data()
    title = input("Enter a movie to delete: ")
    if title not in movies:
        print(f'The movie {title} does not exist')
        title = input("Enter a movie to delete: ")
    else:
        del movies[title]

    # save new data to JSON file
    save_to_json(movies)
    print(f'Movie {title} already deleted')
    print("-----------------")

def update_movie():
    """
    Updates a movie from the movies-database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_data()
    title = input("Enter a name of movie: ")
    new_rating = float(input("Enter a new rating: "))
    if title not in movies:
        print(f'The movie {title} does not exist')
        title = input("Enter a movie to delete: ")
    else:
        movies[title]['rating'] = new_rating

# save new data to JSON file
    save_to_json(movies)
    print(f'A new rating of movie {title} already updated')
    print("-----------------")

def stats_movie():
    movies = get_data()

    rating_sum = 0
    rating_list = []

    for key, value in movies.items():
        rating_sum += (movies[key]['rating'])
        rating_list.append(movies[key]['rating'])
    print(f'Average rating: {rating_sum/len(movies)}')
    print(f'Median rating: {statistics.median(rating_list)}')
    print(f'Highest rating: {max(rating_list)}')
    print(f'Lowest rating: {min(rating_list)}')

def random_movie():
    movies = get_data()
    key, val = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {key.upper()}. It's rated {val['rating']}")

def search_movie():
    movies = get_data()
    movie_name = input("Enter a movie: ")
    for key, value in movies.items():
        if key == movie_name:
            print(f'{key.upper()} was release in {value["year"]} and rating is {value["rating"]}')

def sort_movies():
    movies = get_data()

    res = OrderedDict(sorted(movies.items(), key=lambda x: getitem(x[1], 'rating'), reverse=True))
    # res = sorted(movies.items(), key=lambda x: x[1]['rating'])
    for key, value in res.items():
        print(key, ':', value)

def poster_search(movie_name):
    poster_link = ''
    url = 'https://www.omdbapi.com/?apikey=99b0f16a&t='+f'{movie_name}'
    data = requests.get(url)
    data = data.json()
    if movie_name == data['Title']:
        poster_link = data['Poster']

    return poster_link

def generate_web():
    list_movies()
    output_list = []
    movies = get_data()

    for key, value in movies.items():
        output = ' '
        output += '<li>'
        output += '<div class ="movie">'
        output += f'<img class ="movie-poster" src = "{poster_search(key)}" title = ""/>'
        output += f'<div class ="movie-title"> {key} </div>'
        output += f'<div class ="movie-year"> {movies[key]["year"]} </div>'
        output += f'<div class ="movie-year">( rating: {movies[key]["rating"]} )</div>'
        output += '</div>'
        output += '</li>'
        output_list.append(output)
    # print(output_list)

    outfile_name: str = 'index.html'
    html_head = """
            <html>
            <head>
                <title>My Movie App</title>
            <link rel="stylesheet" href="style.css"/>
            </head>
            <body>
            <div class="list-movies-title">
                <h1>My Movie App</h1>
            </div>
            <div>
                <ol class="movie-grid">
            """

    html_end = """

                </ol>
            </div>
            </body>
            </html>"""

    export_file = open(outfile_name, 'w')
    export_file.write(html_head)
    for movie in output_list:
        export_file.write(str(movie))
    export_file.write(html_end)
    export_file.close()

def favorite_movies():
    list_movies()

    favorite_list =[]
    favorite_name = ''
    while favorite_name.upper() != 'Q':
        favorite_name: str = input("Enter your favorite movie or Q to quit: ")
        favorite_list.append(favorite_name.upper())

    #print(favorite_list)
    output_list = []

    movies = get_data()
    for key, value in movies.items():
        if key.upper() in favorite_list:
            favorite_name_movie = "&#11088;"
        else:
            favorite_name_movie = " "
        output = ' '
        output += '<li>'
        output += '<div class ="movie">'
        output += f'<img class ="movie-poster" src = "{poster_search(key)}" title = ""/>'
        output += f'<div class ="movie-title"> {key} </div>'
        output += f'<div class ="movie-year"> {movies[key]["year"]} </div>'
        output += f'<div class ="movie-year">( rating: {movies[key]["rating"]} )</div>'
        output += f'<span class="favorite-movie">{favorite_name_movie}</span>'
        output += '</div>'
        output += '</li>'
        output_list.append(output)
    # print(output_list)

    outfile_name: str = 'index.html'
    html_head = """
        <html>
        <head>
            <title>My Movie App</title>
        <link rel="stylesheet" href="style.css"/>
        </head>
        <body>
        <div class="list-movies-title">
            <h1>My Movie App</h1>
        </div>
        <div>
            <ol class="movie-grid">
        """

    html_end = """

            </ol>
        </div>
        </body>
        </html>"""

    export_file = open(outfile_name, 'w')
    export_file.write(html_head)
    for movie in output_list:
        export_file.write(str(movie))
    export_file.write(html_end)
    export_file.close()
