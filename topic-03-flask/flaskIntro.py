from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

@app.route("/")
def get_index():
        me = "Josh Romisher"
        return f"<p>Hello, {me} from the world!</p>"

@app.route("/hello")
def get_hello():
        me = "Josh Romisher"
        return f"<p>Hello, {me} from the world!</p>"

@app.route("/goodbye")
def get_goodbye():
        me = "Josh Romisher"
        return f"<p>Goodbye, {me} from the world! Come back soon!</p>"

@app.route("/data")
def get_data():
        data = [
                {"name":"Rosie","type":"dog"},
                {"name":"Peach", "type":"cat"}
        ]
        return jsonify(data)

@app.route("/api/status")
def get_status():
        data = [
                {"name":"suzy", "status":"sleeping"},
                {"name":"dorothy", "status":"hungry"}
        ]
        return jsonify(data)

@app.route('/<path:path>')
def serve_static(path):
        return send_from_directory('.', path)

#run flask --app flaskIntro run 