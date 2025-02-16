from flask import Flask, render_template, jsonify, request
from app.controllers.main_controller import handle_get_summary

def create_app():
    app = Flask(__name__)
    
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/api/get_summary", methods=["POST"])
    def get_summary():
        # When user clicks "Get Summary/Action Items", this route is called
        results = handle_get_summary()
        return jsonify(results), 200

    return app
