from flask import Flask,jsonify
from calc_logic.future_main import doTheThing

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'lol'

    @app.route('/get_expressions/<input>', methods=['GET'])
    def get_expressions(input):
        #unsanitize
        input = input.replace("|","/")
        expressions = doTheThing(input)
        return jsonify(expressions)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
