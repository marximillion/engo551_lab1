# Lab 1

ENGO 551

Creators: Mark De Guzman
Tyson Toews

IMPORTANT:
On first time run through of the application, follow these steps carefully:

In the terminal run the following commands:
python install -r requirements.txt
set FLASK_DEBUG=1
set DATABASE_URL=postgresql://<user>:<password>@localhost/<database_name>

Once the flask application is running successfully, immediately go the database route to create database:
i.e. http://127.0.0.1:5000/database

Once these steps have been followed, the application should run smoothly.

Description [Lab 1]:  
For this lab, users are able to register and login using a username and password that is then stored to the database in the "Users" table.
While on the index of the website, a table "Books" is created where it imports the data from the 'books.csv' file onto the database.

The user must be logged in to access the dashboard, search, and book details functions.
Once the user is logged in, they are taken to the dashboard where they are then able to search for any book in the database through a search query using the books isbn, title, author, or year.
Alongside the search function, the user is also able to leave a review which is then submitted to the database and stored so that when a user is on the book details page, they are able to see the reviews left by other users.
For a user to access the book details page, they must first make a search query either through the isbn, title, author, or year, and once redirected to book details page, they are able to view the current isbn, title, author, and publication year of the book selected as well as any of the reviews from other users.
When the user is finished with the search or book details functions, they are able to log out and will be redirected back to the main index of the website.

Description [Lab 2]:
New Features Added - 02/17/2023
When a user visits the book page, they are able to view the current isbn, title, author, and publication year of the beak, as well as the average ratings and number of ratings from the google api https://www.googleapis.com/books/v1/volumes?q=<isbn>
There are also radio options for the user to choose from between 1 through 5 for a ratings and they are able to leave a comment as well. This review/rating feature is limited to one rating per user, and if a user submits multiple reviews for the same book, an error will be shown.
Alongside the revised book and review features, there is also a hidden route for an api request if you wanted to view the json data of a specific book. Details are in the 'app.py' file in the api function definiton. In short, you specify an isbn and that to the route /api/<isbn> and it returns a page of the raw or parsed json data.

```

*Folder items
/static
dashboard.css : css styling when the user is logged in
sign in : css styling when the user is logged out

/templates
api.html : html code for api request to show json data
[not used] author.html : html code for author search query
base.html : html template for when the user is logged out
base1.html : html template for when the user is logged in
[not used] book.html : html code for book details
book1.html : updated html code for book details
dashboard.html : html code for landing page after user logs in
database.html : html code to show successful creation of database
error.html : html template for registration or login errors
error1.html : html template for review errors
index.html : html code for website main landing page
[not used] isbn.html : html code for isbn search query
login.html : html code for user login
register.html : html code for user registration
search.html : html code for search landing page
[not used] search1.html : html practice code for search functionality
success.html : html code for successful registration landing page
[not used] title.html : html code for title search query
[not used] year.html : html code for year search query

/
app.py : main python flask application code for routes, etc.
books.csv : excel file of the books to import to the database
misc.txt : miscellaneous items
models.py : model creation for required tables and forms and other required imports
requirements.txt : required extensions to run application successfully


```
