import os
from aiohttp import web
import aiohttp_jinja2
import jinja2

from settings import config, BASE_DIR
from routes import setup_routes
from db import close_pg, init_pg, close_sqlite, init_sqlite


app = web.Application()
app['config'] = config
setup_routes(app)
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(str(os.path.join(BASE_DIR, 'templates'))))
# app.on_startup.append(init_pg)
# app.on_cleanup.append(close_pg)
app.on_startup.append(init_sqlite)
app.on_cleanup.append(close_sqlite)
web.run_app(app, port=8088)
