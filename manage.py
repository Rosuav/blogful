import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from blog import app

from blog.database import session, Entry, User, Base
from getpass import getpass
from werkzeug.security import generate_password_hash




manager = Manager(app)


@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)


@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
               Ut enim ad minim veniam, quis nostrud exercitation ullamo laboris nisi ut aliquip ex ea commode consequat.Duis aute irure dolor in 
               reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidate non proident, sunt in 
               culpa qui deserunt mollit amim id est laborum"""
    
    for i in range(25):
        entry = Entry(
            title="Test Entry #{}".format(i), 
            content=content
        )
    session.add(entry)
    session.commit()
 
@manager.command
def adduser():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return
    
    password = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email, password=generate_password_hash(password))
    session.add(user)
    session.commit()




class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata
        
migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)
    
if __name__=="__main__":
    manager.run()