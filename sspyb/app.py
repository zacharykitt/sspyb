import glob

import yaml

from flask import abort, Flask, render_template

app = Flask(__name__)

def aggregate_posts():
    posts = []
    for path in glob.glob('posts/*.yaml'):
        with open(path) as f:
            posts.append(yaml.load(f))
    return posts

@app.route('/')
def index():
    return render_template('index.html', posts=aggregate_posts())

@app.route('/posts/<slug>')
def read(slug):
    for post in aggregate_posts():
        if post['slug'] == slug:
            return render_template('post.html', post=post)
    abort(404)
