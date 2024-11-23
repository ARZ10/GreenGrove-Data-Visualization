# GreenGrove Data Visualization Dashboard

The GreenGrove Data Visualization Dashboard is a robust web-based platform designed to provide actionable insights into user engagement, feedback trends, rewards program analytics, ticket resolution metrics, and content interaction patterns. Built with Flask as the backend framework, the project integrates advanced data visualization libraries to create interactive and meaningful representations of key metrics.

---

## Key Features

- **Comprehensive Analytics**:
  - Gain insights into user activity, feedback distribution, ticket handling metrics, and rewards program participation.
- **Dynamic Visualizations**:
  - Generate interactive heatmaps, bar charts, and line graphs using Matplotlib and Seaborn.
- **Data Export**:
  - Download analytical query results in CSV format for further processing.
- **API Integration**:
  - Access visualizations and raw data via dedicated REST API endpoints.
- **Responsive and Intuitive Design**:
  - A clean and accessible dashboard interface optimized for various devices.

---

## Project Structure

```plaintext
GreenGrove/
├── output_queries/         # CSV files generated from SQL queries
├── src/                    # Source code for the backend logic
│   ├── app.py              # Main Flask application
│   ├── API.py              # REST API for handling visualizations
│   ├── connection.py       # Database connection and query execution logic
│   ├── queries.sql         # SQL scripts for data analytics
├── templates/              # HTML templates for rendering the dashboard
│   ├── index.html          # Dashboard homepage
│   ├── graph.html          # Graph-specific page for visualizations
├── test/                   # Unit and integration tests
│   ├── test.py             # Pytest-based testing scripts
├── .gitignore              # Git ignore file to exclude unnecessary files
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```
---

# Installation Guide

## Prerequisites
To deploy and run this project, ensure the following dependencies are installed:

- Python 3.8 or higher
- MySQL database server
- Git for version control

## Deployment Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/ARZ10/GreenGrove-Data-Visualization.git
   cd GreenGrove-Data-Visualization
   ```
---

## Create and Activate a Virtual Environment

To set up the Python environment, run the following commands:
```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

---

## Install the Project Dependencies

Install the necessary dependencies using:
```bash
pip install -r requirements.txt
```
---
## Set Up the Database

Create a database named GreenGrovePortal in MySQL.
Run the queries.sql script (located in the src/ directory) to generate the required database schema.

---
## Launch the Flask Application

Start the Flask application using the command:
```bash
python src/app.py
```
---

## Access the Dashboard

After starting the application, open your browser and navigate to:
```bash
http://127.0.0.1:5000
```
---

## Usage Instructions

### Dashboard Access
- Navigate to the homepage to explore available visualizations.
- Select a visualization link to view the corresponding graph or chart.

---
## API Endpoints

The REST API provides programmatic access to both raw data and visualizations.

Example Endpoints:
/api/user-activity/graph: Heatmap of user activity
/api/feedback-trends/graph: Feedback ratings distribution
Refer to the API documentation for a comprehensive list of endpoints.

---
## Exporting Data

Visualized data can be exported as CSV files from the output_queries/ directory.
---

## Testing and Validation

To ensure the robustness of the application, unit tests are included. Run the test suite as follows:
```bash
pytest test/
```
Ensure the database and environment variables are correctly configured before running tests.
---


## Environment Variables Configuration

This project uses a .env file to manage sensitive credentials and environment-specific configurations. Create a .env file in the root directory with the following structure:

```plaintext
DB_HOST=localhost
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=GreenGrovePortal
OUTPUT_DIR=output_queries
```

---
## The project leverages the following technologies:

- Backend: Flask
- Database: MySQL
- Data Visualization: Matplotlib, Seaborn
- Data Processing: Pandas
- Testing Framework: Pytest
- Frontend: HTML, CSS

