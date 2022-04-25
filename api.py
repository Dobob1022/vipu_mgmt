
from flask import Flask,request

app = Flask(__name__)


@app.route('/')
def test():
    a = request.args.get('test')
    return {"result":a}


    
if __name__ == "__main__":
    app.run(debug=True, host = '127.0.0.1')