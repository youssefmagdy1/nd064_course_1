import sqlite3
import logging
from datetime import datetime


from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)
    

@app.route('/healthz')
def healthz():
  response = app.response_class(
          response=json.dumps({"result":"OK - healthy"}),
          status=200,
          mimetype='application/json'
  )
  return response
  

@app.route('/metrics')
def metrics():

  connection = get_db_connection()
  post_cnt = connection.execute('SELECT COUNT(id)  AS cnt FROM posts').fetchone()
  connection.close()
  response = app.response_class(
          response=json.dumps({"db_connection_count": 1, "post_count": post_cnt['cnt']}),
          status=200,
          mimetype='application/json'
  )
  return response


# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info("["+ dt_string +"]"+ " Article "+ post['title'] +" not found ") 
      return render_template('404.html'), 404
    else:
      app.logger.info("["+ dt_string +"]"+ "Article "+ post['title'] +" retrieved")      
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("["+ dt_string +"]"+  "The about us page was retrieved")      
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            app.logger.info( "["+ dt_string +"]"+"a new article " + title + " has been created ")      
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   logging.basicConfig(level=logging.DEBUG , datefmt='%Y-%m-%d %H:%M:%S')

   app.run(host='0.0.0.0', port='3111')
