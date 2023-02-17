from fastapi import FastAPI, Path, HTTPException, status
from pydantic import BaseModel
from database import get_by_nationality, get_by_club, get_by_player_name, add_player_to_db, update_player, delete_player

class Player(BaseModel):
    nationality: str
    position: str
    national_team_jersey_number: int
    player_DOB: str
    club: str
    player_name: str
    appearances: int
    goals_scored: int
    assists_provided: int

app = FastAPI()

@app.get("/")
def root():
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Welcome to WorldCupPlayerStatsAPI")

@app.get("/players/{player_name}")
def get_by_name(player_name: str = Path(None, description="Name of the player you'd like to retrieve")):
    player = get_by_player_name(player_name)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return {"Nationality": player[0],
            "Position": player[1],
            "National team jersey number": player[2],
            "Date of birth": player[3],
            "Club": player[4],
            "Appearances": player[6],
            "Goals scored": player[7],
            "Assists provided": player[8],
            }

@app.get("/nationalities/{nationality}")
def get_player_by_nationality(nationality: str = Path(None,description="Nationality of the players you want to query")):
    players = get_by_nationality(nationality)
    if not players:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No player with this nationality")
    result = {}
    for idx, player in enumerate(players):
        result[idx] = {"Position": player[1],
                        "National team jersey number": player[2],
                        "Date of birth": player[3],
                        "Club": player[4],
                        "Player Name": player[5],
                        "Appearances": player[6],
                        "Goals scored": player[7],
                        "Assists provided": player[8],
                    }
    return result

@app.get("/clubs/{club}")
def get_player_by_club(club: str = Path(None,description="Club of the players you want to query")):
    players = get_by_club(club)
    if not players:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No player in this club")
    result = {}
    for idx, player in enumerate(players):
        result[idx] = {"Nationality": player[0],
                        "Position": player[1],
                        "National team jersey number": player[2],
                        "Date of birth": player[3],
                        "Player Name": player[5],
                        "Appearances": player[6],
                        "Goals scored": player[7],
                        "Assists provided": player[8],
                    }
    return result

@app.post("/newPlayer/{player_name}")
def create_player(player_name: str, player: Player):
    if get_by_player_name(player_name):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Player already exists") 
    add_player_to_db(player.nationality, player.position, 
                   player.national_team_jersey_number,
                   player.player_DOB, player.club,
                   player.player_name,
                   player.appearances,
                   player.goals_scored,
                   player.assists_provided)
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail="Player created successfully")

@app.put("/updatePlayer/{player_name}")
def update_player_info(player_name: str, player: Player):
    if not get_by_player_name(player_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found") 
    update_player(player.nationality, player.position, 
                player.national_team_jersey_number,
                player.player_DOB, player.club,
                player.player_name,
                player.appearances,
                player.goals_scored,
                player.assists_provided)
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Player details updated")

@app.delete("/deletePlayer/{player_name}")
def delete_player_info(player_name: str):
    if not get_by_player_name(player_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    delete_player(player_name)
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Player deleted successfully")


