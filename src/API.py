from flask import Flask, jsonify, Response, request
from flask_cors import CORS
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for cross-domain access
CORS(app)

# Mock data retrieval functions
# These functions simulate fetching data from a database or other storage.
# Replace them with actual database queries or API calls in a real application.

def load_user_activity_data():
    """
    Simulate loading user activity data.
    Returns:
        A Pandas DataFrame containing sample user activity data.
    """
    return pd.DataFrame({
        "activity_date": ["2024-01-01", "2024-01-02"],  # Dates of activities
        "activity_type": ["login", "upload"],           # Types of activities
        "activity_count": [10, 5],                      # Counts of each activity
    })

def load_feedback_data():
    """
    Simulate loading feedback trends data.
    Returns:
        A Pandas DataFrame containing sample feedback ratings and counts.
    """
    return pd.DataFrame({
        "rating": [1, 2, 3, 4, 5],                     # Feedback ratings (1 to 5)
        "feedback_count": [10, 20, 15, 5, 8],          # Number of feedbacks for each rating
    })

def load_rewards_data():
    """
    Simulate loading rewards program data.
    Returns:
        A Pandas DataFrame containing sample rewards data for users.
    """
    return pd.DataFrame({
        "user_id": [1, 2],                             # User IDs
        "points_earned": [100, 200],                  # Points earned by each user
        "points_redeemed": [50, 150],                 # Points redeemed by each user
    })

# API Endpoints

@app.route('/api/user-activity', methods=['GET'])
def user_activity():
    """
    API endpoint to fetch user activity data.
    Returns:
        JSON representation of the user activity data.
    """
    data = load_user_activity_data()  # Load mock user activity data
    if data.empty:  # Check if data is empty
        return jsonify({"error": "No data available for user activity"}), 404
    return jsonify(data.to_dict(orient='records'))  # Return data as JSON

@app.route('/api/user-activity/heatmap', methods=['GET'])
def user_activity_heatmap():
    """
    API endpoint to generate a heatmap for user activity.
    Returns:
        PNG image of the heatmap.
    """
    data = load_user_activity_data()  # Load mock user activity data
    if data.empty:  # Check if data is empty
        return jsonify({"error": "No data available for user activity"}), 404

    # Prepare data for the heatmap
    pivot_df = data.pivot(index="activity_date", columns="activity_type", values="activity_count").fillna(0)

    # Create the heatmap using Seaborn
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_df, annot=True, fmt="g", cmap="coolwarm", linewidths=0.5)
    plt.title("User Activity Heatmap")
    plt.tight_layout()

    # Save the heatmap to an in-memory bytes buffer
    output = io.BytesIO()
    plt.savefig(output, format="png")
    plt.close()
    output.seek(0)  # Reset buffer pointer to the start
    return Response(output.getvalue(), mimetype="image/png")  # Return PNG image as response

@app.route('/api/feedback-trends', methods=['GET'])
def feedback_trends():
    """
    API endpoint to fetch feedback trends data.
    Returns:
        JSON representation of the feedback trends data.
    """
    data = load_feedback_data()  # Load mock feedback data
    if data.empty:  # Check if data is empty
        return jsonify({"error": "No data available for feedback trends"}), 404
    return jsonify(data.to_dict(orient='records'))  # Return data as JSON

@app.route('/api/feedback-trends/graph', methods=['GET'])
def feedback_trends_graph():
    """
    API endpoint to generate a bar chart for feedback trends.
    Returns:
        PNG image of the bar chart.
    """
    data = load_feedback_data()  # Load mock feedback data
    if data.empty:  # Check if data is empty
        return jsonify({"error": "No data available for feedback trends"}), 404

    # Create the bar chart using Seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x="rating", y="feedback_count", palette="viridis")
    plt.title("Feedback Trends")
    plt.xlabel("Rating")
    plt.ylabel("Feedback Count")
    plt.tight_layout()

    # Save the bar chart to an in-memory bytes buffer
    output = io.BytesIO()
    plt.savefig(output, format="png")
    plt.close()
    output.seek(0)  # Reset buffer pointer to the start
    return Response(output.getvalue(), mimetype="image/png")  # Return PNG image as response

@app.route('/api/rewards-data', methods=['GET'])
def rewards_data():
    """
    API endpoint to fetch rewards program data.
    Returns:
        JSON representation of the rewards program data.
    """
    data = load_rewards_data()  # Load mock rewards data
    if data.empty:  # Check if data is empty
        return jsonify({"error": "No data available for rewards data"}), 404
    return jsonify(data.to_dict(orient='records'))  # Return data as JSON

@app.route('/api/rewards-analytics', methods=['GET'])
def rewards_analytics():
    """
    API endpoint to generate a bar chart for rewards analytics.
    Returns:
        PNG image of the bar chart.
    """
    data = load_rewards_data()  # Load mock rewards data
    if data.empty:  # Check if data is empty
        return jsonify({"error": "No data available for rewards analytics"}), 404

    # Prepare data for the bar chart
    df_pivot = data.melt(id_vars="user_id", value_vars=["points_earned", "points_redeemed"],
                         var_name="Point Type", value_name="Points")

    # Create the bar chart using Seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_pivot, x="user_id", y="Points", hue="Point Type", palette="muted")
    plt.title("Rewards Analytics")
    plt.xlabel("User ID")
    plt.ylabel("Points")
    plt.tight_layout()

    # Save the bar chart to an in-memory bytes buffer
    output = io.BytesIO()
    plt.savefig(output, format="png")
    plt.close()
    output.seek(0)  # Reset buffer pointer to the start
    return Response(output.getvalue(), mimetype="image/png")  # Return PNG image as response

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    API endpoint to check the health of the API.
    Returns:
        JSON indicating the health status of the application.
    """
    return jsonify({"status": "healthy"}), 200

# Main Entry Point
if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
