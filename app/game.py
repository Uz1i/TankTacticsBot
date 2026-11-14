import sqlite3
from PIL import Image
from random import randint

class Game:
    def __init__(self, db: str, playerCount: int):
        self.gridSize: int = round((playerCount/17)*15)
        self.grid = [[0]*self.gridSize]*self.gridSize
        self.con = sqlite3.connect(db)
        self.cursor = self.con.cursor()
    
    def setup_db(self):
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

    def import_resources(self):
        self.empty = Image.open("./empty.png")
        self.red = Image.open("./red.png")
    
    def render_grid(self):
        xshade = randint(0, len(self.grid)-1)
        yshade = randint(0, len(self.grid)-1)
        imgwidth = self.empty.size[0]*self.gridSize
        imgheight = self.empty.size[1]*self.gridSize
        image = Image.new("RGBA", (imgwidth,imgheight))
        for x,i in enumerate(self.grid):
            for y,j in enumerate(i):
                if x == xshade and y == yshade:
                    image.paste(self.red, (self.empty.size[0]*x, self.empty.size[1]*y))
                elif j == 0 and x != len(self.grid)-1:
                    image.paste(self.empty, (self.empty.size[0]*x, self.empty.size[1]*y))
        print(self.empty.size)
        print(image.size)
        image.save("./map.png")


