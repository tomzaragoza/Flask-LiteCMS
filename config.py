# This will be your Flask web app's configuration file

# For most beginner users, configuring this file
# will be all that's needed, aside from deploying the
# web app to a web host.

# After configuring this file, check these instructions
# for deploying to a web host:
# http://flask.pocoo.org/docs/0.12/deploying/

# Instructions to deploy Flask web app to pythonanywhere.com
# (which is a beginner-friendly and cheap web host)
# https://help.pythonanywhere.com/pages/Flask/

import os

# For most beginner users, these default values will work
# and do not have to be changed.
APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'db/site.db')
DEBUG = False

# Put your name in between the quotes
YOUR_NAME = ''

# Generate a hash of a password using bcrypt.
# Instructions: https://pypi.python.org/pypi/bcrypt/3.1.0
PW_HASH = b''

# Secret key used by Flask to determine whether you are logged in
# Also used by Flask to protect against CSRF
# Generate a secret key using python's os.urandom()
SECRET_KEY = b''

# Put your resume in the folder named static
# Put the filename of the resume in between the quotes
RESUME_FILENAME = ''

# To edit your about page, edit templates/about.html
# To edit your homepage header, edit templates/index.html

# Optional:
# Put your github and linkedin links in between the quotes
# You may leave them blank if you don't have GitHub/LinkedIn
# These buttons are in the about page
GITHUB_LINK = ''
LINKEDIN_LINK = ''

# Optional:
# Place a favicon named favicon.ico in the folder named static
# What is a favicon? https://en.wikipedia.org/wiki/Favicon