from app import app
from waitress import serve
if __name__ == '__main__':
    serve(app, host="localhost", port=8000)
