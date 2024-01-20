from flask import Flask, jsonify, request, send_from_directory
from nltk.stem import WordNetLemmatizer, PorterStemmer
import psycopg2
from psycopg2 import sql, pool

app = Flask(__name__)

# Database connection parameters
db_params = {
    'dbname': 'search_engine_db',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

# Connection pool setup
min_connections = 1
max_connections = 5
connection_pool = psycopg2.pool.SimpleConnectionPool(minconn=min_connections, maxconn=max_connections, **db_params)

# NLTK components
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# Indexing function
def index_documents():
    documents = [
        (1, 'BIG DATA ANALYTICS', '{"Philip Russom"}', '2011-01-01', 'This document explores the concepts and applications of Big Data Analytics...', '{"Big Data", "Analytics"}', 'https://origin-tableau-www.tableau.com/sites/default/files/whitepapers/tdwi_bpreport_q411_big_data_analytics_tableau.pdf'),
        (2, 'Big Data Deep Learning Challenges and perspective', '{"XUE-WEN CHEN","XIAOTONG LIN"}', '2014-05-16', 'This paper discusses the challenges and perspectives of implementing Deep Learning techniques in Big Data environments...', '{"Deep Learning", "Challenges", "Perspective"}', 'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6817512'),
        (3, 'Big Data', '{"Seref SAGIROGLU","Duygu SINANC"}', '2013-01-13', 'This document provides an overview of Big Data technologies, applications, and challenges...', '{"Big Data", "Technologies", "Applications"}', 'https://academics.uccs.edu/~ooluwada/courses/datamining/ExtraReading/Big_data_A_review.pdf'),
        (4, 'Data Mining with Big Data', '{"Xindong Wu","Xingquan Zhu","Gong-Qing Wu","Wei Ding"}', '2013-03-01', 'This paper focuses on data mining techniques, algorithms, and applications in Big Data environments...', '{"Data Mining", "Big Data", "Techniques"}', 'https://d1wqtxts1xzle7.cloudfront.net/48232221/Data_Mining_with_Big_Data-libre.pdf?1471899772=&response-content-disposition=inline%3B+filename%3DData_Mining_with_Big_Data.pdf&Expires=1705682617&Signature=GlREk-ca06WmyZbhFmCbh9pe55w-DM257HB0bqTw3CiOcz4LPYJuF-6~PbpxTpK5F4IXzi4XR78NsDWvZD~YjG4AtI2tyLBTikIH3Ef-nWlWbuqXmEd2~GqeWRuDQMGx8azxu5S5QfHayTvSlvmUXJ5vT5VPVFLYLclSOgow9wC~PHx4~stG3agRdIM5~YAKePSvUbX5FuKm0KedoS~Xuma4RbVHFrGs0xcKLDW4sNTmqAAFwKQZrISdoP33~JUV495u4nmxDnnj9g4HRjH9T0u-Iw1stkiBRxfpgBnQplzwc54rEUHl2XcWsfrQkNrO7KJABGkmZ-kHhwjK3EfgYQ__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA'),
        (5, 'Machine learning and deep learning', '{"Christian Janiesch","Patrick Zschech","Kai Heinrich"}', '2021-04-08', 'This document explores machine learning and deep learning concepts, algorithms, and applications...', '{"Machine Learning", "Deep Learning", "Algorithms"}', 'https://link.springer.com/content/pdf/10.1007/s12525-021-00475-2.pdf'),
        (6, 'Machine learning', '{"M. I. Jordan","T. M. Mitchell"}', '2015-07-20', 'This paper focuses on machine learning algorithms, methodologies, and applications...', '{"Machine Learning", "Algorithms", "Applications"}', 'https://cs.pomona.edu/~dkauchak/classes/s16/cs30-s16/lectures/lecture12-NN-basics.pdf'),
        (7, 'Recent advances in deep learning', '{"Xizhao Wang","Yanxia Zhao","Farhad Pourpanah"}', '2020-02-20', 'This paper discusses recent advances, trends, and innovations in deep learning research and applications...', '{"Deep Learning", "Advances", "Trends"}', 'https://link.springer.com/content/pdf/10.1007/s13042-020-01096-5.pdf'),
        (8, 'Data Analytics', '{"Thomas A. Runkler"}', '2012-08-05', 'This document provides insights into data analytics techniques, tools, and applications...', '{"Data Analytics", "Techniques", "Tools"}', 'http://103.62.146.201:8081/xmlui/bitstream/handle/1/5555/Data%20Analytics.pdf?sequence=1'),
        (9, 'Artificial Intelligence', '{"Michael H. Goldwasser"}', '2013-08-27', 'Fundamental introduction to the broad area of artificial intelligence and its applications. Topics include knowledge representation, logic, search spaces, reasoning with uncertainty, and machine learning', '{"Artificial Intelligence", "Computing","IA"}', 'https://cs.slu.edu/~goldwasser/362/handouts/course-info.pdf'),
        (10, 'CLOUD COMPUTING BASICS', '{"J.SRINIVAS", "K.VENKATA SUBBA REDDY","Dr.A.MOIZ QYSER"}', '2012-07-05', 'This document provides an introduction to the concepts and applications of cloud computing...', '{"Cloud Computing", "Concepts", "Applications"}', 'https://www.researchgate.net/profile/Srinivas-Jagirdar/publication/255994786_CLOUD_COMPUTING_BASICS/links/0c96052159b1a04dac000000/CLOUD-COMPUTING-BASICS.pdf'),
        (11, 'Effective cybersecurity: understanding and using standards and best practices', '{"William Stallings"}', '2018-06-28', 'Explore best practices and strategies for maintaining cybersecurity in modern IT environments...', '{"Cybersecurity", "Standards", "Best Practices", "Strategies"}', 'https://thuvienso.hoasen.edu.vn/bitstream/handle/123456789/11994/Contents.pdf?sequence=1'),
        (12, 'Advances and opportunities in materials science for scalable quantum computing', '{"Vincenzo Lord", "John M. Nichol"}', '2021-07-02', 'Explore recent advances and developments in the field of quantum computing...', '{"Quantum Computing", "Advances", "Developments"}', 'https://link.springer.com/content/pdf/10.1557/s43577-021-00133-0.pdf')
    ]

    with connection_pool.getconn() as conn, conn.cursor() as cursor:
        for document in documents:
            cursor.execute(
                """
                INSERT INTO public.docs (id, title, authors, publication_date, abstract, keywords, link)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    authors = EXCLUDED.authors,
                    publication_date = EXCLUDED.publication_date,
                    abstract = EXCLUDED.abstract,
                    keywords = EXCLUDED.keywords,
                    link = EXCLUDED.link;
                """,
                document
            )

        # Commit the transaction to save changes to the database
        conn.commit()
        # Release the connection back to the pool
        connection_pool.putconn(conn)

# Call the index_documents function to insert documents into the database
index_documents()

# Search endpoint
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    # Lemmatize the query
    lemmatized_query = ' '.join(lemmatizer.lemmatize(word) for word in query.split())

    # Perform anti-dictionary operation
    anti_dict_query = anti_dictionary_operation(lemmatized_query)

    # Perform stemming
    stemmed_query = ' '.join(stemmer.stem(word) for word in anti_dict_query.split())

    with connection_pool.getconn() as conn, conn.cursor() as cursor:
        try:
            # Your search logic here
            # Use the processed query in your SQL query
            search_query = sql.SQL("""
                    SELECT * FROM docs
                    WHERE similarity(title, %s) > 0.3
                    OR EXISTS (
                        SELECT 1
                        FROM unnest(authors) AS author
                        WHERE similarity(author, %s) > 0.3
                    )
                    OR EXISTS (
                        SELECT 1
                        FROM unnest(keywords) AS keyword
                        WHERE similarity(keyword, %s) > 0.3
                    )
                    OR levenshtein(%s::text, title::text) <= 3  -- Adjust the distance threshold as needed
                    OR EXISTS (
                        SELECT 1
                        FROM unnest(authors) AS author
                        WHERE levenshtein(author::text, %s::text) <= 3  -- Adjust the distance threshold as needed
                    )
                    OR EXISTS (
                        SELECT 1
                        FROM unnest(keywords) AS keyword
                        WHERE levenshtein(keyword::text, %s::text) <= 3  -- Adjust the distance threshold as needed
                    )
                    OR similarity(title, %s) > 0.1  -- Trigram similarity for title
                    OR EXISTS (
                        SELECT 1
                        FROM unnest(authors) AS author
                        WHERE similarity(author, %s) > 0.1  -- Trigram similarity for authors
                    )
                    OR EXISTS (
                        SELECT 1
                        FROM unnest(keywords) AS keyword
                        WHERE similarity(keyword, %s) > 0.1  -- Trigram similarity for keywords
                    );
            """)
            cursor.execute(search_query, (stemmed_query, stemmed_query, stemmed_query, stemmed_query, stemmed_query, stemmed_query, stemmed_query, stemmed_query, stemmed_query))

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
                    'keywords': result[5],
                    'link': result[6]
                }
                results_json.append(result_dict)

            return jsonify(results_json)

        except Exception as e:
            # Roll back the transaction in case of an error
            conn.rollback()
            print(f"Error: {e}")
            return jsonify({"error": "An error occurred during the search."}), 500
        finally:
            # Release the connection back to the pool
            connection_pool.putconn(conn)

# Implement your anti-dictionary operation here
def anti_dictionary_operation(query):
    # Terms to be excluded from the search
    exclude_terms = ['Big Data', 'Deep Learning', 'Machine Learning']

    # Remove excluded terms
    for term in exclude_terms:
        query = query.replace(term, '')

    return query

# Serve static files (index.html, styles.css, app.js)
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)