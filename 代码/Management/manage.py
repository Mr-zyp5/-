#-*-coding:utf-8-*-

import sys
sys.path.append('../')
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from Management.app import create_app, db, models

app = create_app('default')
manager = Manager(app)


#绑定app和数据库
migrate = Migrate(app,db)


def make_shell_context():
    return dict(app=app,db=db)

#添加脚本
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("db",MigrateCommand)

if __name__ == "__main__":
    manager.run()