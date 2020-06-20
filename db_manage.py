from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

"""
python3 db_manage.py db init
python3 db_manage.py db migrate
python3 db_manage.py db upgrade
"""
