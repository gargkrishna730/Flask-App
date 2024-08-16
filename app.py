from flask import Flask, jsonify, request
from pymongo import MongoClient, errors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        client = MongoClient('mongodb+srv://DipenRodda:Dipen123@cluster0.gkzq5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        db = client['Assignment']
        collection = db['Assgn']
    except errors.ServerSelectionTimeoutError as err:
        return jsonify({"error": "Database connection failed", "details": str(err)}), 500

    filters = {}
    if request.args:
        for key in ['end_year', 'topic', 'sector', 'region', 'pestle', 'source', 'swot', 'country', 'city']:
            value = request.args.get(key)
            if value:
                filters[key] = value

    try:
        data = list(collection.find(filters, {'_id': 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Failed to retrieve data", "details": str(e)}), 500

if __name__ == '__main__':
    # Use 0.0.0.0 to make the app accessible externally
    app.run(host='0.0.0.0', port=5000, debug=False)  # Set debug to False in production