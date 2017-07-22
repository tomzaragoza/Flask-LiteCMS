import datetime
import re
import urllib.parse
import bcrypt
from flask import (Flask, flash, Markup, redirect, render_template,
				   request, session, url_for)
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *
from flask_wtf.csrf import CSRFProtect, CSRFError


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object('config')
flask_db = FlaskDB(app)
database = flask_db.database
if 'RESUME_FILENAME' not in app.config:
    app.config['RESUME_FILENAME'] = ''


class Entry(flask_db.Model):
	title = CharField()
	slug = CharField(unique=True)
	content = TextField()
	published = BooleanField(index=True)
	timestamp = DateTimeField(default=datetime.datetime.now, index=True)

	@property
	def html_content(self):
		hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
		extras = ExtraExtension()
		markdown_content = markdown(self.content, extensions=[hilite, extras])
		return Markup(markdown_content)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = re.sub('[^\w]+', '-', self.title.lower()).strip('-')
		return super(Entry, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		q = super(Entry, self).delete().where(Entry.slug == self.slug)
		q.execute()
		return

	@classmethod
	def public(cls):
		return Entry.select().where(Entry.published == True)

	@classmethod
	def drafts(cls):
		return Entry.select().where(Entry.published == False)


@app.route('/login/', methods=['GET', 'POST'])
def login():
	next_url = request.args.get('next') or request.form.get('next')
	if request.method == 'POST' and request.form.get('password'):
		password = str.encode(request.form.get('password'))
		if bcrypt.checkpw(password, app.config['PW_HASH']):
			session['logged_in'] = True
			session.permanent = True
			flash('You are now logged in.', 'success')
			return redirect(next_url or url_for('index'))
		else:
			flash('Incorrect password.', 'danger')
	return render_template('login.html', next_url=next_url)


@app.route('/logout/')
def logout():
	if not session.get('logged_in'):
		return render_template('404.html'), 404
	session.clear()
	return redirect(url_for('index'))


@app.route('/')
def index():
	query = Entry.public().order_by(Entry.timestamp.desc())
	return object_list('index.html', query, check_bounds=False)


@app.route('/about/')
def about():
	return render_template('about.html')


@app.route('/' + app.config['RESUME_FILENAME'])
def resume():
    if app.config['RESUME_FILENAME'] == '':
        return render_template('404.html'), 404
    else:
        return app.send_static_file(app.config['RESUME_FILENAME'])


def _create_or_edit(entry, template):
	if request.method == 'POST':
		entry.title = request.form.get('title') or ''
		entry.content = request.form.get('content') or ''
		entry.published = request.form.get('published') or False

		if not (entry.title and entry.content):
			flash('Title and Content are required.', 'danger')
		else:
			try:
				with database.atomic():
					entry.save()
			except IntegrityError:
				flash('Error: This title is already in use.', 'danger')
			else:
				flash('Entry saved successfully.', 'success')
				if entry.published:
					return redirect(url_for('detail', slug=entry.slug))
				else:
					return redirect(url_for('edit', slug=entry.slug))

	return render_template(template, entry=entry)


@app.route('/create/', methods=['GET', 'POST'])
def create():
	if not session.get('logged_in'):
		return render_template('404.html'), 404
	return _create_or_edit(Entry(title='', content=''), 'create.html')


@app.route('/drafts/')
def drafts():
	if not session.get('logged_in'):
		return render_template('404.html'), 404
	query = Entry.drafts().order_by(Entry.timestamp.desc())
	return object_list('drafts.html', query, check_bounds=False)


@app.route('/<slug>/')
def detail(slug):
	if session.get('logged_in'):
		query = Entry.select()
	else:
		query = Entry.public()
	entry = get_object_or_404(query, Entry.slug == slug)
	return render_template('detail.html', entry=entry)


@app.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
	if not session.get('logged_in'):
		return render_template('404.html'), 404
	entry = get_object_or_404(Entry, Entry.slug == slug)
	return _create_or_edit(entry, 'edit.html')


@app.route('/<slug>/delete/', methods=['GET', 'POST'])
def delete(slug):
	if not session.get('logged_in') or request.method == 'GET':
		return render_template('404.html'), 404
	entry = get_object_or_404(Entry, Entry.slug == slug)
	with database.atomic():
		entry.delete()
		flash('Post deleted.', 'warning')
	return redirect(url_for('index'))


@app.template_filter('clean_querystring')
def clean_querystring(request_args, *keys_to_remove, **new_values):
	querystring = dict((key, value) for key, value in request_args.items())
	for key in keys_to_remove:
		querystring.pop(key, None)
	querystring.update(new_values)
	return urllib.parse.urlencode(querystring)


@app.errorhandler(404)
def not_found(exc):
	return render_template('404.html'), 404


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
	return render_template('400_csrf_error.html'), 400


def main():
	database.get_conn()
	database.create_tables([Entry], safe=True)
	database.close()
	app.run(debug=True)


if __name__ == '__main__':
	main()