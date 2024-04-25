from flask import Flask
from routes.account import account
from routes.attendance import attendance
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(attendance,url_prefix="/attendace")

@app.route('/')
def hello_world():
   return 'welcome to collage project backend'

if __name__ == '__main__':
   app.run()