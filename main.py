from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password123@localhost:8889/db_blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.String(1024))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def show_blog():
    id = request.args.get('id')
    if id==None:
        blogs = Posts.query.all()
        return render_template('blog.html',bloglist=blogs)
    else:
        return render_template('entry.html', post=Posts.query.get(id), title='My Blog')

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_body']
        title_error = ''
        body_error = ''

        if title == '':
            title_error = 'Your title cannot be blank!'
        if body == '':
            body_error = 'Your blog entry is empty!'
        if title_error == '' and body_error == '':
            post = Posts(title, body)
            db.session.add(post)
            db.session.commit()
            return redirect('/blog')
    else:
        return render_template('new-post.html',title=" build-a-blog")


app.run()