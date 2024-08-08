import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import m2cgen as m2c

# Load the dataset
teams = pd.read_csv("teams.csv")

# Select relevant columns
teams = teams[["team", "athletes", "prev_medals", "medals", "year"]]

# Drop rows with missing values
teams = teams.dropna()

# Create a mapping for the 'team' column
team_mapping = {team: idx for idx, team in enumerate(teams['team'].unique())}
teams['team'] = teams['team'].map(team_mapping)

# Split data into training and test sets
train = teams[teams["year"] < 2012].copy()
test = teams[teams["year"] >= 2012].copy()

# Define and train the linear regression model
predictors = ["team", "athletes", "prev_medals"]
target = "medals"

reg = LinearRegression()
reg.fit(train[predictors], train[target])

# Make predictions on the test set
predictions = reg.predict(test[predictors])
test["predictions"] = predictions
test.loc[test["predictions"] < 0, "predictions"] = 0
test["predictions"] = test["predictions"].round()

# Evaluate the model
error = mean_absolute_error(test["medals"], test["predictions"])
print(f"Mean Absolute Error: {error}")

# Convert the trained model to Python code using m2cgen
model_code = m2c.export_to_python(reg)
print(model_code)
print(team_mapping)

# Save the team mapping to a JSON file
with open("team_mapping.json", "w") as file:
    json.dump(team_mapping, file)

# Save the generated model code to a Python file
with open("model.py", "w") as file:
    file.write(model_code)

print("Model exported successfully")