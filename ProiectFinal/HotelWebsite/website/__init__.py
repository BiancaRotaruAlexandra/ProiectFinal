from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hida gufy gmca'

    from .home import views
    from .book import book
    from .reviews import reviews
    from .admin import administrator
    from .reports import reports

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(book, url_prefix='/')
    app.register_blueprint(reviews, url_prefix='/')
    app.register_blueprint(administrator, url_prefix='/')
    app.register_blueprint(reports, url_prefix='/')

    return app
