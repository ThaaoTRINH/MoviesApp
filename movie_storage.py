import requests
import json
import statistics
import random
from collections import OrderedDict
from operator import getitem
import matplotlib.pyplot as plt


file_source = "data.json"


def get_data():
    with open(file_source, "r") as handle:
        datas = json.loads(handle.read())
    return datas

def save_to_json(movies):
    new_data = json.dumps(movies)
    with open("data.json", "w") as handle:
        handle.write(new_data)

movies = get_data()
length = len(movies)
def list_movies():
    datas = get_data()
    n = 1
    for i in range(len(datas)):
        for key, value in datas[i].items():
            print(f'{n}. {key.upper()} | Rating: {datas[i][key]["rating"]} | Actors: {datas[i][key]["actors"]}')
            n += 1

def check_movie_exist():
    movie_name_list = []
    for i in range(len(movies)):
        for key, value in movies[i].items():
            movie_name_list.append(key)
    while True:
        title = input("Enter a name of movie: ")
        if title.upper() not in movie_name_list:
            print(f'The movie {title.upper()} does not exist')
        else:
            break
    return title

def input_movie():
    while True:
        movie_title = input("Add a movie title: ")
        if not movie_title:
            print('Movie title is required! ')
            continue
        try:
            movie_title.upper()
        except ValueError:
            print('Invalid! Input again pls')
            continue

        return movie_title

def add_movie():
    title = input_movie()
    movie = {}
# Search title from https://www.omdbapi.com and add on "year release" and others info
    for i in range(len(movies)):
        for key, value in movies[i].items():
            if title.upper() in key.upper():
                print(f'Movie {title.upper()} was already exist')
                return input_movie()

    url = 'https://www.omdbapi.com/?apikey=99b0f16a&t=' + f'{title}'
    data = requests.get(url)
    data = data.json()
    if title.upper() == data['Title'].upper():
        title = data['Title'].upper()
        year_release = data['Year']
        rating = data['imdbRating']
        director = data['Director']
        actors = data['Actors']
        awards = data['Awards']
        genre = data['Genre']
        content = data['Plot']

        movie[title] = {
            'year': year_release,
            'rating': rating,
            'director': director,
            'actors': actors,
            'awards': awards,
            'genre': genre,
            'content': content,
        }
    movies.append(movie)
    save_to_json(movies)
    print(f'Movie {title} successfully added')
    print("-----------------")

def delete_movie():
    print('----- DELETE A MOVIE -----')
    title = check_movie_exist()

    for i in range(len(movies)):
        for key, value in movies[i].items():
            if title.upper() == key:
                del movies[i]

    save_to_json(movies)
    print(f'Movie {title} already deleted')
    print("-----------------")

def update_movie():
    print('----- UPDATE A MOVIE -----')
    title = check_movie_exist()
    try:
        new_rating = float(input("Enter a new rating: "))
    except ValueError:
        print('Invalid number" Try again!')
        return

    for i in range(len(movies)):
        for key, value in movies[i].items():
            if title.upper() == key:
                value['rating'] = new_rating

    save_to_json(movies)
    print(f'A new rating of movie {title.upper()} already updated')
    print("-----------------")


def stats_movie():
    rating_list = []
    for i in range(length):
        for key, value in movies[i].items():
            rating_list.append(float(value['rating']))

    print(f'Average rating: {round(sum(rating_list)/length,2)}')
    print(f'Median rating: {statistics.median(rating_list)}')
    print(f'Highest rating: {max(rating_list)}')
    print(f'Lowest rating: {min(rating_list)}')

def random_movie():

    i = random.randint(0, length-1)
    for key, value in movies[i].items():
        print(f"Your movie for tonight: '\033[1m'\033[96m{key.upper()}. It's rated {value['rating']}'\033[0m\033[00m'"
              f"\nActors: {value['actors']} \n'\033[3m {value['content']}")

