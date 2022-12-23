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

teams = pd.read_csv("sorare_teams.csv")
#teams = teams.iloc[0:2,]
players = []
query_text = queries.query_get_players


def iterate_over_players(data):
    for node in data["club"]["players"]["nodes"]:
        position = node["position"]
        age = node["age"]
        #print(node)
        try:
            current_team_name = node["activeClub"]["name"]
        except:
            current_team_name = None

        try:
            league = node["activeClub"]["domesticLeague"]["displayName"]
        except:
            league = None
        try:
            country_league = node["activeClub"]["domesticLeague"]["country"]["threeLetterCode"]
        except:
            country_league = None

        if node["cardSupply"]:
            players.append(
                {
                    "name": node["displayName"],
                    "position": position,
                    "age": age,
                    "club": current_team_name,
                    "league": league,
                    "league_country": country_league,
                    "player_id": node["id"].split(":")[-1],
                    "slug": node['slug'],
                }
            )


# Iteratting over the teams
for index, row in teams.iterrows():
    query = gql(query_text.replace("team_slug", row["slug"]))
    data = client.execute(query)
    iterate_over_players(data)
    while data["club"]["players"]["pageInfo"]["hasNextPage"]:
        cursor = data["club"]["players"]["pageInfo"]["endCursor"]
        query = gql(query_text.replace("team_slug", row["slug"]).replace("null", f'"{cursor}"'))
        data = client.execute(query)
        iterate_over_players(data)

    if (index % 100 == 0) & (index !=0):
        print(f"Done {index} clubs")
        time.sleep(300)

df = pd.DataFrame(players)  # Saving all the players in a SQL database
df.drop_duplicates(inplace=True)
df.to_csv("player_general.csv")