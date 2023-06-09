
import movie_storage

menu = """_____MENU_____________________________________________________________________
0. Exit                 1. List movies          2. Add movie
3. Delete movie         4. Update movie         5. Stats
6. Random movie         7. Search movie         8. Movies sorted by rating
9. Generate website     10. Favorite movie      11. Movie histogram
______________________________________________________________________________
"""

def my_choice(word):
    if word == 1:
        movie_storage.list_movies()
    elif word == 2:
        movie_storage.add_movie()
    elif word == 3:
        movie_storage.delete_movie()
    elif word == 4:
        movie_storage.update_movie()
    elif word == 5:
        movie_storage.stats_movie()
    elif word == 6:
        movie_storage.random_movie()
    elif word == 7:
        movie_storage.search_movie()
    elif word == 8:
        movie_storage.sort_movies()
    elif word == 9:
        movie_storage.generate_web()
        print('Enjoy index.html! Thank you')
    elif word == 10:
        movie_storage.favorite_movies()
        print('Enjoy index.html! Thank you')
    elif word == 11:
        movie_storage.movies_histogram()
    else:
        print("Over limited")


def main():
    print(menu)
    while True:
        choice = input("Enter choice (0-11): ")
        if choice == '0':
            print("Bye!")
            break

        try:
            choice = int(choice)
            if 0 < choice < 12:
                my_choice(choice)
            else:
                print("Invalid choice. Please enter a number between 0 and 11.")
        except ValueError:
            print("Invalid choice. Please enter a number between 0 and 11.")

        button = input('Continue (Y/N)? : ')
        if button.upper() != "Y":
            print("Thank you!")
            break



if __name__ == "__main__":
    main()