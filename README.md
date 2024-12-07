# cis6930fa24 -- Project 3

Name: Pradhyumna Reddy Madhulapally

# Project Description

This project extends the original Norman PD incident analysis tool by providing a web interface for visualizing incident data. The application allows users to analyze incident reports from the Norman, Oklahoma police department through interactive visualizations, supporting both URL submissions and file uploads of PDF incident reports.

# Features

- Web-based interface for data submission
- Support for both URL and file upload inputs
- Interactive data visualizations:
    - Clustering analysis of incidents by location and nature
    - Top 15 most frequent incident types
    - Heatmap of incidents across locations
- Real-time data processing
- SQLite database storage
- Error handling and user feedback

# Project Structure

```bash
cis6930fa24-project3/
├── src/
│   ├── core/
│   │   └── project0.py
│   ├── visualization/
│   │   └── visualizations.py
│   └── web/
│       ├── app.py
│       └── templates/
│           └── index.html
├── tests/
│   └── test_project.py
└── README.md
```

# How to install 

```bash
# Install dependencies
pipenv install flask matplotlib scikit-learn numpy pandas seaborn pypdf

```

# How to run

```bash
# Start the web server
pipenv run python src/web/app.py
```
Access the interface at http://localhost:5001

# Testing

```bash
# Start the web server
# Run all tests
pipenv run pytest

# Run with verbose output
pipenv run pytest -v
```

<br />
![video](https://youtu.be/m8eKV--7VoY)

<br/>



# Functions


project0.py

1. fetchincidents(url)
    - Parameters: URL string for PDF fetch
    - Returns: String with extracted text data

2. extractincidents(data)
    - Parameters: Raw text data from PDF
    - Returns: List of parsed incidents

3. parse_incident(line)
    - Parameters: Single line of incident data
    - Returns: List of fields or None if invalid

4. createdb()
    - Creates: SQLite database with incidents table
    - Returns: Database connection object

5. populatedb(conn, incidents)
    - Parameters: Database connection and incident list
    - Action: Inserts incidents into database

visualizations.py Functions:

1. visualize_data(incidents)
- Parameters:
    - incidents: List of incidents, each containing [time, number, location, nature, ORI]
- What it does:
    - Creates DBSCAN clustering of incidents by location and nature
    - Generates bar graph of top 15 incident types
    - Produces heatmap of top 10 locations and incident types
- Returns:
    - List of matplotlib figure objects containing the three visualizations

app.py Functions:

1. convert_plot_to_base64(fig)
- Parameters:
    - fig: Matplotlib figure object
- What it does:
    - Converts matplotlib figure to base64 encoded string
    - Sets high DPI and proper formatting
- Returns:
    - Base64 encoded string of the figure

2. process_pdf_data(pdf_data)
- Parameters:
    - pdf_data: Binary PDF data from file upload or URL
- What it does:
    - Processes PDF data using PdfReader
    - Extracts text content with proper formatting
- Returns:
    - String containing extracted text from PDF

3. process_incidents()
- Parameters: None
- What it does:
    - Handles URL or file upload processing
    - Validates and extracts incident data
    - Creates database entries
    - Generates visualizations
- Returns:
    - JSON response with status, message, and visualization data

4. index()
- Parameters: None
- What it does:
    - Renders the main web interface
- Returns:
    - HTML template for the web interface


## Test Cases
1. test_fetch_incidents()
- Purpose: Tests the PDF fetching functionality from a URL
- What it tests:
    - Verifies successful data retrieval from a valid URL
    - Checks if returned data is either string or bytes type
    - Ensures non-null response

2. test_extract_incidents()
- Purpose: Tests the incident extraction from sample data
- What it tests:
    - Proper parsing of incident data format
    -  Verification of all required fields
    - Correct number of fields (5) in parsed output

3. test_database_creation()
- Purpose: Tests SQLite database initialization
- What it tests:
    - Successful database connection establishment
    - Proper table creation
    - Correct table name ('incidents') existence

4. test_database_population()
- Purpose: Tests database population with sample data
- What it tests:
    - Successful insertion of sample incidents
    - Row count verification
    - Database connection handling

5. test_visualization_generation()
- Purpose: Tests the generation of visualizations
- What it tests:
    - Creation of all three required visualizations
    - Proper figure object properties
    - Visualization saving capabilities

6. test_invalid_url()
- Purpose: Tests error handling for invalid URLs
- What it tests:
    - Exception raising for non-existent URLs
    - Proper error handling behavior

7. test_empty_data()
- Purpose: Tests handling of empty input data
- What it tests:
    - Proper handling of empty strings
    - Returns empty list for empty input

8. test_malformed_incident()
- Purpose: Tests handling of incorrect data format
- What it tests:
    - Processing of invalid incident data
    - Returns empty list for malformed input




## Assumptions and Limitations


- PDF reports follow consistent formatting
- Incident data contains standard fields
- File size limited to 16MB
- Requires stable internet connection for URL fetching

## Known Issues


- Format changes in PDF structure may affect parsing
- Multiple simultaneous uploads not supported
- PDF text extraction depends on consistent spacing

