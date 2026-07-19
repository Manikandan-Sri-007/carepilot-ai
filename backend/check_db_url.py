import app.database as database_module
print(database_module.engine.url.render_as_string(hide_password=False))
