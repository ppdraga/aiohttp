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

@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].execute(str(db.question.select())) as cursor:
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        # return web.Response(text=str(questions))
        return {"questions": questions}

@aiohttp_jinja2.template('detail.html')
async def poll(request):
    async with request.app['db'] as conn:
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