from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/video', methods=['POST'])
def post_video():
    print(request.get_json())
    return 'OK'

app.run(host='0.0.0.0', port=8080)