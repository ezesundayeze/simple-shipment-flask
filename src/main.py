from app_config import app
from dotenv import load_dotenv
from model import db
load_dotenv()
port= os.getenv('PORT')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, port={port})