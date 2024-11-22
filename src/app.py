
from flask import Flask, Response, render_template
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Use 'Agg' backend for rendering plots without a GUI
import seaborn as sns
import os
import io


# Define the folder where the output .csv files are stored
output_directory = "/PATH/TO/output_queries"

# Check if the output directory exists, exit if not
if not os.path.exists(output_directory):
    print(f"Error: Directory '{output_directory}' does not exist.")
    exit()

# Function to load data from a CSV file
def load_data(file_name):
    """
    Load data from a CSV file located in the output directory.
    Args:
        file_name (str): Name of the CSV file to load.
    Returns:
        pd.DataFrame or None: Loaded data as a Pandas DataFrame, or None if the file doesn't exist.
    """
    file_path = os.path.join(output_directory, file_name)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"Error: File '{file_name}' not found in '{output_directory}'.")
        return None

# Plotting and Visualization Functions

# 1. User Engagement Reports - Daily User Activity
def plot_user_activity_heatmap():
    """
    Generate a heatmap of daily user activity by type.
    Data is loaded from query_1_results.csv.
    Returns:
        io.BytesIO: PNG image of the heatmap, or None if data is missing.
    """
    df = load_data("query_1_results.csv")
    if df is not None:
        pivot_df = df.pivot(index="activity_date", columns="activity_type", values="activity_count").fillna(0)

        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_df, annot=True, fmt="g", cmap="coolwarm", linewidths=0.5)
        plt.title("Daily User Activity by Type (Heatmap)", fontsize=16, weight="bold")
        plt.xlabel("Activity Type", fontsize=12, weight="bold")
        plt.ylabel("Date", fontsize=12, weight="bold")
        plt.tight_layout()

        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)
        return output
    else:
        print("Error: Data not loaded.")
    return None

# 2. Feedback Trends - Ratings Distribution
def plot_feedback_distribution():
    """
    Generate a bar chart showing the distribution of feedback ratings.
    Data is loaded from query_2_results.csv.
    Returns:
        io.BytesIO: PNG image of the bar chart, or None if data is missing.
    """
    df = load_data("query_2_results.csv")
    if df is not None:
        plt.figure(figsize=(8, 6))
        sns.barplot(data=df, x="rating", y="feedback_count", palette="viridis")
        plt.title("Feedback Ratings Distribution")
        plt.xlabel("Rating")
        plt.ylabel("Number of Feedbacks")
        plt.tight_layout()

        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)
        return output
    return None

# 3. Rewards Program Participation - Points Earned vs Redeemed
def plot_rewards_participation():
    """
    Generate a stacked bar chart showing rewards points earned vs. redeemed for users.
    Data is loaded from query_3_results.csv.
    Returns:
        io.BytesIO: PNG image of the bar chart, or None if data is missing.
    """
    df = load_data("query_3_results.csv")
    if df is not None:
        df = df.sort_values(by="user_id")
        df_pivot = df.melt(id_vars="user_id", value_vars=["total_points_earned", "total_points_redeemed"],
                           var_name="Point Type", value_name="Points")
        
        plt.figure(figsize=(12, 8))
        sns.barplot(data=df_pivot, x="user_id", y="Points", hue="Point Type", palette="viridis")
        plt.title("Rewards Program Participation (Stacked Bar Chart)", fontsize=16, weight="bold")
        plt.xlabel("User ID", fontsize=12, weight="bold")
        plt.ylabel("Total Points", fontsize=12, weight="bold")
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()

        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)
        return output
    return None

# 4. Ticket Resolution Metrics - Ticket Submission Rates
def plot_ticket_submission_rates():
    """
    Generate a bar chart showing ticket submission rates by category.
    Data is loaded from query_4_results.csv.
    Returns:
        io.BytesIO: PNG image of the bar chart, or None if data is missing.
    """
    df = load_data("query_4_results.csv")
    if df is not None:
        plt.figure(figsize=(8, 6))
        sns.barplot(data=df, x="category", y="ticket_count", palette="coolwarm")
        plt.title("Ticket Submission Rates by Category")
        plt.xlabel("Category")
        plt.ylabel("Number of Tickets")
        plt.tight_layout()

        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)
        return output
    return None

# 5. Ticket Resolution Metrics - Average Resolution Time
def plot_avg_resolution_time():
    """
    Generate a bar chart showing average resolution times for tickets by category.
    Data is loaded from query_5_results.csv.
    Returns:
        io.BytesIO: PNG image of the bar chart, or None if data is missing.
    """
    df = load_data("query_5_results.csv")
    if df is not None:
        plt.figure(figsize=(8, 6))
        sns.barplot(data=df, x="category", y="avg_resolution_time", palette="magma")
        plt.title("Average Resolution Time by Ticket Category")
        plt.xlabel("Category")
        plt.ylabel("Average Resolution Time (Hours)")
        plt.tight_layout()

        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)
        return output
    return None

