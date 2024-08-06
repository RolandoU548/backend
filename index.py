from app import app
from utils.db import db
from config import port

with app.app_context():
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    app.run(port=port, debug=True)
