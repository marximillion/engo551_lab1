# postgresql://postgres:23081201@localhost/engo551_lab1
# import requests
from models import *
#from flask_sqlalchemy import SQLAlchemy

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

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


@app.route("/", methods=['GET'])
def main():
    db.create_all()
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, name, author, year in reader:
        book = Books(isbn=isbn, name=name, author=author,
                     year=year)
        db.session.add(book)
    db.session.commit()
    db.session.close()
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    username = form.username.data
    password = form.password.data
    message = "Registration"

    if form.validate_on_submit():
        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        if new_user.query.filter_by(username=form.username.data).first():
            return redirect(url_for('error'))

        return '<h1>New User has been created!</h1>'

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

        return redirect(url_for('error'))

    return render_template("login.html", form=form)


@app.route("/error")
def error():
    # if current_user.is_authenticated == False:
    #message1 = "User already exists"
    message = "Invalid username or password"

    return render_template("error.html", message=message)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route("/search", methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/search/<int:page>', methods=['GET', 'POST'])
@login_required
def search(page):
    page = page
    pages = 30
    books = Books.query.filter().all()
    form = BookForm()
    # if form.validate_on_submit():
    #isbn = Books.query.filter_by(isbn=form.isbn.data).all()
    # return redirect(url_for('results'))
    if request.method == 'POST' and 'title' in request.form:
        title = request.form["title"]
        search = "%{}%".format(title)
        books = Books.query.filter(Books.name.like(search))
        return render_template("search.html", books=books)
    return render_template("search.html", books=books)


@app.route("/results")
@login_required
def results():
    return render_template("search.html")


if __name__ == '__main__':
    with app.app_context():
        main()
