query_get_players = """
{
  club(slug: "team_slug"){
    players(after: null){
      nodes{
          id
          displayName
          age
          position
          slug
        activeClub
        {
          name
          domesticLeague{
            country{
              threeLetterCode
            }
            displayName
          }
        }
        cardSupply{
          rare
          limited
        }
      }
      pageInfo{
          endCursor
        	hasNextPage
      }
    }
  }
}
"""

query_player_scores = """
{
  player(slug:"player-slug"){
    id
    displayName
    activeClub{
      name
    }
    allSo5Scores(first:20){
      nodes{
        score
      }
    }
  }
}"""

query_player_prices = """
{
  player(slug: "player-slug"){
    id
    age
    position
    cards(ownedSinceAfter:"isotime",rarities: limited){
      nodes{
        rarity
        notContractOwners{
          price
          priceInFiat{
						usd
          }
          transferType
          from
        }       
      }
      pageInfo{
          endCursor
        	hasNextPage
      }
    }
  }
}"""

query_players = """
{
  club(slug: "team_slug"){
    players(after: null){
      nodes{
          id
          displayName
          slug
        activeClub{
          name
        }
        cardSupply{
          rare
          limited
        }
      }
      pageInfo{
          endCursor
        	hasNextPage
      }
    }
  }
}
"""

query_clubs = """
{
  clubsReady{
    slug
    name
    domesticLeague{
      country{
        code
      }
      name
    }
  }
}
"""