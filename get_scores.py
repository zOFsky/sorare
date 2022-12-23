import pandas as pd
import queries
import time
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from settings import aud, jwt_token


# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(
    url="https://api.sorare.com/graphql",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
        "JWT_AUD": f"{aud}",
    })

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Retrieving the teams from the DB
players_df = pd.read_csv("sorare_players.csv")
players_df = players_df.iloc[8500:,]

query_text = queries.query_player_scores

players = {"player_id_read": [], "player_id": [], "player_name": [], "week": [], "score": [], "team": []}
# Iteratting over players from each team
def iterate_over_players(data, player_id):

    player_name = data["player"]["displayName"]
    player_id_read = data["player"]["id"]
    if data["player"]["activeClub"]:
        current_team_name = data["player"]["activeClub"]["name"]
    else:
        current_team_name = "None"

    for num, score in enumerate(data["player"]["allSo5Scores"]["nodes"]):
        week_score = score["score"]

        players["player_id"].append(player_id)
        players["player_id_read"].append(player_id_read)
        players["player_name"].append(player_name)
        players["week"].append(num)
        players["score"].append(week_score)
        players["team"].append(current_team_name)


# Iteratting over the teams
for index, row in players_df.iterrows():
    query = gql(query_text.replace("player-slug", row["slug"]))
    data = client.execute(query)
    iterate_over_players(data, row["player_id"])
    if (index % 500 == 0) & (index !=0):
        print(f"Done {index} players")
        time.sleep(600)



df = pd.DataFrame(players)  # Saving all the players in a SQL database
df.to_csv(
    "sorare_players_scores.csv",
   mode = "a",
   header=False
)
