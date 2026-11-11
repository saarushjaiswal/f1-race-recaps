import requests # Improting the library that lets Python make the HTTP requests
import pandas as pd #importing pandas library to work with the dfs.

#  select thr results endopint for season 2026, and race round 1 (which is the Australian Grand Prix)
url ="https://api.jolpi.ca/ergast/f1/2026/1/results/"
#  reference: https://github.com/jolpica/jolpica-f1/blob/main/docs/README.md


# request the race resutls and store the server's response.
response = requests.get(
    url,  #the api address to request
    timeout=15, # set a 15 sec timemout for network waits
    headers={"User-Agent": "F1RaceRecaps/0.1"},  # Identify our app.

)



print(response.status_code)  # Print the HTTP status code of the response
# 200 means the request was successful, 404 means the resource was not found, etc.

# this converts the Json data into python dictionaries and lists.
data = response.json()

# navigaging through those dictionaries to get the list of the races.
races = data["MRData"]["RaceTable"]["Races"]

# getting the first race in the list; the index starts at 0
race = races[0]

# printing the name stored in this races dictionary
print(race["raceName"])


# get the list of dirver resutls for this race.
results = race["Results"]

# then print how many drivers appear in the results
print(len(results))

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

