"""Code for our app"""

from os import getenv

# from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user
# import pdb

# make our app factory
def create_app():
    app = Flask(__name__)

    #add config for database
    # app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    #stop error message about SQLite overload
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # have DB know about the app
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title= 'Home', users=users)

    # why are both of these lines here?
    # why aren't they combined?
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    # why are we passing "name=None" instead of just "name" and assigning it within the function?
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, 
        message=message)
    
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        # pdb.set_trace()
        user1, user2 = sorted([request.values['user1'], request.values['user2']])
        if user1 == user2:
            message = "Can't compare a user  to themselves..."
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2, 
                user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title = 'Reset', user=[])

    return app