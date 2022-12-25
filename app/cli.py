import os
import click
from flask import Blueprint

from models import Actor, Song

from db import conn

bp = Blueprint('commands', __name__)

@bp.cli.command("create_db")
@click.option('-name', default="geniusAPI")
def create_db(name):
    print("creating db %s " % name)
    conn.drop_all()
    conn.create_all()
    conn.session.commit()