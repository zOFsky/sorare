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

teams = []
query_text = queries.query_clubs
query = gql(query_text)
data = client.execute(query)

for club in data["clubsReady"]:
    name = club["slug"]
    t_name = club["name"]
    league = club["domesticLeague"]["name"]
    teams.append({"name": t_name, "slug": name, "league": league})

df = pd.DataFrame(teams)  # Saving all the teams in a SQL database

df.to_csv("sorare_teams.csv")