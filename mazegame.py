


import turtle
import math
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A Maze Game")
wn.setup(700,700)
wn.tracer(0)

#Register shapes
images = ["wizard_right.gif", "wizard_left.gif",
          "treasure.gif", "wall.gif",
          "enemy_left.gif", "enemy_right.gif"]

for image in images:
    turtle.register_shape(image)

#Create Pen
class Pen(turtle.Turtle):
  def __init__(self):
    turtle.Turtle.__init__(self)
    self.shape("square")
    self.color("white")
    self.penup()
    self.speed(0)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wizard_right.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        #Calculate the spot to move to
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24

        #Check if the space has a wall
        if(move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        #Calculate the spot to move to
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24

        #Check if the space has a wall
        if(move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        #Calculate the spot to move to
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor() 

        self.shape("wizard_left.gif")

        #Check if the space has a wall
        if(move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        #Calculate the spot to move to
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()

        self.shape("wizard_right.gif")

        #Check if the space has a wall
        if(move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("treasure.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("enemy_left.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
            self.shape("enemy_left.gif")
        elif self.direction == "right":
            dx = 24
            dy = 0
            self.shape("enemy_right.gif")
        else:
            dx = 0
            dy = 0

        #Check if player is close
        #If so, go in that direction
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        #Calculate the spot to move to
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        #Check if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            #Choose a diffrent direction
            self.direction = random.choice(["up", "down", "left", "right"])

        #Set timer to move next time 
        turtle.ontimer(self.move, t = random.randint(100, 300))

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

#Create levels list
levels = [""]

#Define first level
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXXE         XXXXX",
"X  XXXXXXX  XXXXXX  XXXXX",
"X       XX  XXXXXX  XXXXX",
"X       XX  XXX       EXX",
"XXXXXX  XX  XXX        XX",
"XXXXXX  XX  XXXXXX  XXXXX",
"XXXXXX  XX    XXXX  XXXXX",
"X  XXX        XXXXT XXXXX",
"X  XXX  XXXXXXXXXXXXXXXXX",
"X         XXXXXXXXXXXXXXX",
"X                XXXXXXXX",
"XXXXXXXXXXXX     XXXXX  X",
"XXXXXXXXXXXXXXX  XXXXX  X",
"XXX  XXXXXXXXXX         X",
"XXXE                    X",
"XXX         XXXXXXXXXXXXX",
"XXXXXXXXXX  XXXXXXXXXXXXX",
"XXXXXXXXXX              X",
"XX   XXXXX              X",
"XX   XXXXXXXXXXXXX  XXXXX",
"XX    YXXXXXXXXXXX  XXXXX",
"XX          XXXX        X",
"XXXXE                   X",
"XXXXXXXXXXXXXXXXXXXXXXXXX"
]

#Add a treasures list
treasures = []

#Add enemies list
enemies = []

#Add maze to mazes list
levels.append(level_1)

#Create Level Setup Function
def setup_maze(level):
  for y in range(len(level)):
    for x in range(len(level[y])):
      #Get the characte at each x,y coordinate
      #NOTE the order of y and x in the next line
      character = level[y][x]
      #Calculate the screen x,y coordinates
      screen_x = -288 + (x * 24)
      screen_y = 288 - (y * 24)
      
      #Check if it is an X(representing a wall)
      if character == "X":
        pen.goto(screen_x, screen_y)
        pen.shape("wall.gif")
        pen.stamp()
        #Add coordinates to wall list
        walls.append((screen_x, screen_y))

      #Check if it is a P(representing the player)
      if character == "P":
          player.goto(screen_x, screen_y)        

      #Check if it is a T(representing Treasure)
      if character == "T":
          treasures.append(Treasure(screen_x, screen_y))
          
      #Check if it is an E(representing Enemy)
      if character == "E":
          enemies.append(Enemy(screen_x, screen_y))

#Create class instances
pen = Pen()
player = Player()

#Create wall coordinate list
walls = []

#Set up the level
setup_maze(levels[1])

#Keyboard Binding
turtle.listen()
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_up,"Up")
turtle.onkey(player.go_down,"Down")

#Turn off screen updates
wn.tracer(0)

#Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t = 250)

#Main Game Loop
while True:
  #Check for player collision with treasure
  #Iterate through treasure list
  for treasure in treasures:
      if player.is_collision(treasure):
          #Add the treasure gold to the player gold
          player.gold += treasure.gold
          print ("Player Gold: {}".format(player.gold))
          #Destroy the treasure
          treasure.destroy()
          #Remove the treasure from the treasures list
          treasures.remove(treasure)

  #Iterate through enemy list to see if the player collid
  for enemy in enemies:
      if player.is_collision(enemy):
          print("Player dies!")
  
  #Update screen
  wn.update()
