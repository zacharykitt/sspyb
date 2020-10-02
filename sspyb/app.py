from datetime import datetime
import glob
import json

from flask import abort, Flask, render_template
import markdown
import yaml

# load custom website settings
with open('config.json') as f:
    config = json.load(f)

theme_dir = config['theme_dir']
base_title = config['base_title']

# init app
app = Flask(__name__)

def parse_yaml(fpath):
    with open(fpath) as f:
        doc = yaml.load(f)
        doc['html'] = markdown.markdown(doc['mark'])
    return doc

def aggregate_posts():
    posts = []
    for path in glob.glob('posts/*.yaml'):
        posts.append(parse_yaml(path))
    posts = sorted(posts,
                   reverse=True,
                   key=lambda x: datetime.strptime(x['date'], '%m/%d/%y'))
    return posts

def aggregate_pages():
    pages = []
    for path in glob.glob('pages/*.yaml'):
        pages.append(parse_yaml(path))
    sorted(pages, key=lambda x: x['slug'])
    return pages

@app.route('/')
def index():
    return render_template(theme_dir + 'index.html',
                           posts=aggregate_posts(),
                           title = base_title)
@app.route('/<slug>')
def page(slug):
    for page in aggregate_pages():
        if page['slug'] == slug:
            title = page['title'] + ' - ' + base_title
            return render_template(theme_dir + 'page.html', page=page)
    abort(404)

@app.route('/posts/<slug>')
def post(slug):
    for post in aggregate_posts():
        if post['slug'] == slug:
            title = post['title'] + ' - ' + base_title
            return render_template(theme_dir + 'post.html', post=post, title=title)
    abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
