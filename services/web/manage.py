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
    OneUser=User(key="david.recchia@reveals.lu",email="david.recchia@reveals.lu",
    name="David",
    role="Root",
    password="Root")
    db.session.add(OneUser)
    db.session.commit()


if __name__ == "__main__":
    cli()
