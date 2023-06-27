from flask import Flask, flash, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import UserMixin, LoginManager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, static_url_path='/static')



base_dir = os.path.dirname(os.path.realpath(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
    os.path.join(base_dir, 'chris_blog.db')
app.config["SQLACLHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'you-will-never-guess1315123'

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    
def __repr__(self):
    return f"User <{self.username}>"

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), unique=False, nullable=False)
    author = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f"Article <{self.title}>"
    
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String, nullable=False)
    priority = db.Column(db.String(20))
        
    def __repr__(self):
            return f"Message: <{self.title}>"
        
with app.app_context():
    db.create_all()
        
@app.route('/')
def index():
    articles = Article.query.all()
    context = {
        "articles": articles
    }
    return render_template('practice.html',title='Home', **context)
    
@app.route('/about')
def about():
    return render_template('about.html', title="About")
    
@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        sender = request.form.get('name')
        email = request.form.get('email')
        title = request.form.get('title')
        message = request.form.get('message')
        priority = request.form.get('priority')
            
        new_message = Message(sender=sender, email=email,
        title=title, message=message, priority=priority)
        
        db.session.add(new_message)
        db.session.commit()
        
        flash("Message sent. Thanks for reaching out!")
        return redirect(url_for('index'))
    
    return render_template('contact.html')

login_manager = LoginManager(app)

@app.route('/signup', methods=["GET", "POST"])
def register():
    if request.method=="POST":
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        username_exits = User.query.filter_by(
            username=username).first()
        if username_exits:
            flash("This username already exists!")
            return redirect(url_for('register'))
        
        email_exits = User.query.filter_by(
            email=email).first()
        if email_exits:
            flash("This email is already registered!")

        password_hash = generate_password_hash(password)

        new_user = User(username=username, first_name=first_name, last_name=last_name,
                        email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("You have signed up successfully!")
        return redirect(url_for('login'))
    
    return render_template('practice.html', title='Home')


if __name__ == '__main__':
    app.run(debug=True)
            
