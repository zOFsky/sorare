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
target_date = "2022-12-01T00:00:00Z"
players_df = pd.read_csv("sorare_players.csv")
players_df = players_df.iloc[9000:,]

query_text = queries.query_player_prices

players = {"player_id": [], "age": [], "position": [], "rarity": [], "usd_price": [], "eth_price": [], "transfer_type":[],
           "date": []}
# Iteratting over players from each team
def iterate_over_players(data, player_id):

    player_id = data["player"]["id"]
    age = data["player"]["age"]
    position = data["player"]["position"]

    for card in data["player"]["cards"]["nodes"]:
        rarity = card["rarity"]
        for sale in card["notContractOwners"]:
            if (sale["from"] > target_date) and (int(sale["price"]) > 0):
                usd_price = sale["priceInFiat"]["usd"]
                eth_price = sale["price"]
                date = sale["from"]
                transfer_type = sale["transferType"]

                players["player_id"].append(player_id)
                players["age"].append(age)
                players["position"].append(position)
                players["rarity"].append(rarity)
                players["usd_price"].append(usd_price)
                players["eth_price"].append(eth_price)
                players["transfer_type"].append(transfer_type)
                players["date"].append(date)


# Iteratting over the teams
for index, row in players_df.iterrows():
    query_text_new = query_text.replace("isotime", target_date)
    query = gql(query_text_new.replace("player-slug", row["slug"]))
    data = client.execute(query)
    iterate_over_players(data, row["player_id"])
    if (index % 500 == 0) & (index !=0):
        print(f"Done {index} players")
        time.sleep(300)


df = pd.DataFrame(players)  # Saving all the players in a SQL database
df.to_csv(
    "sorare_players_prices.csv",
    mode = "a",
    header=False
)
