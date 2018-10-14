import glob

import yaml

from flask import Flask, render_template

app = Flask(__name__)

def aggregate_posts():
    posts = []
    for path in glob.glob('posts/*.yaml'):
        with open(path) as f:
            posts.append(json.load(f))
    return posts

@app.route('/')
def index():
    posts = aggregate_posts()
    return render_template('index.html', posts=posts)

@app.route('/posts/<slug>')
def read(slug):
    with open(f'posts/{slug}.yaml') as f:
        post = yaml.load(f)
    return render_template('post.html', post=post)
