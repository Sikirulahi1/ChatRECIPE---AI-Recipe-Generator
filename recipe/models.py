from recipe import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = True)
    email = db.Column(db.String, unique=True, nullable = False)
    google_id = db.Column(db.String(256), unique=True, nullable=True)

    def __repr__(self):
        return f" User {self.username} with the email {self.email}"
    
    def get_id(self):
        return self.uid
