# Import Flask, render_template, and jsonify from the flask module
from flask import Flask, render_template, jsonify
# Import the extraction module for custom data extraction and processing functions
import extraction

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    # Render the index.html template when the home page is accessed
    return render_template('index.html')

# Define the route for the teams page
@app.route('/teams')
def teams():
    # Retrieve team data using the get_teams function from the extraction module
    teams_data = extraction.get_teams()
    # Create a conference chart using the retrieved team data
    extraction.create_conference_chart(teams_data['data'])
    # Render the teams.html template and pass the team data to it
    return render_template('teams.html', teams=teams_data['data'])

# Define the route for the players page
@app.route('/players')
def players():
    # Retrieve player data using the get_players function from the extraction module
    players_data = extraction.get_players()
    # Create a histogram of heights using the retrieved player data
    extraction.create_height_histogram(players_data['data'])
    # Create a histogram of weights using the retrieved player data
    extraction.create_weight_histogram(players_data['data'])
    # Calculate central tendency metrics and normality test for heights
    average_height, median_height, mode_height, message_heights = extraction.ctm_height(players_data['data'])
    # Calculate central tendency metrics and normality test for weights
    average_weight, median_weight, mode_weight, message_weights = extraction.ctm_weight(players_data['data'])
    # Sort players by first name
    sorted_players = sorted(players_data['data'], key=lambda x: x['first_name'])
    # Render the players.html template and pass the player data, central tendency metrics, and normality test messages to it
    return render_template('players.html', players=sorted_players, height_mean=average_height, height_median=median_height, height_mode=mode_height, height_normality_message=message_heights, weight_mean=average_weight, weight_median=median_weight, weight_mode=mode_weight, weight_normality_message=message_weights)

# Define the route for fetching player information based on player ID
@app.route('/player_info/<int:player_id>')
def player_info(player_id):
    # Retrieve player data using the get_players function from the extraction module
    players_data = extraction.get_players()
    # Find the player with the matching ID
    player = next((player for player in players_data['data'] if player['id'] == player_id), None)
    # Return the player data as JSON
    return jsonify(player)

# Run the Flask application
if __name__ == '__main__':
    # Set the app to run on host 0.0.0.0 and port 8080
    app.run(host='0.0.0.0', port=8080)