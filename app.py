from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from datetime import timedelta
from flask import render_template

from models import db
from models.node import Node
from models.topic import Topic , Comment
from models.user import User


app = Flask(__name__)
manager = Manager(app)


def register_routes(app):
    from routes.node import main as routes_node
    from routes.topic import main as routes_topic
    from routes.user import main as routes_user
    from routes.homepage import main as routes_homepage

    app.register_blueprint(routes_user, url_prefix='/user')
    app.register_blueprint(routes_topic, url_prefix='/topic')
    app.register_blueprint(routes_node, url_prefix='/node')
    app.register_blueprint(routes_homepage, url_prefix='/home')

def set_error(app):
    @app.errorhandler(401)
    def error401(e):
        return render_template('401.html')


def configured_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    import config
    app.secret_key = config.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
    # session有效时间的设置
    # app.permanent_session_lifetime = timedelta(minutes=1)
    db.init_app(app)
    register_routes(app)
    set_error(app)


    return app


@manager.command
def server():
    print('server run')
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)


def configure_manager():
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configured_app()
    manager.run()






