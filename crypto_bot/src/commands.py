import click

from src.database import db
from src.puller.controller import Puller
from src.data_preparator.preparator import Preparator


@click.group()
def commands_group():
    pass


@commands_group.command()
def init_db():
    db.init_db()


@commands_group.command()
def run_puller():
    Puller().run()


@commands_group.command()
@click.argument('ticker')
def prepare(ticker):
    Preparator().prepare(ticker=ticker).save()