from flask import Flask, render_template, request, redirect
from mongita import MongitaClientDisk
from bson import ObjectId

app = Flask(__name__)

# Writing the data to a Mongita DB file
# Create Mongita Client connection
client = MongitaClientDisk()

# create a quotes DB
quotes_db = client.quotes_db

@app.route("/", methods=["GET"])
@app.route("/quotes", methods=["GET"]) 
def get_quotes():
         # open a quotes collection
        quotes_collection = quotes_db.quotes_collection
        data = list(quotes_collection.find({}))
        for item in data:
                item["_id"] = str(item["_id"])
                item["object"] = ObjectId(item["_id"])
        return render_template("quotes.html", data=data)

@app.route("/create", methods=["GET"])
def get_create_quotes():
        return render_template("create.html")

@app.route("/create", methods=["POST"])
def post_quotes():
        if request.method == "POST":
                #open quotes collection
                quotes_collection = quotes_db.quotes_collection
                #tell function where to find quote and author input
                quote = request.form.get("quote", "")
                author = request.form.get("author", "")
                if quote and author:
                        print([quote, author])
                        quotes_data = {
                                "text":quote,
                                "author":author
                        }
                        quotes_collection.insert_one(quotes_data)
                        return redirect("/quotes")
                else:
                        return "Both author and quote are required"

@app.route("/edit", methods=["GET"])
@app.route("/edit/<id>", methods=["GET"])
def get_edit_quotes(id=None):
        if id:  
                #open collection
                quotes_collection = quotes_db.quotes_collection
                #find quote by ObjectId
                data = quotes_collection.find_one({"_id": ObjectId(id)})
                
        return render_template("/edit.html", data=data)


@app.route("/delete", methods=["GET"])
@app.route("/delete/<id>", methods=["GET"]) 
def get_delete(id=None):
         # delete a scifi collection
        if id:
                #open collection
                quotes_collection = quotes_db.quotes_collection
                #delete the item
                quotes_collection.delete_one({"_id":ObjectId(id)})
                

        return redirect("/quotes")
       
#run flask --app flaskIntro run 