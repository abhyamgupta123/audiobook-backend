import os
# os.environ['connection'] = os.path.join(os.getcwd(), 'Requip', 'static')
# os.environ['FILES'] = os.path.join(os.getcwd(), 'Requip', 'media')
from dotenv import load_dotenv
load_dotenv()
# print(os.getenv('connection'))
from audiobook import app

app.run(debug=True, host="0.0.0.0")
