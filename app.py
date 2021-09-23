# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

from datetime import datetime

from flask import Flask, render_template, flash, request, redirect, url_for
from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager,current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, equal_to
# create a flask instance
from wtforms.widgets import TextArea

from webForms import  *

app = Flask(__name__)
# secret key


# add db

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' ## old one
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/users'  ## new one
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/users'  ## new one

app.config['SECRET_KEY'] = "my super secret key"

# init the db

db = SQLAlchemy(app)
migrate = Migrate(app,
                  db)


# Create db Model:



#
# # create form class
# class NamerForm(FlaskForm):
#     name = StringField("What is your name?",
#                        validators=[DataRequired()])
#     submit = SubmitField("Submit")
#
#
# class PasswordForm(FlaskForm):
#     email = StringField("What is your email?",
#                         validators=[DataRequired()])
#     password_hash = PasswordField("What is your password?",
#                                   validators=[DataRequired()])
#     submit = SubmitField("Submit")


# class UserForm(FlaskForm):
#     name = StringField("Name",
#                        validators=[DataRequired()])
#
#     username = StringField("username",
#                            validators=[DataRequired()])
#     email = StringField("Email",
#                         validators=[DataRequired()])
#     fav_color = StringField("Favorite Color")
#     password_hash = PasswordField("Password",
#                                   validators=[DataRequired(), equal_to('password_hash_2',
#                                                                        message='Password must to match')])
#     password_hash_2 = PasswordField("Confirm Password",
#                                     validators=[DataRequired()])
#     submit = SubmitField("Submit")




# class PostForm(FlaskForm):
#     title = StringField("Title",
#                         validators=[DataRequired()])
#     content = StringField("Content",
#                           validators=[DataRequired()],
#                           widget=TextArea())
#     author = StringField("Author",
#                          validators=[DataRequired()])
#     slug = StringField("Slug",
#                        validators=[DataRequired()])
#     submit = SubmitField("Submir")
#

# add a post page
@app.route('/add-post',
           methods=['GET', 'POST'])
# @login_required # only login user can add a post
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data,
                     content=form.content.data,
                     author=form.author.data,
                     slug=form.slug.data)
        # clear the form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # add data to the db
        db.session.add(post)
        db.session.commit()
        flash("Blog post submitted successfully")

    return render_template('add_post.html',
                           form=form)


@app.route('/posts/<int:id>')
def post(id):
    _post = Posts.query.get_or_404(id)
    return render_template("post.html",
                           post=_post)


@app.route('/posts/edit/<int:id>',
           methods=['GET', 'POST'])
@login_required
def edit_post(id):
    _post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        _post.title = form.title.data
        _post.author = form.author.data
        _post.slug = form.slug.data
        _post.content = form.content.data

        # update db
        db.session.add(_post)
        db.session.commit()
        flash("Post has been updated")
        return redirect(url_for('post',
                                id=_post.id))
    form.title.data = _post.title
    form.author.data = _post.author
    form.slug.data = _post.slug
    form.content.data = _post.content
    return render_template('edit_post.html',
                           form=form)


@app.route('/posts/delete/<int:id>')
def delete_post(id):
    form = PostForm()
    name = None
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post deleted successfully")
        our_posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',
                               posts=our_posts)



    except:
        flash("error in deleting")
        our_posts = Posts.query.order_by(Posts.date_posted)
        return render_template(url_for('post',
                                       posts=our_posts))


@app.route('/posts')
def posts():
    # show all the posts from the db
    posts = Posts.query.order_by(Posts.date_posted)

    return render_template("posts.html",
                           posts=posts)


# update recorde in database

@app.route('/update/<int:id>',
           methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.fav_color = request.form['fav_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            db.session.commit()
            flash("error in updating")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else:  # GET
        return render_template("update.html",
                               form=form,
                               name_to_update=name_to_update)


# delete recorde in database
@app.route('/delete/<int:id>')
def delete(id):
    form = UserForm()
    name = None
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
                               form=form,
                               name=name,
                               our_users=our_users)



    except:
        flash("error in deleting")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
                               form=form,
                               name=name,
                               our_users=our_users)


# create route -> with a decorator


