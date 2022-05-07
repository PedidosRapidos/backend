from . import database, app  # noqa: F401,F403

database.init()
app = app.app
