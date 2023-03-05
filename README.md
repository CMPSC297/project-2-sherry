# Book Review Website
This simple web application allows users to search for books, view book details, and write reviews. Below is a breakdown of the tools used for the project as well as descriptions on each project file:

**Programming Languages**: Python, SQL

**Framework/Libraries**: Flask, SQLAlchemy

**Database**: PostgreSQL

## Descriptions of each file:

**application.py:** Main application file that contains the Flask routes and view functions.

**import.py:** Opens and reads book.csv and imports all books into the database table books. 

**sampleAPI.py:** Utilized the Google Books API to extract information on specific books. The API was used to find the average rating and number of ratings. In addition, the API was also used to create a JSON object containing relevant information on a book. 

**queries.sql:** Defines the schema for creating the tables in the database. Consists of three tables: books, users, and reviews.

**api.html:** Displays the information of a book extracted from Google Books API. 

**base.html:** Provides the basic Flask layout for the rest of the HTML files.

**book.html:** Displays all information about a book and its reviews and provides users a text area to submit their reviews as well.

**error.html:** Shows an error message, indicating the user's review cannot be added because the user already has a review for the book.

**index.html:** First page of the application. Allows users to register an account.

**login.html:** Login page.

**search.html:** Utilities are provided where users are able to search for a book by either ISBN, title, or author.

**success.html:** Shows success message, indicating the user's review has successfully been added to the database

**main.css:** Contains the CSS for the application


## Note
For displaying the existing reviews for a book, I had issues with the formatting. I could not figure out how to remove the parentheses and the comma. 
