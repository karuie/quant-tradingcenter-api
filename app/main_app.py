import os.path
import pathlib
import sys
from dotenv import load_dotenv
load_dotenv()


app_path = pathlib.Path(__file__).parent
sys.path.extend([
    os.path.abspath(app_path),
    os.path.abspath(app_path.parent),
    os.path.dirname(os.environ.get('FALCON_LIB_PATH')),
    os.environ.get('FALCON_LIB_PATH'),
])

from app import create_app
from api.auth import token_required

app = create_app()


@app.route('/')
@token_required
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    # app = create_app()
    print(sys.path)
    app.run()
    pass
