from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(25), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f'Blog post f{self.id} created!'

all_post = [
    {
        'title': 'Post 1',
        'content': 'This the content',
        'author': 'David'
    },
    {
        'title': 'Post 2',
        'content': 'This the content again',
        'author': 'David part 2'
    }
]

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/post', methods=['GET', 'POST'])
def post():

    if request.method  == 'POST':
        post_tit = request.form['title']
        post_con = request.form['content']
        Author = request.form['author']
        new = BlogPost(title=post_tit, content=post_con, author=Author)
        db.session.add(new)
        db.session.commit()
        return redirect('/post')
    else:
        all_post = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('post.html', post=all_post)

@app.route('/onlyg', methods=['GET', 'POST'])
def getr():
    return 'You can only get this webpage'

@app.route('/post/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/post')

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':

        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/post')
    else:
        return render_template('edit.html',post=post)

@app.route('/create')
def create():
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run(debug=True)