# 6. Ticket Resolution Metrics - Status Distribution
def plot_ticket_status_distribution():
    """
    Generate a pie chart showing the distribution of ticket statuses.
    Data is loaded from query_6_results.csv.
    Returns:
        io.BytesIO: PNG image of the pie chart, or None if data is missing.
    """
    df = load_data("query_6_results.csv")
    if df is not None:
        plt.figure(figsize=(8, 8))
        plt.pie(
            df["ticket_count"], 
            labels=df["status"], 
            autopct="%1.1f%%", 
            startangle=140, 
            colors=sns.color_palette("coolwarm", len(df))
        )
        plt.title("Ticket Status Distribution")
        plt.tight_layout()

        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)
        return output
    return None

# 7. Content Interaction Analytics - Popular Content Types
def plot_content_type_interaction():
    """
    Generate a bar chart showing the number of interactions for each content type.
    Data is loaded from query_7_results.csv.
    Returns:
        io.BytesIO: PNG image of the bar chart, or None if data is missing.
    """
    # Load the data for content interaction by type
    df = load_data("query_7_results.csv")
    if df is not None:
        # Set up the figure size for the plot
        plt.figure(figsize=(8, 6))
        
        # Create a bar chart with Seaborn
        sns.barplot(data=df, x="content_type", y="interaction_count", palette="crest")
        
        # Add title and axis labels to the chart
        plt.title("Content Interaction by Type")
        plt.xlabel("Content Type")
        plt.ylabel("Number of Interactions")
        
        # Adjust layout to prevent clipping of titles or labels
        plt.tight_layout()
        
        # Save the plot as a PNG image to a bytes buffer
        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)  # Move the pointer to the start of the buffer for reading
        return output
    return None  # Return None if data is not available

# 8. Content Interaction Analytics - Content Interaction by Category
def plot_content_category_interaction():
    """
    Generate a bar chart showing the number of interactions for each content category.
    Data is loaded from query_8_results.csv.
    Returns:
        io.BytesIO: PNG image of the bar chart, or None if data is missing.
    """
    # Load the data for content interaction by category
    df = load_data("query_8_results.csv")
    if df is not None:
        # Set up the figure size for the plot
        plt.figure(figsize=(8, 6))
        
        # Create a bar chart with Seaborn
        sns.barplot(data=df, x="category", y="interaction_count", palette="coolwarm")
        
        # Add title and axis labels to the chart
        plt.title("Content Interaction by Category")
        plt.xlabel("Category")
        plt.ylabel("Number of Interactions")
        
        # Adjust layout to prevent clipping of titles or labels
        plt.tight_layout()
        
        # Save the plot as a PNG image to a bytes buffer
        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)  # Move the pointer to the start of the buffer for reading
        return output
    return None  # Return None if data is not available

# 9. Content Interaction Analytics - Top Content
def plot_top_content_items():
    """
    Generate a bar chart showing the most popular content items by number of interactions.
    Data is loaded from query_9_results.csv.
    Returns:
        io.BytesIO: PNG image of the bar chart, or None if data is missing.
    """
    # Load the data for top content items
    df = load_data("query_9_results.csv")
    if df is not None:
        # Sort the data in descending order of interaction count
        df = df.sort_values(by="interaction_count", ascending=False)
        
        # Set up the figure size for the plot
        plt.figure(figsize=(10, 8))
        
        # Create a bar chart with Seaborn
        sns.barplot(data=df, x="interaction_count", y="title", palette="viridis")
        
        # Add title and axis labels to the chart
        plt.title("Top Content Items by Interactions")
        plt.xlabel("Number of Interactions")
        plt.ylabel("Content Title")
        
        # Adjust layout to prevent clipping of titles or labels
        plt.tight_layout()
        
        # Save the plot as a PNG image to a bytes buffer
        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)  # Move the pointer to the start of the buffer for reading
        return output
    return None  # Return None if data is not available

# 10. Overall Data Visualization - Engagement Trends
def plot_engagement_trends():
    """
    Generate a line chart showing overall user engagement trends over time.
    Data is loaded from query_10_results.csv.
    Returns:
        io.BytesIO: PNG image of the line chart, or None if data is missing.
    """
    # Load the data for engagement trends
    df = load_data("query_10_results.csv")
    if df is not None:
        # Set up the figure size for the plot
        plt.figure(figsize=(10, 6))
        
        # Create a line chart with Seaborn
        sns.lineplot(data=df, x="activity_date", y="total_activities", marker="o", color="green")
        
        # Add title and axis labels to the chart
        plt.title("Overall User Engagement Trends")
        plt.xlabel("Date")
        plt.ylabel("Total Activities")
        
        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Adjust layout to prevent clipping of titles or labels
        plt.tight_layout()
        
        # Save the plot as a PNG image to a bytes buffer
        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)  # Move the pointer to the start of the buffer for reading
        return output
    return None  # Return None if data is not available

