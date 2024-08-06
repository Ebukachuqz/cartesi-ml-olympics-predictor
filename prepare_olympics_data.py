
import pandas as pd

def prepare_olympics_data(athletes_file, output_file):
    # Load the athletes data
    athletes = pd.read_csv(athletes_file)

    # Filter for Summer Olympics
    athletes = athletes[athletes["Season"] == "Summer"]

    # Function to summarize team data
    def team_summary(data):
        return pd.Series({
            'team': data.iloc[0,:]["NOC"],
            'country': data.iloc[-1,:]["Team"],
            'year': data.iloc[0,:]["Year"],
            'events': len(data['Event'].unique()),
            'athletes': data.shape[0],
            'age': data["Age"].mean(),
            'height': data['Height'].mean(),
            'weight': data['Weight'].mean(),
            'medals': sum(~pd.isnull(data["Medal"]))
        })

    # Summarize team data by NOC and Year
    team = athletes.groupby(["NOC", "Year"]).apply(team_summary)

    # Reset the index and drop NA values
    team = team.reset_index(drop=True)
    team = team.dropna()

    # Function to calculate previous medals
    def prev_medals(data):
        data = data.sort_values("year", ascending=True)
        data["prev_medals"] = data["medals"].shift(1)
        data["prev_3_medals"] = data.rolling(3, closed="left", min_periods=1).mean()["medals"]
        return data

    # Calculate previous medals for each team
    team = team.groupby(["team"]).apply(prev_medals)
    team = team.reset_index(drop=True)
    team = team[team["year"] > 1960]
    team = team.round(1)

    # Save the prepared data to a CSV file
    team.to_csv(output_file, index=False)
    return team

# Example usage:
# team_data = prepare_olympics_data("athlete_events.csv", "teams.csv")
