query_get_scores = """
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
        allSo5Scores(last: 20){
          nodes{
            score
          }
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