# 11. Overall Data Visualization - System Performance Heatmap
def plot_system_performance_heatmap():
    """
    Generate a heatmap showing system performance metrics over time.
    Data is loaded from query_14_results.csv.
    Returns:
        io.BytesIO: PNG image of the heatmap, or None if data is missing.
    """
    # Load the data for system performance
    df = load_data("query_14_results.csv")
    if df is not None:
        # Pivot the data to prepare for heatmap plotting
        pivot_df = df.pivot(index="activity_date", columns="category", values="performance_metric").fillna(0)
        
        # Set up the figure size for the plot
        plt.figure(figsize=(12, 6))
        
        # Create a heatmap with Seaborn
        sns.heatmap(pivot_df, annot=True, fmt=".1f", cmap="coolwarm", linewidths=0.5)
        
        # Add title and axis labels to the chart
        plt.title("System Performance Overview (Heatmap)")
        plt.xlabel("Category")
        plt.ylabel("Date")
        
        # Adjust layout to prevent clipping of titles or labels
        plt.tight_layout()
        
        # Save the plot as a PNG image to a bytes buffer
        output = io.BytesIO()
        plt.savefig(output, format="png")
        plt.close()
        output.seek(0)  # Move the pointer to the start of the buffer for reading
        return output
    return None  # Return None if data is not available


"""
# Call all the functions to generate visualizations
plot_user_activity_heatmap()
plot_feedback_distribution()
plot_rewards_participation()
plot_ticket_submission_rates()
plot_avg_resolution_time()
plot_ticket_status_distribution()
plot_content_type_interaction()
plot_content_category_interaction()
plot_top_content_items()
plot_engagement_trends()
plot_system_performance_heatmap()
"""

# Initialize the Flask application
app = Flask(__name__)

# Graph Function Wrappers for Flask
def generate_plot(plot_function):
    """
    Execute a plot function and return the resulting PNG image as a Flask response.
    Args:
        plot_function (function): The function that generates the plot.
    Returns:
        Response: Flask HTTP response containing the PNG image or an error message.
    """
    output = plot_function()  # Call the plotting function
    if output:
        # Return the PNG image as an HTTP response
        return Response(output.getvalue(), mimetype='image/png')
    else:
        # Return an error message if the plot could not be generated
        return "Error generating graph", 500

# Routes for Graphs

@app.route('/')
def index():
    """
    Render the dashboard homepage.
    This page serves as the entry point for the application.
    """
    return render_template('index.html')

@app.route('/user-activity')
def user_activity():
    """
    Render the page for the User Activity Heatmap.
    This page includes a link to the graph rendering route.
    """
    return render_template('graph.html', title="User Activity Heatmap", graph_url="/user-activity/plot")

@app.route('/user-activity/plot')
def user_activity_plot():
    """
    Generate and return the User Activity Heatmap.
    Returns:
        Response: PNG image or an error message if the plot fails to generate.
    """
    output = plot_user_activity_heatmap()  # Call the function to generate the heatmap
    if output:
        # Return the PNG image as an HTTP response
        return Response(output.getvalue(), mimetype='image/png')
    else:
        # Return an error message if the plot fails to generate
        return "Error generating graph", 500

@app.route('/feedback-distribution')
def feedback_distribution():
    """
    Render and display the Feedback Ratings Distribution graph.
    """
    return generate_plot(plot_feedback_distribution)

@app.route('/rewards-participation')
def rewards_participation():
    """
    Render and display the Rewards Program Participation graph.
    """
    return generate_plot(plot_rewards_participation)

@app.route('/ticket-submission-rates')
def ticket_submission_rates():
    """
    Render and display the Ticket Submission Rates graph.
    """
    return generate_plot(plot_ticket_submission_rates)

@app.route('/avg-resolution-time')
def avg_resolution_time():
    """
    Render and display the Average Resolution Time graph.
    """
    return generate_plot(plot_avg_resolution_time)

@app.route('/ticket-status-distribution')
def ticket_status_distribution():
    """
    Render and display the Ticket Status Distribution graph.
    """
    return generate_plot(plot_ticket_status_distribution)

@app.route('/content-type-interaction')
def content_type_interaction():
    """
    Render and display the Content Type Interaction graph.
    """
    return generate_plot(plot_content_type_interaction)

@app.route('/content-category-interaction')
def content_category_interaction():
    """
    Render and display the Content Category Interaction graph.
    """
    return generate_plot(plot_content_category_interaction)

@app.route('/top-content-items')
def top_content_items():
    """
    Render and display the Top Content Items graph.
    """
    return generate_plot(plot_top_content_items)

@app.route('/engagement-trends')
def engagement_trends():
    """
    Render and display the Engagement Trends graph.
    """
    return generate_plot(plot_engagement_trends)

@app.route('/system-performance-heatmap')
def system_performance_heatmap():
    """
    Render and display the System Performance Heatmap graph.
    """
    return generate_plot(plot_system_performance_heatmap)



# Main Entry Point
if __name__ == "__main__":
    # Run the Flask application in debug mode for development
    app.run(debug=True)

