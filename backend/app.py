from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database connection details
DB_CONFIG = {
    "dbname": "WellsData",
    "user": "teamc-admin",
    "password": "123456",  # Update with secure credentials
    "host": "127.0.0.1",   # Change to Google Cloud instance if needed
    "port": "5432"
}

def get_db_connection():
    """Establish connection to PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


# **1️⃣ Total Oil Production Over Time**
@app.route('/api/trends', methods=['GET'])
def get_trends():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """SELECT "Year", SUM("Total_Wells_Annual_Oil_Production") AS total_oil_production
                   FROM well_data GROUP BY "Year" ORDER BY "Year";"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{"year": row[0], "total_oil_production": row[1]} for row in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# **2️⃣ Wells Per State**
@app.route('/api/wells-per-state', methods=['GET'])
def get_wells_per_state():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """SELECT "State", SUM("Total_Wells") AS total_wells
                   FROM well_data GROUP BY "State" ORDER BY total_wells DESC;"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{"state": row[0], "total_wells": row[1]} for row in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# **3️⃣ Most & Least Producing States**
@app.route('/api/most-least-producing', methods=['GET'])
def get_most_least_producing():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """SELECT "State", SUM("Total_Wells_Annual_Oil_Production") AS total_oil_production
                   FROM well_data GROUP BY "State" ORDER BY total_oil_production DESC;"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        top_5 = data[:5]
        bottom_5 = data[-5:]
        return jsonify({"most_producing": top_5, "least_producing": bottom_5})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
