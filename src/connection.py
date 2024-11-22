import mysql.connector
import pandas as pd
import os

# Define the base directory where the script and the "queries.sql" file are located
base_dir = "/Users/amir/Desktop/GreenGrove"

# Define the output directory relative to the base directory
# This directory will store the query results as CSV files
output_directory = os.path.join(base_dir, "output_queries")

# Ensure the output directory exists; create it if it doesn't
os.makedirs(output_directory, exist_ok=True)

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",       # Replace with your MySQL server host (e.g., localhost, IP address)
    user="yourusername",            # Replace with your MySQL username
    password="yourpassword",  # Replace with your MySQL password
    database="DATABASE"  # Replace with your target database name
)

# Check if the database connection was successful
if connection.is_connected():
    print("Connected to MySQL database")
    
    try:
        # Path to the SQL file containing the queries
        sql_file_path = os.path.join(base_dir, "queries.sql")

        # Open the SQL file and read its contents
        with open(sql_file_path, 'r') as file:
            # Split the file into individual queries using ';' as a delimiter
            queries = file.read().split(';')

        # Create a cursor object for executing SQL commands
        cursor = connection.cursor()

        # Loop through each query in the list
        for idx, query in enumerate(queries):
            query = query.strip()  # Remove any leading or trailing whitespace from the query
            if query:  # Skip empty queries (in case of extra semicolons in the SQL file)
                try:
                    # Execute the current query
                    cursor.execute(query)

                    # Extract column names from the query results
                    columns = [desc[0] for desc in cursor.description]

                    # Fetch all rows of data returned by the query
                    data = cursor.fetchall()

                    # Convert the fetched data into a Pandas DataFrame
                    result_df = pd.DataFrame(data, columns=columns)

                    # Define the path to save the CSV file for the current query
                    csv_file_path = os.path.join(output_directory, f"query_{idx + 1}_results.csv")

                    # Save the DataFrame to a CSV file
                    result_df.to_csv(csv_file_path, index=False)
                    print(f"Query {idx + 1} executed successfully and saved to '{csv_file_path}'")
                except Exception as e:
                    # Handle any errors that occur during query execution
                    print(f"Error executing query {idx + 1}: {e}")

    except FileNotFoundError as e:
        # Handle the case where the SQL file is not found
        print(f"SQL file not found: {e}")
    except Exception as e:
        # Handle any other errors while reading the SQL file
        print(f"An error occurred while processing the SQL file: {e}")

    # Close the cursor and database connection after processing all queries
    cursor.close()
    connection.close()
    print("Connection closed.")
else:
    # Print an error message if the database connection fails
    print("Failed to connect to MySQL database")
