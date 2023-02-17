# Lab 1

ENGO 551

Creators: Mark De Guzman
          Tyson Toews
          
For this lab, users are able to register and login using a username and password that is then stored to the database in the "Users" table. 
While on the index of the website, a table "Books" is created where it imports the data from the 'books.csv' file onto the database.

The user must be logged in to access the dashboard, search, and book details functions.
Once the user is logged in, they are taken to the dashboard where they are then able to search for any book in the database through a search query using the books isbn, title, author, or year. 
Alongside the search function, the user is also able to leave a review which is then submitted to the database and stored so that when a user is on the book details page, they are able to see the reviews left by other users. 
For a user to access the book details page, they must first make a search query either through the isbn, title, author, or year, and once redirected to book details page, they are able to view the current isbn, title, author, and publication year of the book selected as well as any of the reviews from other users.
When the user is finished with the search or book details functions, they are able to log out and will be redirected back to the main index of the website.


*Folder items
```
/static
dashboard.css : css styling when the user is logged in
sign in : css styling when the user is logged out

/templates
author.html : html code for author search query
base.html : html template for when the user is logged out
base1.html : html template for when the user is logged in
book.html : html code for book details
dashboard.html : html code for landing page after user logs in
error.html : html template for registration or login errors
index.html : html code for website main landing page
isbn.html : html code for isbn search query
login.html : html code for user login
register.html : html code for user registration
search.html : html code for search landing page
title.html : html code for title search query
year.html : html code for year search query
```




