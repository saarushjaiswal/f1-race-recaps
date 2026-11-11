import requests # Improting the library that lets Python make the HTTP requests
import pandas as pd #importing pandas library to work with the dfs.
import sys # Importing the sys library which helps us to exit the program.

#  select thr results endopint for season 2026, and race round 1 (which is the Australian Grand Prix)
# url ="https://api.jolpi.ca/ergast/f1/2026/1/results/"
#  reference: https://github.com/jolpica/jolpica-f1/blob/main/docs/README.md

# ask the user for a season; input()return text
season = input("Enter a season (example: 2026): ")

round_number = input("Enter race round (example: 1):")

# fetching the exact season and round requested from the user
url = f"https://api.jolpi.ca/ergast/f1/{season}/{round_number}/results/"


# Excpetion handling: try the request so network faliures can be handled.
try:
    # request resutls for the selected race.
    response = requests.get(url, timeout=15, headers = {"User-Agent": "F1RaceRecaps/0.1"}
                            ) # set a timeout of 10 seconds for the request
    response.raise_for_status() # raise an exception if the request failed like the 404 or 500 errors

except requests.exceptions.RequestException as e:
    # Explaining why the request failed to the user.
    print(f"Could not fetch the requested race data: {e}")

    # Stopping
    sys.exit(1)


# this converts the Json data into python dictionaries and lists.
data = response.json()

# navigaging through those dictionaries to get the list of the races.
races = data["MRData"]["RaceTable"]["Races"]

# Excpetion handling: if the race is is empty which means the requested season and round.
if not races:
    print("No races data found for season " + season + " and round " + round_number + ". Check and try again.")
    sys.exit(1) # this stops before trying to access the invalid race

race = races[0]


# getting the first race in the list; the index starts at 0
race = races[0]

# printing the name stored in this races dictionary
print("Race: " +race["raceName"])


# get the list of dirver resutls for this race.
results = race["Results"]

# then print how many drivers appear in the results
print("Number of Drivers: " + str(len(results)))

# # looping through each driver's result.
# for result in resutls:
#     # get the dictionary containing the driver's info
#     driver = result["Driver"]

#     # printing the drivers finishing pos, and name
#     print(result["position"], driver["givenName"], driver["familyName"])

# Start an empty list to hold the table rows.
rows = []

for result in results:
    # build one row using the fields we want to keep
    row = {
        "Position": int(result["position"]),
        "Driver": result["Driver"]["givenName"] + " " + result["Driver"]["familyName"],
        "Team": result["Constructor"]["name"],
        "Grid": int(result["grid"]),
        "Points": float(result["points"]),
    }   

    # add this drriver's row to our list.
    rows.append(row)

table = pd.DataFrame(rows)  # convert the list of rows into a pandas df

# pritn the table without pandas extra row-num column.
print(table.to_string(index=False))  

