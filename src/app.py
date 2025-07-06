from flask import Flask, jsonify, request, render_template
from scrapers.worldometers.scraper import scrape_country_population  # make sure folder name matches

app = Flask(__name__, template_folder='./templates')

import traceback

@app.route("/api/<source>/<category>/<target>", methods=["GET"])
def get_population(source, category, target):
    country = target.strip().lower()
    if not country:
        return jsonify({
            "error": "Missing 'target' URL parameter",
            "source": source,
            "category": category,
            "target": target
        }), 400
    try:
        if source.lower() != "worldometers" or category.lower() != "population":
            return jsonify({"code": 400,
                            "error": "Unsupported source or category",
                            "source": source,
                            "category": category,
                            "target": target
                            }), 400

        data = scrape_country_population(country)
        return jsonify({"data": data})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        # Log full traceback for debugging
        print("[ERROR]", traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500
        
@app.route("/")
def home():
    return render_template('index.html')  # loads src/templates/index.html

@app.route("/api")
def api():
    return render_template('api/index.html')  # loads src/templates/api/index.html
    
@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(debug=True)
