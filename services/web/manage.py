from flask.cli import FlaskGroup

from project import app

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    counter = 0


@cli.command("seed_db")
def seed_db():
    counter = 0

if __name__ == "__main__":
    cli()
