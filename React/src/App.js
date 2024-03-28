import React, { useState, useEffect } from 'react';
import './App.css'; // Import CSS file for styling

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("/recipes")
      .then(res => res.json())
      .then(data => {
        setData(data);
        console.log("DATA:", data); // Log fetched data to the console
      })
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  const handleAddRecipe = () => {
    const recipeName = window.prompt("Enter recipe name:");
    if (recipeName) {
      const isVegetarian = window.confirm("Is the recipe vegetarian?\nClick OK for Yes, Cancel for No");
      const newRecipe = {
        recipe_name: recipeName,
        vegetarian: isVegetarian
      };

      // Send a PUT request to the server to add the new recipe
      fetch("/recipes", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(newRecipe)
      })
      .then(response => {
        if (response.ok) {
          console.log("Recipe added successfully!");
          // Update the state to reflect the new recipe
          setData([...data, newRecipe]);
        } else {
          console.error("Failed to add recipe:", response.statusText);
        }
      })
      .catch(error => console.error("Error adding recipe:", error));
    }
  };

  const handleDeleteRecipe = (recipeName) => {
    if (window.confirm(`Are you sure you want to delete ${recipeName}?`)) {
      fetch(`/recipes/${recipeName}`, {
        method: "DELETE",
      })
      .then(response => {
        if (response.ok) {
          console.log("Recipe deleted successfully!");
          // Update the state to remove the deleted recipe
          setData(data.filter(recipe => recipe.recipe_name !== recipeName));
        } else {
          console.error("Failed to delete recipe:", response.statusText);
        }
      })
      .catch(error => console.error("Error deleting recipe:", error));
    }
  };

  return (
    <div className="container">
      <h1>Recipes</h1>
      <button className="add-button" onClick={handleAddRecipe}>Add Recipe</button>
      <ul className="recipe-list">
        {data.map((recipe, index) => (
          <li key={index} className="recipe-item">
            <div>
              <strong>Name:</strong> {recipe.recipe_name}, <strong>Vegetarian:</strong> {recipe.vegetarian ? 'Yes' : 'No'}
            </div>
            <button className="delete-button" onClick={() => handleDeleteRecipe(recipe.recipe_name)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
