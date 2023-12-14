Movie Recommendation System with Neo4j Database

This program is a movie recommendation system that utilizes a Neo4j database to store user information, movie details, and their interactions. Follow the steps below to set up and run the program on your computer.

Prerequisites

- Ensure you have Python installed on your machine.
- Install the Neo4j database on your local server.

Neo4j Setup

1. Download and install Neo4j from [Neo4j Download Page](https://neo4j.com/download/).

2. Start Neo4j server.

3. Create a new database or use an existing one.

4. Set the Neo4j credentials in the program:
   - Open the Python script (`movie_recommendation_system.py`).
   - Update the `uri`, `username`, and `password` variables with your Neo4j connection details.

Program Setup

1. Open a terminal or command prompt.

2. Navigate to the directory containing the Python script.

3. Install the required Python packages by running the following command:

   pip install neo4j

Running the Program

1. In the terminal or command prompt, run the Python script:

   python movie_recommendation_system.py

2. The program will present a menu with options for various interactions.

Program Usage

1. Identify User (Option 1):
   - Enter your user ID (1-600).
   - The program will search for the user in the database.
   - If found, it will display a welcome message; otherwise, it will prompt you to enter your name and add you to the database.

2. Search Movie (Option 2):
   - Enter a movie title keyword to search for matching movies.
   - The program will display movie details, including title, genres, and average rating.

3. Top 5 Recommendations (Option 3)
   - Enter your user ID (1-600) to get personalized movie recommendations.
   - The program will display the top 5 recommended movies based on your genre preferences and previous ratings.

4. Rate a Movie (Option 4):
   - Enter your user ID, movie ID, and your rating to add a rating for a movie.
   - The program will update the database with the rating information.

5. Exit (Option 5):
   - Choose this option to exit the program.

Closing the Program

- The program will automatically close the Neo4j database connection when you choose to exit.

Note: Make sure to customize the Neo4j connection details in the script and follow the instructions to ensure a smooth setup and execution of the movie recommendation system.
