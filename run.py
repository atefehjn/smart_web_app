from app import create_app
from flask_login import LoginManager
app = create_app()
login_manager = LoginManager()
if __name__ == '__main__':
    
    # login_manager.init_app(app)
    app.run(debug=True,port=8080)
    



