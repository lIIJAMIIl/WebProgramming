from flask import Flask, render_template, request, redirect, make_response
from mongita import MongitaClientDisk
from bson import ObjectId

app = Flask(__name__)

# Writing the data to a Mongita DB file
# Create Mongita Client connection
client = MongitaClientDisk()

# create a quotes DB
quotes_db = client.quotes_db
session_db = client.session_db

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
        #open a session collection
        session_collection = session_db.session_collection
        #find and list session data
        session_data = list(session_collection.find({"session_id": session_id}))
        if len(session_data) == 0:
                response = redirect("/logout")
                return response
        assert len(session_data) == 1
        session_data = session_data[0]
        #getting session information from the session data variable
        user = session_data.get("user", "unknown user")
         # open a quotes collection
        quotes_collection = quotes_db.quotes_collection
        data = list(quotes_collection.find({"owner": user}))
        for item in data:
                item["_id"] = str(item["_id"])
                item["object"] = ObjectId(item["_id"])
        html = render_template("quotes.html", data=data, number_of_visits = number_of_visits, session_id=session_id, user = user)
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
        session_id = request.cookies.get("session_id", None)
        if not session_id:
                response = redirect("/login")
                return response
        #open session collection db
        session_collection = session_db.session_collection
        #get session data from the db
        session_data = list(session_collection.find({"session_id": session_id}))
        if len(session_data) == 0:
                response = redirect("/logout")
                return response
        assert len(session_data) == 1
        session_data = session_data[0]
        #get user information from the session data
        user = session_data.get("user", "unknown user")
        text = request.form.get("text", "")
        author = request.form.get("author", "")
        if text != "" and author != "":
                #opening quotes db
                quotes_collection = quotes_db.quotes_collection
                #inserting quote into the quotes db
                quotes_data = {"owner": user, "text": text, "author": author}
                quotes_collection.insert_one(quotes_data)
        return redirect("/quotes")

#@app.route("/edit", methods=["GET"])
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
                values = {"$set": {"text": text, "author": author}}
                data = quotes_collection.update_one({"_id": ObjectId(_id)}, values)
                if data.modified_count > 0:
                        print("Quote updated successfully.")
                else:
                        print("Update unsuccessful.")

        # Return to quotes page
        return redirect("/quotes")

@app.route("/logout", methods=["GET"])
def get_logout():
        #get session_id
        session_id = request.cookies.get("session_id", None)
        if session_id:
                #open the session db collection
                session_collection = session_db.session_collection
                #deleting the session information from the database
                session_collection.delete_one({"session_id": session_id})
        response = redirect("/login")
        response.delete_cookie("session_id")
        return response

@app.route("/login", methods=["POST"])
def post_login():
        #set session id
        session_id =str(uuid.uuid4())
        #get the user from the form input field
        user = request.form.get("user", "")
        #open session collection
        session_collection = session_db.session_collection
        #insert the user into the session_db
        session_collection.delete_one({"session_id": session_id})
        session_data = {"session_id": session_id, "user": user}
        session_collection.insert_one(session_data)
        response = redirect("/quotes")
        response.set_cookie("session_id", session_id)
        return response

@app.route("/login", methods=["GET"])
def get_login():
        session_id = request.cookies.get("session_id", None)
        print("Pre-login session id is:", session_id)
        if session_id:
                return redirect("/quotes")
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