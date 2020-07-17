from flask import Flask , request , jsonify , Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/liveware_db"
mongo = PyMongo(app)

@app.route("/users" , methods=["POST"])
def create_user():
    ## Recibir data
    title_job = request.json["title_job"]
    description = request.json["description"]
    datetime = request.json["datetime"]

    if title_job and description and datetime:

       id = mongo.db.jobs.insert({"title_job":title_job,
                                "description":description,
                                "datetime" : datetime})

       response = {
            "_id" : str(id),
            "title_job":title_job,
            "description":description,
            "datetime" : datetime
       }

       return response

    else:
        return not_found()


    return {"message":"received"}

@app.route("/users", methods=["GET"])
def get_users():
    users = mongo.db.jobs.find()
    response = json_util.dumps(users)
    ## el mime type es una cabecera para que el cliente imprima la lista tipica de json
    return Response(response , mimetype = "application/json")

@app.errorhandler(404)
def not_found(error=None):
    ## ACA HACEMOS QUE LARGUE EL ERROR Y QUE CAMBIE EL STATUS A 404
    response = jsonify({
    "message":"Recurso no encontrado " +request.url,
    "status" : 404
    })
    response.status_code = 404
    return response

@app.route("/users/<id>")
def get_user(id):
    user = mongo.db.jobs.find_one({"_id":ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route("/users/<id>", methods = ["PUT"])
def update_user(id):
    title_job = request.json["title_job"]
    description = request.json["description"]
    datetime = request.json["datetime"]

    if title_job and description and datetime:
        mongo.db.jobs.update_one(
            {"_id": ObjectId(id) },{"$set": {
            "title_job":title_job,
            "description":description,
            "datetime" : datetime}
            })
    response = jsonify({"message":f"El usuario con la {id} fue actualizado"})
    return response

@app.route("/users/<id>",methods = ["DELETE"])
def delete_user(id):
    mongo.db.jobs.delete_one({"_id": ObjectId(id)})
    response = jsonify({"message": "El usuario :" + id + "fue eliminado correctamente"})
    return response


if __name__ == "__main__":
    app.run(debug=True)
