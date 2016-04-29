#coding=utf-8
'''
Created on 2016年04月15日

@FileName: manage.py

@Description: (描述) 

@Site:  http://www.sugarguo.com/

@author: 'Sugarguo'

@version V1.0.0
'''

import os
import sys
sys.path.insert(0,'ext_lib')

from app import create_app, db
from app.models import User
from flask.ext.script import Manager, Shell
from flask.ext.script.commands import ShowUrls, Clean
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('test') 
    unittest.TextTestRunner(verbosity=2).run(tests)


def make_shell_context():
	return dict(app = app, db = db, User = User)
manager.add_command("shell", Shell(make_context = make_shell_context))
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
