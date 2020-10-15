from aiohttp import web
import aiohttp_jinja2
import db

# async def index(request):
#     # return web.Response(text='Hello Aiohttp!')
#     async with request.app['db'].acquire() as conn:
#         cursor = await conn.execute(db.question.select())
#         records = await cursor.fetchall()
#         questions = [dict(q) for q in records]
#         return web.Response(text=str(questions))

# @aiohttp_jinja2.template('detail.html')
# async def poll(request):
#     async with request.app['db'].acquire() as conn:
#         question_id = request.match_info['question_id']
#         try:
#             question, choices = await db.get_question_sqlite(conn,
#                                                       question_id)
#         except db.RecordNotFound as e:
#             raise web.HTTPNotFound(text=str(e))
#         return {
#             'question': question,
#             'choices': choices
#         }

# @aiohttp_jinja2.template('results.html')
# async def results(request):
#     async with request.app['db'].acquire() as conn:
#         question_id = request.match_info['question_id']

#         try:
#             question, choices = await db.get_question(conn,
#                                                       question_id)
#         except db.RecordNotFound as e:
#             raise web.HTTPNotFound(text=str(e))

#         return {
#             'question': question,
#             'choices': choices
#         }

# async def vote(request):
#     async with request.app['db'].acquire() as conn:
#         question_id = int(request.match_info['question_id'])
#         data = await request.post()
#         try:
#             choice_id = int(data['choice'])
#         except (KeyError, TypeError, ValueError) as e:
#             raise web.HTTPBadRequest(
#                 text='You have not specified choice value') from e
#         try:
#             await db.vote(conn, question_id, choice_id)
#         except db.RecordNotFound as e:
#             raise web.HTTPNotFound(text=str(e))
#         router = request.app.router
#         url = router['results'].url_for(question_id=str(question_id))
#         return web.HTTPFound(location=url)



# sqlite:

@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].execute(str(db.question.select())) as cursor:
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        # return web.Response(text=str(questions))
        return {"questions": questions}


@aiohttp_jinja2.template('detail.html')
async def poll(request):

    conn = request.app['db']
    question_id = request.match_info['question_id']
    try:
        question, choices = await db.get_question_sqlite(conn,
                                                    question_id)
    except db.RecordNotFound as e:
        raise web.HTTPNotFound(text=str(e))
    return {
        'question': question,
        'choices': choices
    }

@aiohttp_jinja2.template('results.html')
async def results(request):
    conn = request.app['db']
    question_id = request.match_info['question_id']

    try:
        question, choices = await db.get_question_sqlite(conn,
                                                    question_id)
    except db.RecordNotFound as e:
        raise web.HTTPNotFound(text=str(e))

    return {
        'question': question,
        'choices': choices
    }


async def vote(request):
    conn = request.app['db']
    question_id = int(request.match_info['question_id'])
    data = await request.post()
    try:
        choice_id = int(data['choice'])
    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(
            text='You have not specified choice value') from e
    try:
        await db.vote_sqlite(conn, question_id, choice_id)
    except db.RecordNotFound as e:
        raise web.HTTPNotFound(text=str(e))
    router = request.app.router
    url = router['results'].url_for(question_id=str(question_id))
    return web.HTTPFound(location=url)
