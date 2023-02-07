# postgresql://postgres:23081201@localhost/engo551_lab1
# import requests
from models import *
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

bootstrap = Bootstrap(app)

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


@app.route("/")
def main():
    db.create_all()
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, name, author, year in reader:
        book = Books(isbn=isbn, name=name, author=author,
                     year=year)
    db.session.add(book)
    db.session.commit()
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

        return '<h1>New User has been created!</h1>'

    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    message = "Login"
    if form.validate_on_submit():
        user = Users.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password!</h1>'

    return render_template("login.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with application.app_context():
        main()
