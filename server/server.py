from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialization route
@app.route("/")
def init():
    # Get a new database connection for each request
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS recipes")
    cursor.execute("CREATE TABLE recipes (recipe_name TEXT NOT NULL, vegetarian BOOLEAN NOT NULL)")
    cursor.execute("INSERT INTO recipes VALUES ('Fried Rice', 0)")  # Assuming False is represented as 0
    conn.commit()  # Commit the transaction to save changes
    conn.close()   # Close the connection
    return "Initialization complete"

# Recipes route
@app.route("/recipes")
def recipes():
    # Get a new database connection for each request
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM recipes").fetchall()
    conn.close()   # Close the connection
    return jsonify([dict(row) for row in rows])  # Convert rows to dictionaries and return as JSON

@app.route("/recipes", methods=["PUT"])
def addRecipe():
    try:
        # Retrieve data from request body
        data = request.json
        if data is None:
            print("Empty")
        recipe_name = data.get('recipe_name')
        vegetarian = data.get('vegetarian')
        print(recipe_name, vegetarian)
        # Validate data
        if not recipe_name:
            return jsonify({'error': 'Recipe name is required'}), 400

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the new recipe into the database
        cursor.execute("INSERT INTO recipes (recipe_name, vegetarian) VALUES (?, ?)", (recipe_name, vegetarian))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Recipe added successfully'}), 201

    except Exception as e:
        print("Error")
        return jsonify({'error': str(e)}), 500
    

@app.route("/recipes/<recipe_name>", methods=["DELETE"])
def deleteRecipe(recipe_name):
    print("Deleting")
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the recipe from the database using the recipe_name route parameter
        cursor.execute("DELETE FROM recipes WHERE recipe_name = ?", (recipe_name,))
        conn.commit()
        conn.close()

        return jsonify({'message': f'Recipe {recipe_name} deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, port=5001)
