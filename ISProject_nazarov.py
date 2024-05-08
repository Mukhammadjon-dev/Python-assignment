import csv #This library is used to work with CSV files
import re #This library is used to work with regular expressions
import requests #This library is usedto fitch online file to Python file.
import pytz #This library is used to detect current time
from datetime import datetime #This library is used to work with time and date

#<<<<<<<<<<< Step-1 CODES ARE BELOW >>>>>>>>>>>>>>

#This function logic removes year from the movie titles, and gives the years separately.
def remove_year_from_title(title):
    year_pattern = r'\(\d{4}\)'
    match = re.search(year_pattern, title) #This logic filters title and remove year from the title
    if match:
        year = match.group().strip('()')
        title_without_year = title.replace(match.group(), '').strip()
        return title_without_year, year
    else:
        return title, None

#This function below reads and generates the first 10 movie details from the file.
def read_generate_ten_movies(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #This helps to skip the header of the table
        movies = []
        for i, row in enumerate(csv_reader):
            if i < 10: # This logic generates only the first 10 movies. It gives only movieId and title
                movieId, title, _ = row
                title_without_year, year = remove_year_from_title(title)
                movies.append([movieId, title_without_year, year or 'N/A'])
            else:
                break
        return movies

#This function below writes the first 10 movie details into new file named yoursurname.csv.
def write_new_csv_file(file_path, data):
   with open(file_path, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['MovieID', 'Title', 'Year'])
        for row in data:
            csv_writer.writerow(row)

#<<<<<<<<<<< Step-1 CODES ARE ABOVE >>>>>>>>>>>>>>

#<<<<<<<<<<< Step-2 CODES ARE BELOW >>>>>>>>>>>>>>

#This logic fetiching the data from the online file
def access_onlinefile_data(url):
    response = requests.get(url)
    response.raise_for_status() #This shows error if fetching fails
    content = response.text
    # The logic below converts the fetched content to a list of lists (rows)
    data = [row.split(',') for row in content.split('\n') if row]
    return data

#The logic below appends the online data to the file starting from the end of the document.
def append_data_to_csv(file_path, data, start_movie_id):
    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        for row in data[1:]:  # This skips the header row from the online file
            movie_id = start_movie_id
            csv_writer.writerow([movie_id] + row)
            start_movie_id += 1 #This generates MovieIDs for new added movies, assuming the lastMovieID was 10

#<<<<<<<<<<< Step-2 CODES ARE ABOVE >>>>>>>>>>>>>>

#<<<<<<<<<<< Step-3 CODES ARE BELOW >>>>>>>>>>>>>>

#This logic helps to detect current time in Europe/Berlin time zone.
def get_current_time():
    timezone = pytz.timezone("Europe/Berlin")
    return datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

#This function adds User-provided Title and data-retrieved time to CSV
def add_title_and_time_to_csv(output_file):
    title = input('Enter a title for the output file: ')
    current_time = get_current_time() #This line of code generates actual date and time for newly appended movies
    with open(output_file, 'r+', encoding='utf-8') as file:
        content = file.read()
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"{title.strip()}\n\nData Retrieved on: {current_time}\n\n{content}")


#Main Function. This function orchestrates the flow of the program by calling each function at the appropriate time.
def main():

    #Call functions for Step-1
    movies_list = 'movies.csv'
    output_file = 'nazarov_output.csv'

    movies_data = read_generate_ten_movies(movies_list)
    write_new_csv_file(output_file, movies_data)

    #Call functions for Step-2
    online_data = access_onlinefile_data("http://pythonscraping.com/files/MontyPythonAlbums.csv")

    #Append data to CSV file
    append_data_to_csv('nazarov_output.csv', online_data, start_movie_id=11)

    #Call functions for Step-3
    add_title_and_time_to_csv(output_file)

if __name__ == "__main__":
    main()


#<<<<<<<<<<< Step-3 CODES ARE ABOVE >>>>>>>>>>>>>>
