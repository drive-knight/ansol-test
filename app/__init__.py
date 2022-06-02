import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from elasticsearch import Elasticsearch
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
es = Elasticsearch('http://localhost:9200', timeout=30)


def create_app(test_config=None):

    app = Flask(__name__)
    app.config.from_object(Config)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import Document

    db.init_app(app)
    migrate.init_app(app, db)

    from .main.routes import main
    app.register_blueprint(main)

    return app
