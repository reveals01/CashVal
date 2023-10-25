from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash 
from project import app,db,User


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("init_db")
def init_db():
    OneUser=User(key="admin@orchestro.lu",email="admin@orchestro.lu",
    name="Admin",
    surname="Admin",
    role="Root",
    password="Root",)
    db.session.add(OneUser)
    SndUser=User(key="demo@orchestro.lu",email="demo@orchestro.lu",
    name="Demo",
    surname="Demo",
    role="demo",
    password="Demo",)
    db.session.add(SndUser)
    db.session.commit()

if __name__ == "__main__":
    cli()
