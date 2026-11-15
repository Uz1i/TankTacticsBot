import sqlite3
from PIL import Image
from random import randint

class Game:
    def __init__(self, db: str, playerCount: int):
        self.gridSize: int = round((playerCount/17)*15)
        print(self.gridSize)
        self.grid = [[0]*self.gridSize]*self.gridSize
        self.con = sqlite3.connect(db)
        self.cursor = self.con.cursor()
        self.playerPos = [(0, 0),]
    def setup_db(self) -> None:
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS playerlist (
                            idx INTEGER AUTOINCREMENT PRIMARY KEY,
                            discord_uid INTEGER NOT NULL,
                            username VARCHAR(25) NOT NULL,
                            country VARCHAR(50) NOT NULL,
                            mbti CHAR(4) NOT NULL,
                            action_points INTEGER,
                            range INTEGER,
                            lives INTEGER,
                            isAlive BOOLEAN,
                            current_X INTEGER,
                            current_y INTEGER
                            );""")
        self.con.commit()
    
    def update_position(self, position: tuple[int, int], direction: str) -> tuple[int, int] | None:
        if direction == "UP" and not position[1]-1 < 0:
            return (position[0], position[1]-1)
        elif direction == "DOWN" and not position[1]+1 > self.gridSize-1:
            return (position[0], position[1]+1)
        elif direction == "LEFT" and not position[0]-1 < 0:
            return (position[0]-1, position[1])
        elif direction == "RIGHT" and not position[0]+1 > self.gridSize-1:
            return (position[0]+1, position[1])
        else:
            return None

    def get_player_positions(self) -> list[tuple]:
        result = self.cursor.execute("SELECT current_x, current_y FROM playerlist;")
        positions = result.fetchall()
        print(positions)
        return positions

    def setup_player_positions(self) -> None:
        result = self.cursor.execute("SELECT discord_uid FROM playerlist;")
        players = result.fetchall()
        playerPositions = []
        for i, _ in enumerate(players):
            playerPositions.append((randint(0, self.gridSize-1), randint(0, self.gridSize-1), i+1))
        self.cursor.executemany("UPDATE playerlist SET current_x = ?, current_y = ? WHERE idx = ?;", playerPositions)
    
    def import_resources(self):
        self.empty = Image.open("./empty.png")
        self.red = Image.open("./red.png")
    
    def render_grid(self):
        playerPositions = self.get_player_positions()
        imgwidth = self.empty.size[0]*self.gridSize
        imgheight = self.empty.size[1]*self.gridSize
        mapImage = Image.new("RGBA", (imgwidth,imgheight))
        for x, column in enumerate(self.grid):
            for y, row in enumerate(column):
                if (x, y) in playerPositions:
                    mapImage.paste(self.red, (self.empty.size[0]*x, self.empty.size[1]*y))
                elif row == 0 and x != len(self.grid)-1:
                    mapImage.paste(self.empty, (self.empty.size[0]*x, self.empty.size[1]*y))
        
        mapImage.save("./map.png")



