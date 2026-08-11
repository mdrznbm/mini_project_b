# A Flask app for portfolio and community features

import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "comments.db")

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "mini project a and b"
login_manager = LoginManager()
login_manager.init_app(app)


# --- Database Models ---

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)

    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


# --- Application Routes ---

@app.route("/")
def index():
    return render_template("main_page.html")


@app.route("/about-me")
def about_me():
    return render_template("about_me.html")


@app.route("/contact-me")
def contact_me():
    return render_template("contact_me.html")


@app.route("/community-board", methods=["GET", "POST"])
def community_board():
    if request.method == "GET":
        return render_template("community_board.html", comments=Comment.query.all())

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('community_board'))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None or not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('community_board'))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('community_board'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
