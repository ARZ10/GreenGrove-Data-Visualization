import os
import mysql.connector
import tempfile
import pytest

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'test_user',  # Update with your database test user
    'password': 'password',  # Update with your database password
    'database': 'GreenGroveDB'
}

# Utility function to execute queries
def execute_query(query, fetch_results=True):
    """
    Executes a SQL query on the database.
    Args:
        query (str): The SQL query to execute.
        fetch_results (bool): Whether to fetch and return the results.
    Returns:
        List[Dict]: Query results if `fetch_results` is True, else None.
    """
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        if fetch_results:
            return cursor.fetchall()
        connection.commit()
    finally:
        connection.close()

# Setup and teardown for tests
@pytest.fixture(scope="function")
def setup_teardown():
    """
    Pytest fixture to set up and tear down the database environment for tests.
    Creates necessary tables and cleans up after tests.
    """
    # Setup: Create necessary tables
    execute_query("""
        CREATE TABLE IF NOT EXISTS ActivityLog (
            activity_type VARCHAR(50),
            activity_date DATE
        );
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS Feedback (
            rating INT
        );
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS Rewards (
            user_id INT,
            points_earned INT,
            points_redeemed INT
        );
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS support_ticket (
            category VARCHAR(50),
            created_at DATE,
            updated_at DATE,
            status VARCHAR(50)
        );
    """)
    yield  # Run the test
    # Teardown: Drop the tables
    execute_query("DROP TABLE IF EXISTS ActivityLog;")
    execute_query("DROP TABLE IF EXISTS Feedback;")
    execute_query("DROP TABLE IF EXISTS Rewards;")
    execute_query("DROP TABLE IF EXISTS support_ticket;")

# Test cases
def test_activity_summary(setup_teardown):
    """
    Test user activity summary query for accuracy.
    """
    execute_query("""
        INSERT INTO ActivityLog (activity_type, activity_date)
        VALUES ('Login', '2024-11-01'), ('Purchase', '2024-11-01');
    """, fetch_results=False)
    result = execute_query("""
        SELECT activity_type, COUNT(*) AS activity_count
        FROM ActivityLog
        GROUP BY activity_type;
    """)
    assert len(result) == 2
    assert result[0]['activity_count'] > 0

def test_feedback_trends(setup_teardown):
    """
    Test feedback trends query for correct group counts.
    """
    execute_query("""
        INSERT INTO Feedback (rating)
        VALUES (5), (4), (4), (3);
    """, fetch_results=False)
    result = execute_query("""
        SELECT rating, COUNT(*) AS count
        FROM Feedback
        GROUP BY rating;
    """)
    assert len(result) == 3
    assert result[0]['count'] > 0

def test_rewards_program(setup_teardown):
    """
    Test rewards program participation query for aggregation accuracy.
    """
    execute_query("""
        INSERT INTO Rewards (user_id, points_earned, points_redeemed)
        VALUES (1, 100, 50), (1, 50, 20), (2, 200, 150);
    """, fetch_results=False)
    result = execute_query("""
        SELECT user_id, SUM(points_earned) AS total_points_earned
        FROM Rewards
        GROUP BY user_id;
    """)
    assert len(result) == 2
    assert result[0]['total_points_earned'] > 0

def test_ticket_submission_rates(setup_teardown):
    """
    Test ticket submission rates query for percentage calculations.
    """
    execute_query("""
        INSERT INTO support_ticket (category)
        VALUES ('Technical'), ('Billing'), ('Technical'), ('General');
    """, fetch_results=False)
    result = execute_query("""
        SELECT category, COUNT(*) AS ticket_count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM support_ticket), 2) AS percentage
        FROM support_ticket
        GROUP BY category;
    """)
    assert len(result) == 3
    assert result[0]['percentage'] > 0

def test_python_query_execution():
    """
    Test Python script execution to generate output files.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['OUTPUT_DIR'] = temp_dir
        os.system("python read_queries_execute.py")
        assert len(os.listdir(temp_dir)) > 0

def test_error_handling():
    """
    Test Python script error handling for invalid queries.
    """
    # Corrupt the SQL file temporarily
    sql_file = "queries.sql"
    with open(sql_file, 'a') as file:
        file.write("\nINVALID QUERY HERE;")
    try:
        # Run the Python script
        os.system("python read_queries_execute.py")
        # Check if error is logged without crash
        with open('logs.txt', 'r') as file:
            logs = file.read()
        assert "Error" in logs
    finally:
        # Clean up corrupted SQL file
        with open(sql_file, 'r') as file:
            lines = file.readlines()
        with open(sql_file, 'w') as file:
            file.writelines(lines[:-1])

def test_daily_user_engagement(setup_teardown):
    """
    Test daily user engagement query for correct counts.
    """
    execute_query("""
        INSERT INTO ActivityLog (activity_date)
        VALUES ('2024-11-01'), ('2024-11-01'), ('2024-11-02');
    """, fetch_results=False)
    result = execute_query("""
        SELECT activity_date, COUNT(*) AS daily_total
        FROM ActivityLog
        GROUP BY activity_date;
    """)
    assert len(result) == 2
    assert result[0]['daily_total'] > 0

def test_popular_content(setup_teardown):
    """
    Test content analytics query for most popular content.
    """
    execute_query("""
        CREATE TABLE Content (content_id INT, interactions INT);
    """)
    execute_query("""
        INSERT INTO Content (content_id, interactions)
        VALUES (1, 100), (2, 50), (3, 150);
    """, fetch_results=False)
    result = execute_query("""
        SELECT content_id
        FROM Content
        ORDER BY interactions DESC;
    """)
    assert len(result) == 3
    assert result[0]['content_id'] == 3
    execute_query("DROP TABLE IF EXISTS Content;")

# Main entry point for running tests
if __name__ == "__main__":
    pytest.main()
