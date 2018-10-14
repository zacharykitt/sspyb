import glob
import json

from flask import Flask, render_template

app = Flask(__name__)

def aggregate_posts():
    posts = []
    for path in glob.glob('posts/*.json'):
        with open(path) as f:
            posts.append(json.load(f))
    return posts

@app.route('/')
def index():
    posts = aggregate_posts()
    return render_template('index.html', posts=posts)