@app.route('/users/add',
           methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_password = generate_password_hash(form.password_hash.data,
                                                     "sha256")
            user = Users(name=form.name.data,
                         username=form.username.data,
                         email=form.email.data,
                         fav_color=form.fav_color.data,
                         password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.fav_color.data = ''
        form.password_hash = ''
        form.username = ''
        flash("user added")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)


# Flask login stuff
login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = 'login'


@login_manger.user_loader
def load_user(id):
    return Users.query.get_or_404(id)


# create login form

# creat login page
class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired()])

    password = PasswordField("Confirm Password",
                             validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/login',
           methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if (user):
            # check the hash password
            if check_password_hash(user.password_hash,
                                   form.password.data):
                # login
                login_user(user)
                flash("OK")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password\n please try age")
        else:
            flash("this user doesnt exist")
    return render_template('login.html',
                           form=form)


# create logout page
@app.route('/logout',
           methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("logout succeeds")
    return redirect(url_for('login'))


@app.route('/dashboard',
           methods=['POST', 'GET'])




@login_required
def dashboard():
    form = UserForm()
    id = current_user.id

    name_to_update = Users.query.get_or_404(current_user.id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.fav_color = request.form['fav_color']
        name_to_update.username = request.form['username']

        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template("dashboard.html",
                                   form=form,
                                   name_to_update=name_to_update,id=id)
        except:
            db.session.commit()
            flash("error in updating")
            return render_template("dashboard.html",
                                   form=form,
                                   name_to_update=name_to_update,id=id)
    else:  # GET
        return render_template("dashboard.html",
                               form=form,
                               name_to_update=name_to_update,id=id)

    return render_template('dashboard.html')


# creat dashboard page

@app.route('/')
def index():
    flash("WELCOME")
    first_name = "avi"
    return render_template('index.html')


# localhost:500/user/username

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',
                           user_name=name)


# create a test password page

@app.route('/test_psw',
           methods=['POST', 'GET'])
def test_psw():
    email = None
    password = None
    psw_to_check = None
    passed = None
    form = PasswordForm()
    # validate Form
    if form.validate_on_submit():
        # if the form was filled and submit was clicked
        email = form.email.data
        password = form.password_hash.data

        # clear the form
        form.email.data = ''
        form.password_hash.data = ''

        # retrieve the passed by the email
        psw_to_check = Users.query.filter_by(email=email).first()

        # check hash password
        passed = check_password_hash(psw_to_check.password_hash,
                                     password)

        # flash("Form Submitted successful")
    return render_template('test_psw.html',
                           email=email,
                           password=password,
                           passed=passed,
                           psw_to_check=psw_to_check,
                           form=form)


# create a name page
@app.route('/name',
           methods=['POST', 'GET'])
def name():
    name = None
    form = NamerForm()
    # validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted successful")
    return render_template('name.html',
                           name=name,
                           form=form)


@app.route('/date')
def get_current_date():
    fav_pizza = {
        "Natan": "pepperoni",
        "Avi": "Cheese",
        "Tim": "Mushrooms"
    }
    return fav_pizza
    # return  {"Date:":date.today()}

#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template("404.html"), 404
#
#
# # Internal Server Error
# @app.errorhandler(500)
# def page_not_found(e):
#     return render_template("500.html"), 500
class Users(db.Model,
            UserMixin):
    username = db.Column(db.String(20),
                         nullable=False,
                         unique=True)
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(200),
                     nullable=False)
    email = db.Column(db.String(120),
                      nullable=False,
                      unique=True)
    fav_color = db.Column(db.String(120),
                          default="None")

    date_added = db.Column(db.DateTime,
                           default=datetime.utcnow())
    # passwords things
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable')

    @password.setter
    def password(self, _password):
        self.password_hash = generate_password_hash(_password)

    def verify_password(self, _password):
        return check_password_hash(self.password_hash,
                                   _password)

    # create a string
    def __repr__(self):
        return '<Name %r>' % self.name

class Posts(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(225))
    content = db.Column(db.Text)
    author = db.Column(db.String(225))
    date_posted = db.Column(db.DateTime,
                            default=datetime.utcnow)
    slug = db.Column(db.String(255))

    # class Users(db.Model,
    #             UserMixin):
    #     username = db.Column(db.String(20),
    #                          nullable=False,
    #                          unique=True)
    #     id = db.Column(db.Integer,
    #                    primary_key=True)
    #     name = db.Column(db.String(200),
    #                      nullable=False)
    #     email = db.Column(db.String(120),
    #                       nullable=False,
    #                       unique=True)
    #     fav_color = db.Column(db.String(120),
    #                           default="None")
    #
    #     date_added = db.Column(db.DateTime,
    #                            default=datetime.utcnow())
    #     # passwords things
    #     password_hash = db.Column(db.String(128))
    #
    #     @property
    #     def password(self):
    #         raise AttributeError('password is not a readable')
    #
    #     @password.setter
    #     def password(self, _password):
    #         self.password_hash = generate_password_hash(_password)
    #
    #     def verify_password(self, _password):
    #         return check_password_hash(self.password_hash,
    #                                    _password)

if __name__ == '__main__':
    app.run()
