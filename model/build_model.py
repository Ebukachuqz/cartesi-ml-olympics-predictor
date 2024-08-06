import pandas as pd
import m2cgen as m2c
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

def build_and_export_model(teams_file, output_file):
    # Load the teams data
    teams = pd.read_csv(teams_file)

    # Select relevant columns
    teams = teams[["team", "country", "year", "athletes", "age", "prev_medals", "medals"]]

    # Drop rows with missing values
    teams = teams.dropna()

    # Split data into training and test sets
    train = teams[teams["year"] < 2012].copy()
    test = teams[teams["year"] >= 2012].copy()

    # Define and train the linear regression model
    reg = LinearRegression()
    predictors = ["athletes", "prev_medals"]
    reg.fit(train[predictors], train["medals"])

    # Make predictions on the test set
    predictions = reg.predict(test[predictors])
    test["predictions"] = predictions
    test.loc[test["predictions"] < 0, "predictions"] = 0
    test["predictions"] = test["predictions"].round()

    # Evaluate the model
    error = mean_absolute_error(test["medals"], test["predictions"])
    print(f"Mean Absolute Error: {error}")

    # Transpile the model to pure Python code
    model_to_python = m2c.export_to_python(reg)

    # Gather the final model's input features/columns
    model_columns = predictors

    # Write the model to a Python file
    with open(output_file, "w") as text_file:
        print(f"{model_to_python}", file=text_file)
        print(f"columns = {model_columns}", file=text_file)

    print("Model exported successfully")

# Example usage:
build_and_export_model("../teams.csv", "../model.py")
