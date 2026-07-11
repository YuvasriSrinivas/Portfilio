from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
CORS(app)

# Database Configuration Variables
DB_SETTINGS = {
    'host': 'localhost',
    'user': 'root',          # Default MySQL user is usually 'root'
    'password': 'vasu@123'  # Replace with your actual MySQL password
}
DB_NAME = 'portfolio_db'

def initialize_database():
    """Connects to MySQL server, creates the database and table if missing."""
    try:
        # Connect to server without a specific database
        conn = mysql.connector.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        
        # 1. Dynamically generate database if missing
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # 2. Dynamically generate table if missing
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hire_submissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                system_tier VARCHAR(50) NOT NULL,
                company VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                project_scale TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.close()
        conn.close()
        print(f"--> Database Matrix Verified: '{DB_NAME}' engine is online.")
    except mysql.connector.Error as err:
        print(f"Critical Database Setup Error: {err}")
        exit(1)

def get_db_connection():
    """Standard runtime database connection pooler."""
    return mysql.connector.connect(
        **DB_SETTINGS,
        database=DB_NAME
    )

@app.route('/api/hire', methods=['POST'])
def handle_hire_intake():
    try:
        data = request.json
        system_tier = data.get('system_tier')
        company = data.get('company')
        email = data.get('email')
        project_scale = data.get('project_scale')

        if not company or not email or not project_scale:
            return jsonify({"status": "error", "message": "Missing required parameters."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO hire_submissions (system_tier, company, email, project_scale)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (system_tier, company, email, project_scale))
        conn.commit()
        
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "Data written cleanly to database layer."}), 201

    except Exception as e:
        print(f"Runtime Exception: {e}")
        return jsonify({"status": "error", "message": "Internal structural engine failure."}), 500

if __name__ == '__main__':
    # Initialize infrastructure before exposing port
    initialize_database()
    app.run(debug=True, port=5000)