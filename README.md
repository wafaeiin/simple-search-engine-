
```markdown
# Search Engine Project

This project is a simple search engine built using Flask and PostgreSQL. It allows users to search for documents based on their titles.

## Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/wafaeiin/search-engine-project.git
   cd search-engine-project
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the PostgreSQL database:**

   - Create a PostgreSQL database named `search_engine_db`.
   - Update the database connection parameters in `app.py` to match your PostgreSQL setup.

      ```python
      # app.py
      db_params = {
          'dbname': 'search_engine_db',
          'user': 'postgres',
          'password': 'admin', 
          'host': 'localhost',
          'port': '5432'
      }
      ```

   - Run the following command to create the database schema:

      ```bash
      psql -U postgres -d search_engine_db -a -f create_tables.sql
      ```

   - Run the following command to insert sample data into the database:

      ```bash
      psql -U postgres -d search_engine_db -a -f init_data.sql
      ```

## Deployment

### Running with Waitress (Production Server)

To run your Flask application with Waitress, follow these steps:

1. Install Waitress:

   ```bash
   pip install waitress
   ```

2. Run the application:

   ```bash
   waitress-serve --listen=0.0.0.0:5500 app:app
   ```

   This command starts the Waitress server and binds it to port 5500. The application will be accessible at [http://0.0.0.0:5500](http://0.0.0.0:5500).

### Running with Flask Development Server (For Testing)

During development, you can use the Flask development server:

```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to access the application.


## Usage

1. Open the web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).
2. Enter your search query in the input field and click the "Search" button.
3. View the search results displayed on the page.

## Project Structure

- `app.py`: Main Flask application file.
- `static/`: Folder containing static files (HTML, CSS, JS).
- `requirements.txt`: List of Python dependencies.


## License

This project is licensed under the [MIT License](LICENSE).
```
