# coding: utf-8
from aiohttp.web import Application
from aiohttp.web_urldispatcher import UrlDispatcher

from bernard.platforms.facebook import web as fb

app = Application()

router = app.router  # type: UrlDispatcher

router.add_get('/hooks/facebook', fb.check_hook)
router.add_post('/hooks/facebook', fb.receive_events)