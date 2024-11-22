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


