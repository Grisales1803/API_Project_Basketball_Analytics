# Import the requests module for making HTTP requests
import requests
# Import the matplotlib module for creating charts
import matplotlib.pyplot as plt
# Import statistics module for central tendency calculations
import statistics
# Import shapiro function from scipy.stats for normality test
from scipy.stats import shapiro

# API key for the Ball Don't Lie API
API_KEY = "c9f5d6af-9f0f-4756-aed1-913ef442851c"
# Headers for the HTTP request, including the API key for authorization
HEADERS = {"Authorization": API_KEY}

def get_teams():
    # Make a GET request to the Ball Don't Lie API to retrieve team data
    response = requests.get("https://api.balldontlie.io/v1/teams", headers=HEADERS)
    # Return the response in JSON format
    return response.json()

def create_conference_chart(teams_data):
    # Calculate the number of teams in the East and West conferences
    east_teams = sum(1 for team in teams_data if team['conference'] == 'East')
    west_teams = sum(1 for team in teams_data if team['conference'] == 'West')

    # Define the labels and counts for the pie chart
    conferences = ['East', 'West']
    counts = [east_teams, west_teams]
    # Define the colors for the pie chart
    colors = ['lightgray', '#ff6f00']

    # Create a pie chart with the given data
    plt.figure(figsize=(6, 6))
    # Configure the pie chart with the given labels, counts, and colors
    plt.pie(counts, labels=conferences, colors=colors, 
            autopct=lambda p: '{:.0f}'.format(p * sum(counts) / 100), startangle=140)
    # Set the title of the chart
    plt.title('Number of Teams in Each Conference')

    # Save the plot as a PNG image in the 'static' folder
    plt.savefig('static/conference_teams.png')

def get_players():
    # Make a GET request to the Ball Don't Lie API to retrieve player data
    players_page = {"per_page": 100}  # Fetch up to 100 players per page
    response = requests.get("https://api.balldontlie.io/v1/players", headers=HEADERS, params=players_page)
    # Return the response in JSON format
    return response.json()

def create_height_histogram(players_data):
    # Extract heights of all players
    heights = [player['height'] for player in players_data]

    # Convert height from 'ft-in' to inches
    heights_in_inches = []
    for height in heights:
        feet, inches = map(int, height.split('-'))
        total_inches = feet * 12 + inches
        heights_in_inches.append(total_inches)

    # Create the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(heights_in_inches, bins=range(min(heights_in_inches), max(heights_in_inches) + 1, 1), color='#ff6f00', edgecolor='white')
    plt.title('Height Distribution of NBA Players')
    plt.xlabel('Height (inches)')
    plt.ylabel('Number of Players')

    # Save the histogram as a PNG image in the 'static' folder
    plt.savefig('static/height_histogram.png')

def create_weight_histogram(players_data):
    # Extract weights of all players and convert to integers
    weights = []
    for player in players_data:
        try:
            # Convert weight to integer
            weight = int(player['weight'])
            weights.append(weight)
        except (ValueError, TypeError):
            # Handle cases where weight is not a valid integer
            continue

    # Create the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(weights, bins=range(min(weights), max(weights) + 1, 5), color='#4b4b4b', edgecolor='white')
    plt.title('Weight Distribution of NBA Players')
    plt.xlabel('Weight (lbs)')
    plt.ylabel('Number of Players')

    # Save the histogram as a PNG image in the 'static' folder
    plt.savefig('static/weight_histogram.png')

def ctm_height(players_data):
    # Extract heights of all players
    heights = [player['height'] for player in players_data]

    # Convert height from 'ft-in' to inches
    heights_in_inches = []
    for height in heights:
        feet, inches = map(int, height.split('-'))
        total_inches = feet * 12 + inches
        heights_in_inches.append(total_inches)

    # Calculate the average height in inches
    average_height = statistics.mean(heights_in_inches)
    # Calculate the median height in inches
    median_height = statistics.median(heights_in_inches)
    # Calculate the mode height in inches
    mode_height = statistics.mode(heights_in_inches)
    # Perform a Shapiro-Wilk test to check the normality of the data
    # Null hypothesis (H0): The data follows a normal distribution
    # Alternative hypothesis (H1): The data does not follow a normal distribution
    _, p_value = shapiro(heights_in_inches)
    # If p-value is less than 0.05, the data is not normally distributed
    if p_value < 0.05:
        message_heights = "With a confidence of 95%, the data of heights in inches is not normally distributed."
    else:
        message_heights = "With a confidence of 95%, the data of heights in inches is normally distributed."

    return average_height, median_height, mode_height, message_heights

def ctm_weight(players_data):
    # Extract weights of all players and convert to integers
    weights = []
    for player in players_data:
        try:
            # Convert weight to integer
            weight = int(player['weight'])
            weights.append(weight)
        except (ValueError, TypeError):
            # Handle cases where weight is not a valid integer
            continue

    # Calculate the average weight in lbs
    average_weight = statistics.mean(weights)
    # Calculate the median weight in lbs
    median_weight = statistics.median(weights)
    # Calculate the mode weight in lbs
    mode_weight = statistics.mode(weights)
    # Perform a Shapiro-Wilk test to check the normality of the data
    # Null hypothesis (H0): The data follows a normal distribution
    # Alternative hypothesis (H1): The data does not follow a normal distribution
    _, p_value = shapiro(weights)
    # If p-value is less than 0.05, the data is not normally distributed
    if p_value < 0.05:
        message_weights = "With a confidence of 95%, the data of weights in lbs is not normally distributed."
    else:
        message_weights = "With a confidence of 95%, the data of weights in lbs is normally distributed."

    return average_weight, median_weight, mode_weight, message_weights