from pack import app, db
from pack.models import Unit, Admin


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)




