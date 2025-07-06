import traceback
from flask import Blueprint, jsonify
from scrapers.worldometers import (
    scrape_country_population,
    scrape_world_population,
    scrape_world_population_ranking
)

population_bp = Blueprint('population', __name__)

@population_bp.route("/api/v1/population/world", methods=["GET"])
def get_world_population():
    try:
        data = scrape_world_population() 
        return jsonify({"data": data}), 200
    except Exception:
        print("[ERROR]", traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

@population_bp.route("/api/v1/population/world/ranking", methods=["GET"])
def get_world_population_ranking():
    try:
        data = scrape_world_population_ranking() 
        return jsonify({"data": data}), 200
    except Exception:
        print("[ERROR]", traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500


@population_bp.route("/api/v1/population/country/<country>", methods=["GET"])
def get_country_population(country):
    try:
        country = country.strip().lower()
        data = scrape_country_population(country)
        return jsonify({"data": data}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception:
        print("[ERROR]", traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500
