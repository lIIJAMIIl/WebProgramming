from flask import Flask, render_template, request, redirect, make_response
from mongita import MongitaClientDisk
from bson import ObjectId

app = Flask(__name__)

# Writing the data to a Mongita DB file
# Create Mongita Client connection
client = MongitaClientDisk()

# create a quotes DB
quotes_db = client.quotes_db

import uuid

session_key = uuid.uuid4()

print(session_key)

@app.route("/", methods=["GET"])
@app.route("/quotes", methods=["GET"]) 
def get_quotes():
        #get number of visits via cookie; cookies always strings so cast to int
        number_of_visits = int(request.cookies.get("number_of_visits", "0"))
        session_id = request.cookies.get("session_id", None)
        if not session_id:
                response = redirect("/login")
                return response
         # open a quotes collection
        quotes_collection = quotes_db.quotes_collection
        data = list(quotes_collection.find({}))
        for item in data:
                item["_id"] = str(item["_id"])
                item["object"] = ObjectId(item["_id"])
        html = render_template("quotes.html", data=data, number_of_visits = number_of_visits, session_id=session_id)
        response = make_response(html)
        response.set_cookie("number_of_visits", str(number_of_visits + 1))
        response.set_cookie("session_id", str(session_id))
        return response

@app.route("/create", methods=["GET"])
def get_create_quotes():
        session_id = request.cookies.get("session_id", None)
        if not session_id:
                response = redirect("/login")
                return response
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
        session_id = request.cookies.get("session_id", None)
        if not session_id:
                response = redirect("/login")
                return response
        if id:  
                #open collection
                quotes_collection = quotes_db.quotes_collection
                #find quote by ObjectId
                data = quotes_collection.find_one({"_id": ObjectId(id)})
                #return json as string
                data["id"] = str(data["_id"])
                return render_template("/edit.html", data=data)
        return render_template("/quotes.html")

@app.route("/edit", methods=["POST"])
def post_edit():
        session_id = request.cookies.get("session_id", None)
        if not session_id:
                response = redirect("/login")
                return response
        _id = request.form.get("_id", None)
        text = request.form.get("text", "")
        author = request.form.get("author", "")
        if _id:
                # Open collection
                quotes_collection = quotes_db.quotes_collection
                # Update the values associated with this particular ObjectId
                data = quotes_collection.update_one({"_id": ObjectId(_id)}, {"$set": {"text": text, "author": author}})
                if data.modified_count > 0:
                        print("Quote updated successfully.")
                else:
                        print("Update unsuccessful.")

        # Return to quotes page
        return redirect("/quotes")

@app.route("/logout", methods=["GET"])
def get_logout():
        response = redirect("/login")
        response.delete_cookie("session_id")
        return response

@app.route("/login", methods=["POST"])
def post_login():
        session_id =str(uuid.uuid4())
        response = redirect("/quotes")
        response.set_cookie("session_id", session_id)
        user = request.form.get("user", "")
        response.set_cookie("user", user)
        return response

@app.route("/login", methods=["GET"])
def get_login():
        return render_template("login.html")

@app.route("/delete", methods=["GET"])
@app.route("/delete/<id>", methods=["GET"]) 
def get_delete(id=None):
        session_id = request.cookies.get("session_id", None)
        if not session_id:
                response = redirect("/login")
                return response
         # delete a quote
        if id:
                #open collection
                quotes_collection = quotes_db.quotes_collection
                #delete the item
                quotes_collection.delete_one({"_id":ObjectId(id)})
                

        return redirect("/quotes")
       
#run flask --app flaskIntro run 