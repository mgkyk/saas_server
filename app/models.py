#encoding:utf8
from passlib.apps import custom_app_context as pwd_context
from app import db
import random

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(40))
    password_hash = db.Column(db.String(40))  # password need to be hashed before installed
    source_info = db.Column(db.String(200))
    
    def __init__(self, id, user):
        self.id = id
        self.user = user
        self.source_info = ""

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def hash_password(self, password):
        self.password_hash =  pwd_context.encrypt(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)


# table VM_machine
class VM_machine(db.Model):
    mc_id = db.Column(db.String(40), primary_key=True)
    user = db.Column(db.String(40))
    apply_info = db.Column(db.String(200))  # 部署应用的情况
    state = db.Column(db.String(10))  # 是否开启

    def __repr__(self):
        return '<mc_id %r>' % self.mc_id


# table Resource
class Resource(db.Model):
    source_name = db.Column(db.String(40), primary_key=True)
    map = db.Column(db.String(40))
    shell_path = db.Column(db.String(200))
    detail = db.Column(db.String(200))

    def __init__(self, source_name, map, shell_path, detail):
        self.source_name = source_name
        self.map = map
        self.shell_path = shell_path
        self.detail = detail

    def __repr__(self):
        return '<source_name %r>' % self.source_name


def create_id():  # create a new id
    return random.randrange(0, 1000, 1)

