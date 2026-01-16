from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    author = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    download_link = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(300), nullable=False)


@app.route('/')
def index():
    return render_template("home.html")

@app.route("/Register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("register.html")

@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('area'))
        else:
            return "Invalid credentials", 401
    return render_template("login.html")

@app.route("/Area", methods=["GET",])
def area():
    return render_template("main.html", users = [user.username for user in User.query.all()], books = book.query.all())

@app.route("/Publish", methods=['GET', 'POST'])
def publish():
    if request.method == "POST":
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')
        isbn = request.form.get('isbn')
        download_link = request.form.get('download_link')
        image = request.form.get('image')
        new_book = book(title=title, author=author, year=year, isbn=isbn, download_link=download_link, image=image)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('area'))
    return render_template("publish.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)