from flask import Flask, jsonify, request, render_template
from scrapers.worldometers.scrape import scrape_country_population  # make sure folder name matches
import traceback
from routes import population_bp

app = Flask(__name__, template_folder='./templates')    
app.register_blueprint(population_bp)

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
