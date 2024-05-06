from flask.cli import FlaskGroup

from project import app

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    pass


@cli.command("seed_db")
def seed_db():
    pass


if __name__ == "__main__":
    cli()
