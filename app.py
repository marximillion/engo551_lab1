# postgresql://postgres:23081201@localhost/engo551_lab1
# import requests
from models import *
import requests
import json
# from flask_sqlalchemy import SQLAlchemy

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

bootstrap = Bootstrap(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
db.init_app(app)
Session(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.errorhandler(IntegrityError)
def handle_integrity_error(e, message="User already exists. Please Try Again"):
    return render_template("error.html", message=message), 500


@app.route("/database")
def database():
    db.create_all()
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, name, author, year in reader:
        book = Books(isbn=isbn, name=name, author=author,
                     year=year)
        db.session.add(book)
    db.session.commit()
    db.session.close()
    return render_template("database.html")


@app.route("/", methods=['GET'])
def main():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    username = form.username.data
    password = form.password.data
    source = "Registration"

    if form.validate_on_submit():
        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        if new_user.query.filter_by(username=form.username.data).first():
            return render_template("success.html", name=form.username.data)

        try:
            db.session.commit()
            return render_template("success.html", name=form.username.data)
        except IntegrityError:
            db.session.rollback()
            return handle_integrity_error(None, message="User already exists. Please Try Again")

    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return render_template("error.html", message="Invalid Username or Password")

    return render_template("login.html", form=form)


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/dashboard")
@login_required
def dashboard():
    res = requests.get("https://www.googleapis.com/books/v1/volumes",
                       params={"q": "isbn:1442468351"})
    print(res.json())
    data = res.json()
    data_str = json.dumps(data, indent=4)
    return render_template("dashboard.html", name=current_user.username, test=data_str)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route("/library", methods=['GET', 'POST'])
@login_required
def library():
    page = request.args.get('page', 1, type=int)
    per_page = 50

    books = Books.query.paginate(page=page, per_page=per_page)
    return render_template("library.html", books=books,)


@app.route("/search1", methods=['GET', 'POST'])
@login_required
def search1():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    book_isbn = request.args.get('isbn')

    if book_isbn:
        books = Books.query.filter_by(id=book_isbn).paginate(
            page, per_page, error_out=False)
    else:
        books = Books.query.filter((Books.isbn.ilike(f'%{book_isbn}%')))

    return render_template('search1.html', books=books, book_isbn=book_isbn)


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    book_id = request.form.get("book_id")
    title = request.form.get("title")
    author = request.form.get("author")
    year = request.form.get("year")
    search_item = ""
    if book_id:
        search_item = book_id
    elif title:
        search_item = title
    elif author:
        search_item = author
    elif year:
        search_item = year
    items = Books.query.filter(
        Books.isbn.ilike(f'%{book_id}%'),
        Books.name.ilike(f'%{title}%'),
        Books.author.ilike(f'%{author}%'),
        Books.year.ilike(f'%{year}%')
    ).all()
    return render_template("search.html", items=items, search_item=search_item)


@ app.route("/isbn", methods=['GET', 'POST'])
@ login_required
def isbn():
    books = ""
    if request.method == 'POST' and 'isbn' in request.form:
        isbn = request.form["isbn"]
        search = "%{}%".format(isbn)
        books = Books.query.filter(Books.isbn.ilike(search))
        return render_template("isbn.html", books=books, search=isbn)
    return render_template("isbn.html", books=books)


@ app.route("/title", methods=['GET', 'POST'])
@ login_required
def title():
    books = ""
    if request.method == 'POST' and 'title' in request.form:
        title = request.form["title"]
        search = "%{}%".format(title)
        books = Books.query.filter(Books.name.ilike(search))
        return render_template("title.html", books=books, search=title)
    return render_template("title.html", books=books)


@ app.route("/author", methods=['GET', 'POST'])
@ login_required
def author():
    books = ""
    if request.method == 'POST' and 'author' in request.form:
        author = request.form["author"]
        search = "%{}%".format(author)
        books = Books.query.filter(Books.author.ilike(search))
        return render_template("author.html", books=books, search=author)
    return render_template("author.html", books=books)


@ app.route("/year", methods=['GET', 'POST'])
@ login_required
def year():
    books = ""
    if request.method == 'POST' and 'year' in request.form:
        year = request.form["year"]
        search = "%{}%".format(year)
        books = Books.query.filter(Books.year.ilike(search))
        return render_template("year.html", books=books, search=year)
    return render_template("year.html", books=books)


@app.route("/book/<book_isbn>", methods=["GET", "POST"])
def book(book_isbn):

    #fullcode = code.zfill(10)
    # print(fullcode)
    res = requests.get("https://www.googleapis.com/books/v1/volumes",
                       params={"q": f"isbn:{book_isbn}"})

    data = res.json()
    data_str = json.dumps(data, indent=4)
    average_rating = data['items'][0]['volumeInfo']['averageRating']
    ratings_count = data['items'][0]['volumeInfo']['ratingsCount']
    book = Books.query.filter(Books.isbn.ilike(f'%{book_isbn}%'))

    return render_template("book1.html", data_str=data_str, data=jsonify(data), avg_rtg=average_rating, ratings_count=ratings_count, book=book)


@app.route("/review/<book_isbn>", methods=["GET", "POST"])
def review(book_isbn):
    rating = request.form["review"]
    comment = request.form.get('comment')
    new_review = Reviews(user_id=current_user.username, book_id=book_isbn,
                         rating=rating, comment=comment)
    db.session.add(new_review)
    try:
        db.session.commit()
        items = Reviews.query.filter(
            Reviews.book_id.ilike(f'%{book_isbn}%')).all()
        return render_template("review.html", rating=rating, comment=comment, user=current_user.username, items=items)
    except IntegrityError:
        db.session.rollback()
        return handle_integrity_error(None, message="You have already submitted a review for this book.")


@app.route("/api/<book_isbn>", methods=["GET", "POST"])
def api(book_isbn):

    #fullcode = code.zfill(10)
    # print(fullcode)
    res = requests.get("https://www.googleapis.com/books/v1/volumes",
                       params={"q": f"isbn:{book_isbn}"})

    data = res.json()
    data_str = json.dumps(data, indent=4)

    return render_template("api.html", data=data_str, book_isbn=book_isbn)


if __name__ == '__main__':
    with app.app_context():
        main()
