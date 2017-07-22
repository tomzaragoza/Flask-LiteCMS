# Flask-LiteCMS

Lightweight, beginner-friendly, and configurable CMS written in Python 3 + Flask 0.12. This CMS is useful for professionals who just want a simple personal website with a blog, an about page, and resume download. Set up and configuration takes less than 30 minutes!

All of the blog posts are Markdown-powered. To read more about Markdown, go to [whatismarkdown.com/](whatismarkdown.com/)

[Sample site](http://www.johnsonshi.com) that runs on Flask-LiteCMS. Flask-LiteCMS is based on [this.](http://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/)

### Installation

* Clone this git repository by running `git clone git@github.com:johnsonshi/Flask-LiteCMS.git` on a terminal
* Install Python 3: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Install pip: [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)
* Install virtualenv: [https://virtualenv.pypa.io/en/stable/installation/](https://virtualenv.pypa.io/en/stable/installation/)
* Activate a virtualenv: [https://virtualenv.pypa.io/en/stable/userguide/](https://virtualenv.pypa.io/en/stable/userguide/)
* Install the required Python 3 libraries by running `pip3 install -r Flask-LiteCMS/requirements.txt` on a terminal

### Configuration and Set Up

* Open Flask-LiteCMS/config.py. This file contains the configurations for your Flask web application.
* Follow the instructions in the file (setting up your resume, filling in your name, your GitHub/LinkedIn links, your password hash, about me page contents, etc.)

### Password Hash Generation

* In order to log in to your site and to manage your blog posts, this web app needs a bcrypt hash of your site admin password (whatever password you like).
* In order to generate a bcrypt password hash, launch a Python 3 interpreter and run the following commands:
``` python
>>> import bcrypt
>>> password = b"PUT YOUR UNHASHED PASSWORD HERE"
>>> hashed = bcrypt.hashpw(password, bcrypt.gensalt())
>>> print(hashed)
b'output_containing_random_characters'
```
* The hash of your password will be outputted as a random string of characters. Copy this (including the letter b at the beginning, as well as the quotes), and paste it in the PW_HASH variable within the Flask-LiteCMS/config.py file.
* Remember your unhashed password. This will be used to log in to your site to manage your blog posts. Keep this a secret!

### Flask Secret Key Generation

* Flask needs a secret key in order to manage your sessions (to determine whether you are logged in to your site as an admin or not), as well as to protect you against CSRF attacks.
* In order to generate a secret key, launch a Python 3 interpreter and run the following commands:
``` python
>>> import os
>>> os.urandom(24)
b'output_containing_random_characters'
```
* Your secret key will be outputted as a random string of characters. Copy this (including the letter b at the beginning, as well as the quotes), and paste it in the SECRET_KEY variable within the Flask-LiteCMS/config.py file.
* You do not have to remember your secret key, but keep it a secret!

### Creating the Database

* Your blog posts will be in a SQLite database. To create the database for the first time, launch a bash terminal, and enter the following commands:
```bash
$ cd Flask-LiteCMS/
$ python3.6 flasksite.py
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
^C (when the site shows the running message, press control C to quit)
```
* Your database would have been created in Flask-LiteCMS/db/ as site.db.

### Running and Testing Locally

* To run the site locally on your machine, launch a bash terminal, and enter the following commands:
```bash
$ cd Flask-LiteCMS/
$ python3 flasksite.py
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
* Launch your browser and go to http://127.0.0.1:5000/

### Deployment

Check out the following links for deployment options:
* [Flask Deployment Documentation](http://flask.pocoo.org/docs/0.12/deploying/)
* [Deploying to pythonanywhere.com](https://help.pythonanywhere.com/pages/Flask/)

### Logging in as Site Admin

* Make sure you've followed the instructions above for generating a password hash and Flask secret key.
* If the Flask web app is run locally, visit http://127.0.0.1:5000/login/ to log in.
* If you've deployed the Flask web app on a webhost, go to http://www.yourdomain.com/login/ to log in.
* Enter your unhashed password.
