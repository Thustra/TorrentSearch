__author__ = 'Peter'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import datetime
import os

Base = automap_base()

engine = create_engine(os.environ['DATABASE_URL'])

# Reflect the tables
Base.prepare(engine,reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.

Downloads = Base.classes.downloads
Shows = Base.classes.shows

Session = sessionmaker(bind=engine)

def get_downloads():
    session = Session()
    for instance in session.query(Downloads).all():
        print(instance.filename)

def get_series(watching=True,finished=False):
    session = Session()
    return session.query(Shows).filter_by(watching=watching).all()


def get_downloads(series):
    session = Session()
    for result in session.query(Shows).filter_by(title=series).all():
        print(result.id)


def get_show_id(series):
    session = Session()
    for result in session.query(Shows).filter_by(title=series).all():
        return result.id

#
# Method works
# TODO: get the right data
#
def add_download(filename,size,location,season,show):
    session = Session()
    show_id = get_show_id(show)
    download_timestamp = datetime.datetime.now()
    entry = Downloads(filename=filename, size=size, location=location,
                      download_timestamp=download_timestamp, show_id=show_id,
                      season=season)
    session.add(entry)
    session.commit()

def add_show(name, watching, finished,tvmaze_id):
    session = Session()
    entry = Shows(title=name, watching=watching, finished=finished,tvmaze_id=tvmaze_id)
    session.add(entry)
    session.commit()