def search_movie():
    print('SEARCH MOVIE')
    movie_name = input("Enter movie name (enter for skip) : ")
    movie_rating = 0
    while True:
        movie_rating_input = input("Enter rating (enter for skip) : ")
        if movie_rating_input == '':
            break
        try:
            movie_rating = float(movie_rating_input)
            break
        except ValueError:
            print('Invalid! Re-enter: ')
    movie_actor = input("Enter actor (enter for skip) : ")
    movie_director = input("Enter director (enter for skip) : ")
    movie_genre = input("Enter movie genre (enter for skip) : ")
    print('--------------------------------------------------------------------------------------')
    for i in range(length):
        for key, value in movies[i].items():
            display = f'{key.upper()} was release in {value["year"]} and rating is {value["rating"]} \n' \
                      f'. Director: {value["director"]} | Actors: {value["actors"]}'
            if key.upper() == movie_name.upper():
                print(display)
            elif (movie_rating != 0) and (float(value["rating"]) >= movie_rating):
                print(display)
            elif movie_actor and (movie_actor.upper() in value['actors'].upper()):
                print(display)
            elif movie_director and (movie_director.upper() in value['director'].upper()):
                print(display)
            elif movie_genre and (movie_genre.upper() in value['genre'].upper()):
                print(display)
    print('--------------------------------------------------------------------------------------')

def sort_movies():
    sorted_movie = sorted(movies, key=lambda x: x[list(x.keys())[0]]['rating'], reverse=True)
    print('--------------------------------------------------------------------------------------')
    print('SORT MOVIES BY THE RATING :')
    print('--------------------------------------------------------------------------------------')
    n = 1
    for i in range(length):
        for key, value in sorted_movie[i].items():
            print(f'{n}. {key.upper()} | Rating: {value["rating"]} | Actors: {value["actors"]}')
            n += 1

def poster_search(movie_name):
    poster_link = ''
    url = 'https://www.omdbapi.com/?apikey=99b0f16a&t='+f'{movie_name}'
    data = requests.get(url)
    data = data.json()
    if movie_name.upper() in data['Title'].upper():
        poster_link = data['Poster']

    return poster_link

def generate_web():
    list_movies()
    output_list = []
    for i in range(length):
        for key, value in movies[i].items():
            output = ' '
            output += '<li>'
            output += '<div class ="movie">'
            output += f'<img class ="movie-poster" src = "{poster_search(key.lower())}" title = ""/>'
            output += f'<div class ="movie-title"> {key} </div>'
            output += f'<div class ="movie-year"> {value["year"]} </div>'
            output += f'<div class ="star">*</div>'
            output += f'<div class ="movie-year">(rating: {value["rating"]})</div>'

            output += '</div>'
            output += '</li>'
            output_list.append(output)

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
    movie_name_list = []
    favorite_list = []
    favorite_name = ''
    n = 1
    for i in range(length):
        for key, value in movies[i].items():
            movie_name_list.append(key)
            print(f'{n}. {key}')
            n += 1

    while True:
        movie_number_input = input("Enter your favorite movie # (press enter to skip): ")
        if movie_number_input == '':
            break
        else:
            movie_number = int(movie_number_input)
            favorite_list.append(movie_name_list[movie_number - 1].upper())

    output_list = []
    for i in range(length):
        for key, value in movies[i].items():
            if key.upper() in favorite_list:
                favorite_name_movie = "&#11088;"
            else:
                favorite_name_movie = " "
            output = ' '
            output += '<li>'
            output += '<div class ="movie">'
            output += f'<img class ="movie-poster" src = "{poster_search(key)}" title = ""/>'
            output += f'<div class ="movie-title"> {key} </div>'
            output += f'<div class ="movie-year"> {value["year"]} </div>'
            output += f'<div class ="movie-year">( rating: {value["rating"]} )</div>'
            output += f'<span class="favorite-movie">{favorite_name_movie}</span>'
            output += '</div>'
            output += '</li>'
            output_list.append(output)

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

def movies_histogram():
    movie_rating_list = []
    for i in range(length):
        for key, value in movies[i].items():
            movie_rating_list.append((key, value['rating']))
    movie_names = [movie[0] for movie in movie_rating_list]
    ratings = [movie[1] for movie in movie_rating_list]

    fig, ax = plt.subplots()
    ax.bar(movie_names, ratings, color='lightblue')
    plt.xticks(rotation=90, ha="right")
    plt.xlabel("Movie Title", fontsize=12, fontweight='bold')
    plt.ylabel("Rating", fontsize=12, fontweight='bold')
    plt.title("MOVIE AND RATING HISTOGRAM", fontsize=18, fontweight='bold', color='skyblue')

    filename = input("Enter a filename for the histogram: ")
    filetype = input("which filetype (jpeg, jpg) for the histogram ? ")
    if filetype in "eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff":
        file_name = filename + "." + filetype
        plt.savefig(file_name)
        plt.tight_layout()
        plt.show()
        return movies
    raise ValueError("Unsupported Format")
