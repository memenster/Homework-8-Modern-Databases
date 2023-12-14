# Miles Cook Menster
# 11/30/2023
# Homework 8 Modern Databases

from neo4j import GraphDatabase  # import neo4j

uri = "neo4j://localhost:7687"  # default port
username = "neo4j"  # default username
password = "HeroHawk1020!@#"

driver = GraphDatabase.driver(uri, auth=(username, password))

userId = 0


def close_driver():
    driver.close()


def find_or_add_user(user_id):
    global userId
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $id}) RETURN u.name", id=user_id)
        user = result.single()
        userId = user_id

        if user and user["u.name"]:
            print(f"Welcome, {user['u.name']}!")
        else:
            new_name = input("Please input your name: ")
            session.run("MERGE (u:User {id: $id}) ON CREATE SET u.name = $name", id=user_id, name=new_name)
            print(f"Welcome, {new_name}!")


def search_movie(title_keyword):
    with driver.session() as session:
        result = session.run(
            "MATCH (m:Movie)-[:IN_GENRE]->(g:Genre) "
            "WHERE m.title CONTAINS $keyword "
            "OPTIONAL MATCH (m)<-[r:RATED]-() "
            "RETURN m.title AS Title, collect(DISTINCT g.name) "
            "AS Genres, coalesce(avg(r.rating), 'No ratings') AS Rating",
            keyword=title_keyword)
        movies = result.values()

        for movie in movies:
            title = movie[0]  # Title
            genres = movie[1]  # Genres
            rating = movie[2]  # Avg Rating

            # Case where there are no genres listed for a movie
            genres_str = ', '.join(genres) if genres else 'No genres listed'

            # Format the rating as a string; if it's 'No ratings', leave it as is, otherwise format the number
            rating_str = f"{rating:.1f}" if isinstance(rating, float) else rating
            print(f"Title: {title}, Genres: {genres_str}, Rating: {rating_str}")


def top_5_recommendations(user_id):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {userId: $user_id})-[gp:genre_pref]->(g:Genre)
            WITH u, g ORDER BY gp.preference DESC LIMIT 5
            MATCH (g)<-[:IN_GENRE]-(m:Movie)
            WHERE NOT (u)-[:RATED]->(m)
            OPTIONAL MATCH (m)<-[r:RATED]-()
            WITH m.movieId AS MovieID, m.title AS Movie, coalesce(avg(r.rating), 2.5) AS Rating
            ORDER BY Rating DESC LIMIT 5
            RETURN MovieID, Movie, Rating
            """,
            user_id=user_id)
        recommendations = result.values()

        if recommendations:
            print("Top 5 Recommendations:")
            for rec in recommendations:
                # Since `rec` is a list, use indexing to access elements
                movie_id = rec[0]  # Assuming MovieID is first
                title = rec[1]  # Assuming Movie is second
                rating = rec[2]  # Assuming Rating is third

                # If rating is float, format it with one decimal place, otherwise, 'No ratings'
                rating_str = f"{rating:.1f}" if isinstance(rating, float) else rating
                print(f"Movie ID: {movie_id}, Title: {title}, Rating: {rating_str}")
        else:
            print(f"There were no recommendations found for user ID {user_id}.")


def rate_movie(user_id, movie_id, rating):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            # Convert inputs to the correct types
            user_id_int = int(user_id)
            movie_id_int = int(movie_id)
            rating_float = float(rating)

            # Run the Cypher query
            result = tx.run(
                "MATCH (u:User {userId: $user_id}), (m:Movie {movieId: $movie_id}) "
                "MERGE (u)-[r:RATED]->(m) "
                "ON CREATE SET r.rating = $rating "
                "ON MATCH SET r.rating = $rating "
                "RETURN u.userId AS userId, m.movieId AS movieId, r.rating AS rating",
                {'user_id': user_id_int, 'movie_id': movie_id_int, 'rating': rating_float})

            # Check records are returned
            records = list(result)
            if not records:
                print("Rating not submitted or changes not made.")
            else:
                for record in records:
                    print(
                        f"User {record['userId']} rated Movie {record['movieId']} with a rating of {record['rating']}.")
            # Commit transaction
            tx.commit()


def main():
    while True:
        print("\nMenu:")
        print("1. Identify User")
        print("2. Search for a Movie")
        print("3. Top 5 Movie Recommendations")
        print("4. Rate a Movie")
        print("5. Exit Program")

        choice = input("Enter your choice: ")

        if choice == '1':
            user_id = input("Enter your user ID (1-600): ")
            find_or_add_user(user_id)
        elif choice == '2':
            title_keyword = input("Enter movie title or keyword to search: ")
            search_movie(title_keyword)
        elif choice == '3':
            user_id = int(input("Enter your user ID (1-600) for recommendations: "))
            top_5_recommendations(user_id)
        elif choice == '4':
            user_id = input("Enter your user ID: ")
            movie_id = input("Enter movie ID to rate: ")
            rating = input("Enter your rating: ")
            rate_movie(user_id, movie_id, rating)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")
    # closes the driver
    close_driver()


if __name__ == "__main__":
    main()
