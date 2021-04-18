import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

def startServer(app):
  config = Config().from_pyfile("config.py")
  asyncio.run(serve(app, config))
