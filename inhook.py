import flask
app = flask.Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = flask.request.get_json()
    print(update)
    return "OK", 200

app.run(host="0.0.0.0", port=5000)