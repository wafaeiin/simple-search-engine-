from flask import Flask, jsonify, request, send_from_directory
import psycopg2

app = Flask(__name__)

# Database connection parameters
db_params = {
    'dbname': 'search_engine_db',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

# Connect to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Indexing function
def index_documents():
    # Your indexing logic here
    pass

# Search endpoint
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    # Your search logic here
    cursor.execute("SELECT * FROM docs WHERE title ILIKE %s;", ('%' + query + '%',))
    results = cursor.fetchall()

    # Convert results to JSON format
    results_json = []
    for result in results:
        result_dict = {
            'id': result[0],
            'title': result[1],
            'authors': result[2],
            'publication_date': result[3].isoformat() if result[3] else None,
            'abstract': result[4],
            'keywords': result[5]
        }
        results_json.append(result_dict)

    return jsonify(results_json)

# Serve static files (index.html, styles.css, app.js)
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
