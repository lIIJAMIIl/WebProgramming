from flask import Flask, jsonify, render_template, send_from_directory
from mongita import MongitaClientDisk

# Writing the data to a Mongita DB file
# open Mongita Client connection
client = MongitaClientDisk()

# create a movei DB
movie_db = client.movie_db



app = Flask(__name__)

@app.route("/data/movies/scifi")
def get_data_movies_scifi():
        # with open("classic_sci_fi_movies.json", "r") as f:
        #         data =json.load(f) 
        # open a scifi collection
        scifi_collection = movie_db.scifi_collection
        data = list(scifi_collection.find({}))
        for item in data:
                del item["_id"]
        return jsonify(data)

@app.route("/hello")
@app.route("/hello/<name>")
def get_hello(name="Guest"):
        return render_template("hello.html", names=[name,"Alpha","Beta","Gamma"])

@app.route("/movies")
@app.route("/movies/<keyword>")
def get_movies(keyword=None):
        scifi_collection = movie_db.scifi_collection
        data = list(scifi_collection.find({}))
        for item in data:
                del item["_id"] 
        if keyword:
                 data = [item for item in data if keyword in item['plot']] 
        return render_template("movies.html", movies=data)

@app.route("/movies")
@app.route("/movies/<keyword>")
def get_movies2(keyword=None):
        scifi_collection = movie_db.scifi_collection
        data = list(scifi_collection.find({}))
        if keyword:
                data = list(scifi_collection.find({"title": keyword }))
        else:
                data = list(scifi_collection.find({}))
        for item in data:
                del item["_id"] 
        if keyword:
                 data = [item for item in data if keyword in item['plot']] 
        return render_template("movies.html", movies=data)



@app.route("/hello2/<name>")
def get_hello2(name):
        return render_template("hello.html", name=name)

@app.route('/')
def serve_index():
        return send_from_directory('.',"index.html")

@app.route('/<path:path>')
def serve_static(path):
        return send_from_directory('.', path)

#run flask --app flaskIntro run 