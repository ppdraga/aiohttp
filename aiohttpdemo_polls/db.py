import aiosqlite
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date, create_engine
)

__all__ = ['question', 'choice']

meta = MetaData()

question = Table(
    'question', meta,

    Column('id', Integer, primary_key=True),
    Column('question_text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False)
)

choice = Table(
    'choice', meta,

    Column('id', Integer, primary_key=True),
    Column('choice_text', String(200), nullable=False),
    Column('votes', Integer, server_default="0", nullable=False),

    Column('question_id',
           Integer,
           ForeignKey('question.id', ondelete='CASCADE'))
)

class RecordNotFound(Exception):
    """Requested record in database was not found"""

# postgres
async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

async def get_question(conn, question_id):
    result = await conn.execute(
        question.select()
        .where(question.c.id == question_id))
    question_record = await result.first()
    if not question_record:
        msg = "Question with id: {} does not exists"
        raise RecordNotFound(msg.format(question_id))
    result = await conn.execute(
        choice.select()
        .where(choice.c.question_id == question_id)
        .order_by(choice.c.id))
    choice_records = await result.fetchall()
    return question_record, choice_records


async def vote(conn, question_id, choice_id):
    result = await conn.execute(
        choice.update()
        .returning(*choice.c)
        .where(choice.c.question_id == question_id)
        .where(choice.c.id == choice_id)
        .values(votes=choice.c.votes+1))
    record = await result.fetchone()
    if not record:
        msg = "Question with id: {} or choice id: {} does not exists"
        raise RecordNotFound(msg.format(question_id, choice_id))



# sqlite
async def init_sqlite(app):
    engine = await aiosqlite.connect('data.sqlite')
    engine.row_factory = aiosqlite.Row
    app['db'] = engine
    # yield

async def close_sqlite(app):
    await app['db'].close()
    # await app['db'].wait_closed()

async def get_question_sqlite(conn, question_id):
    result = await conn.execute(str(question.select().where(question.c.id == question_id)), {'id_1': question_id})
    question_record = await result.fetchone()
    if not question_record:
        msg = "Question with id: {} does not exists"
        raise RecordNotFound(msg.format(question_id))
    result = await conn.execute(str(choice.select().where(choice.c.question_id == question_id).order_by(choice.c.id)), 
        {'question_id_1': question_id})
    choice_records = await result.fetchall()
    return question_record, choice_records


async def vote_sqlite(conn, question_id, choice_id):
    result = await conn.execute(
        # str(choice.update()
        # .returning(*choice.c)
        # .where(choice.c.question_id == question_id)
        # .where(choice.c.id == choice_id)
        # .values(votes=choice.c.votes+1)), 
        """
        UPDATE 
            choice SET votes=(choice.votes + :votes_1) 
        WHERE 
            choice.question_id = :question_id_1 AND choice.id = :choice_id 
        """,
        {'votes_1': 1, 'question_id_1': question_id, 'choice_id': choice_id, })
    await conn.commit()
    # record = await result.fetchone()
    # if not record:
    #     msg = "Question with id: {} or choice id: {} does not exists"
    #     raise RecordNotFound(msg.format(question_id, choice_id))

async def get_question_sqlite(conn, question_id):
    result = await conn.execute(
        str(question.select()
        .where(question.c.id == question_id)), {'id_1': question_id})
    question_record = await result.fetchone()
    if not question_record:
        msg = "Question with id: {} does not exists"
        raise RecordNotFound(msg.format(question_id))
    result = await conn.execute(
        str(choice.select()
        .where(choice.c.question_id == question_id)
        .order_by(choice.c.id)), {'question_id_1': question_id})
    choice_records = await result.fetchall()
    return question_record, choice_records