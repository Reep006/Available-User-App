from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)

db = client["availabilityDB"]
collection = db["users"]

# Insert default users only once
if collection.count_documents({}) == 0:

    default_users = [
        {
            "name": "Rahul Sharma",
            "role": "Frontend Developer",
            "available": True,
            "image": "https://i.pinimg.com/736x/82/3b/1f/823b1fb0be191c537854fe693f80c269.jpg"
        },
        {
            "name": "Priya Patel",
            "role": "Backend Developer",
            "available": False,
            "image": "https://i.pinimg.com/736x/2e/e2/5d/2ee25dd0a426eac38863d27545e628dd.jpg"
        },
        {
            "name": "Aman Verma",
            "role": "UI/UX Designer",
            "available": True,
            "image": "https://i.pinimg.com/1200x/cb/97/54/cb975474eeea701f6da246d04f438238.jpg"
        },
        {
            "name": "Sneha Kapoor",
            "role": "Project Manager",
            "available": False,
            "image": "https://i.pinimg.com/736x/10/13/6e/10136e54eccb86c510645dcd7075f076.jpg"
        },
        {
            "name": "Arjun Mehta",
            "role": "Full Stack Developer",
            "available": True,
            "image": "https://i.pinimg.com/1200x/d7/ee/36/d7ee366b6f99c2e0fe11357180df8978.jpg"
        },
        {
            "name": "Neha Joshi",
            "role": "QA Engineer",
            "available": True,
            "image": "https://i.pinimg.com/736x/9b/32/45/9b3245e4274b5d939f11fc37eccd508f.jpg"
        },
        {
            "name": "Karan Malhotra",
            "role": "DevOps Engineer",
            "available": False,
            "image": "https://i.pinimg.com/736x/e8/c4/27/e8c4274e1999641fd6c36b4f9f4f0209.jpg"
        },
        {
            "name": "Riya Singh",
            "role": "Mobile App Developer",
            "available": True,
            "image": "https://i.pinimg.com/736x/9c/98/00/9c9800e979af5dbb2b9e40ad47aeb07a.jpg"
        }
    ]

    collection.insert_many(default_users)


@app.route("/users", methods=["GET"])
def get_users():

    users = []

    for user in collection.find():

        users.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "role": user["role"],
            "available": user["available"],
            "image": user["image"]
        })

    return jsonify(users)


@app.route("/toggle/<id>", methods=["PUT"])
def toggle_availability(id):

    try:

        user = collection.find_one({"_id": ObjectId(id)})

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        new_status = not user["available"]

        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"available": new_status}}
        )

        return jsonify({
            "message": "Availability Updated",
            "available": new_status
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)