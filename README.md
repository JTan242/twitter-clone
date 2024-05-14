# Final Project
[![Tests](https://github.com/jtan242/final-project/workflows/tests/badge.svg)](https://github.com/jtan242/final-project/actions?query=workflow%3Atests)

## Overview 
This project is inspired by the architecture of Instagram to create a Twitter-like, database-backed webpage from scratch.

## Techstack
 - Python: Utilized for backend development
 - Flask: micro web framework employed for handling server-side logic
 - HTML/CSS: Used for front-end design and styling
 - Jinja2: Templating engine for rendering dynamic content
 - PostgreSQL: A templating engine that facilitates the rendering of dynamic content
 - Docker: Utilized for containerizing the application, enhancing both development and production environments
 - Nginx:  Serves as both a high-performance web server and a reverse proxy
 - Gunicorn: A WSGI HTTP server for managing web server requests

## Database
The database consists of 3 tables within Postgres: users, tweets, and url
### urls
- id_urls
- url
### users
- id_users
- username
- password
### tweets
- id_tweets
- id_users
- text
- created_at
- id_url
Within these tables, a scipt is employed to input random strings into each of the tables

## Functionality 

This project replicates Twitter's CRUD (Create, Read, Update, Delete) functionality. The webpage features seven functional endpoints, each dedicated to handling a specific task

**Home Page**
 - Visible whether the user is logged in or not logged in
 - Displays the most recent 20 tweets, with a link at the bottom that leads to previous messages
 - Each tweet includes the username that created it, the time of creation, and the message contents

 **Login**
  - This page is only visible if the user is not logged in
  - Prompts the user to enter their username/passwords
  - Validates the credentials by displaying error messages

**Logout**
 - This page is only visible if the user is logged in
 - Deletes the cookies that the login form creates, logging the user out

**Create Account**
 - This page is only visible if the user is not logged in
 - Prompts the user to input a new username/passwords
 - Displays an error if both password inputs don't match or username has been taken

**Create Message**
 - This page is only visible if the user is logged in
 - Lets the user enter whatever message body they want, and creates a tweet with the accurate time of creation

**Search**
 - This page is always visible
 - User inputs a search query into the input field, which uses a FTS over all tweet contents in the databse, and returns results in order of recentness

## Indexes 
Our database consists of tables with over a million rows of inputs. To make our queries process quickly, indexes were made on each table. An important index for our database was the RUM index on the message contents within our tweets table, which allowed for our FTS in the search funtionality to be proccessed fast.


## Build Instructions
To bring up the services follow run the following commands:

To build the and run the development containers we run:
```
$ docker-compose up -d --build
```
We can access our webpage at http://localhost:2425/

To stop the current container we run:
```
$ docker-compose down 
```
Before proceeding to the production server, a ```.env.prod.db``` text file containing your database credentials must be included in the project root.

To build and run the production containers we run: 
```
$ docker-compose -f docker-compose.prod.yml up -d --build
```
We access our webpage with the same link:  http://localhost:2425/


