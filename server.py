from flask_app import app
from flask_app.controllers.dojos_and_ninjas import Dojo, Ninja

if __name__ == '__main__':
    app.run(debug=True)