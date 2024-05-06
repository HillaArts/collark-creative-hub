from app import app
from db import db, init_app
init_app(app)
with app.app_context():
    db.create_all()