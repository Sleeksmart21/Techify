from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from datetime import datetime
import os

app = Flask(__name__)

base_dir = os.path.dirname(os.path.realpath(__file__))

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///' + os.path.join(base_dir,'blog.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '026b0eb800ec2934fb5cf2e7'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class Blog(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    post = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"User <{self.username}>"

# with app.app_context():
    # db.init_app(app)
    # db.create_all()

# @app.route('/')
# def index():
    # users = User.query.all('username')
    # return render_template('index.html')

@app.route('/')
def blog():
    blogs = Blog.query.all()
    return render_template('index.html', blogs=blogs)


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id):
    post = Blog.query.get_or_404(id)
   
    if post.author != current_user.first_name:
        flash('You have to login to edit a Post')

        return redirect(url_for('blog'))

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.post = request.form.get('post')
        post.date_posted = datetime.now()
        db.session.commit()

        return redirect(url_for('blog'))

    return render_template('edit.html', post=post)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(id):
    post = Blog.query.get_or_404(id)
    if post.author != current_user.first_name:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post successfully deleted')
        return redirect(url_for('blog'))


@app.route('/signup', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(url_for('register'))

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            return redirect(url_for('register'))
        
        password_hash = generate_password_hash(password)

        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('signup.html')


@app.route('/login', methods=['POST','GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return redirect(url_for('blog'))

    return render_template('login.html')


@app.route('/post', methods=['POST', 'GET'])
@login_required
def post():
    if post.author != current_user.first_name:

        flash('You have to login to edit a Post')

    return redirect(url_for('blog'))


    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('post')
        author = current_user.first_name
        date_posted = datetime.now()
        new_post = Blog(title=title, post=content, author=author, date_posted=date_posted)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('blog'))

    return render_template('create_post.html')


@app.route('/create_post')
def create_post():
    return render_template('create_post.html')



@app.route('/post/<int:id>', methods=['POST', 'GET'])
def read_more(id):
    post = Blog.query.get_or_404(id)
    return render_template('read_more.html', post=post)

        
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# @app.route('/protected')
# @login_required
# def protected():
    # return render_template('protected.html')
    

if __name__=="__main__":
    app.run(debug=True)