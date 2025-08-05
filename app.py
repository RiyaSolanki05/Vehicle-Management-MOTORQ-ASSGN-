from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/api/vehicles",methods=["GET"])
    def list_vehicles():
        try:
            return jsonify(get_vehicles())
        except Exception as e:
            return jsonify({"message": "Failed to get vehicles"}), 500
