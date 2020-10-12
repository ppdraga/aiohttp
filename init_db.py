from datetime import datetime

from sqlalchemy import create_engine, MetaData

from aiohttpdemo_polls.settings import config
from aiohttpdemo_polls.db import question, choice


# DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
DSN = 'sqlite:///data.sqlite'

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[question, choice])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(question.insert(), [
        {'question_text': 'What\'s new?',
         'pub_date': datetime.strptime('2015-12-15 17:17:49.629+0200', '%Y-%m-%d %H:%M:%S.%f%z')}
    ])
    conn.execute(choice.insert(), [
        {'choice_text': 'Not much', 'votes': 0, 'question_id': 1},
        {'choice_text': 'The sky', 'votes': 0, 'question_id': 1},
        {'choice_text': 'Just hacking again', 'votes': 0, 'question_id': 1},
    ])
    conn.close()


if __name__ == '__main__':
    # db_url = DSN.format(**config['postgres'])
    engine = create_engine(DSN)

    create_tables(engine)
    sample_data(engine)
