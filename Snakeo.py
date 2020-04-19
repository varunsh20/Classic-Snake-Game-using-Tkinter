import tkinter as tk
from random import randint
from PIL import Image, ImageTk

MOVE_INCREMENT = 20
moves_per_second=15
GAME_SPEED=1000//moves_per_second


class Snakeo(tk.Canvas):
     def __init__(self):
         super().__init__(width=700, height=720, background="black", highlightthickness=0)
         self.score=0

         self.snakepos=[(100, 100), (80, 100), (60, 100)]
         self.foodpos=self.set_new_food_position()
         self.direction="Right"
         self.bind_all("<Key>", self.on_key_press)




         self.load_assets()
         self.create_objects()
         self.after(GAME_SPEED, self.perform_actions)


     def load_assets(self):
         self.snake_body_image=Image.open("C:\\Users\Varun\\Desktop\\snake.png")
         self.snakebody=ImageTk.PhotoImage(self.snake_body_image)

         self.food_image=Image.open("C:\\Users\\Varun\\Desktop\\food.png")
         self.food=ImageTk.PhotoImage(self.food_image)
     def create_objects(self):

         self.create_text(
             50, 15, text=f"Score: {self.score} (speed: {moves_per_second})",tag="score",fill="#fff")




         for x_pos,y_pos in self.snakepos:

            self.create_image(x_pos, y_pos, image=self.snakebody, tags="snake")
         self.create_image(*self.foodpos, image=self.food, tags="food")

     def move_object(self):
         head_xpos, head_ypos = self.snakepos[0]
         if self.direction =="Left":
             new_head_pos = (head_xpos - MOVE_INCREMENT, head_ypos)
         elif self.direction == "Right":
             new_head_pos = (head_xpos + MOVE_INCREMENT, head_ypos)
         elif self.direction == "Down":
             new_head_pos = (head_xpos , head_ypos + MOVE_INCREMENT)
         elif self.direction == "Up":
             new_head_pos = (head_xpos, head_ypos - MOVE_INCREMENT)


         self.snakepos = [new_head_pos] + self.snakepos[:-1]

         for segment, position in zip(self.find_withtag("snake"), self.snakepos):
             self.coords(segment, position)
     def perform_actions(self):
         if self.check_collision():
             self.end_game()
             return
         self.check_food_collison()

         self.move_object()
         self.after(GAME_SPEED, self.perform_actions)

     def check_collision(self):
         head_xpos, head_ypos = self.snakepos[0]

         return (
              head_xpos in (0,700)
             or head_ypos in (20,720)
             or (head_xpos, head_ypos) in self.snakepos[1:]
         )

     def on_key_press(self, e):
         new_direction = e.keysym
         all_directions = ("Up","Down", "Left", "Right")
         opposites = ({"Up","Down"},{"Left","Right"})

         if (
             new_direction in all_directions
             and {new_direction, self.direction} not in opposites
         ):

            self.direction = new_direction
     def check_food_collison(self):
         if self.snakepos[0] == self.foodpos:
             self.score+=1
             self.snakepos.append(self.snakepos[-1])

             if self.score % 5 ==0:
                 global moves_per_second
                 moves_per_second+=1

             self.create_image(
                 *self.snakepos[-1], image = self.snakebody,tags ="snake"
             )
             self.foodpos = self.set_new_food_position()
             self.coords(self.find_withtag("food"),self.foodpos)
             score = self.find_withtag("score")
             self.itemconfigure(score,text = f"Score: {self.score}(speed:{moves_per_second})",
                                tag="score"
                                )

     def set_new_food_position(self):
         while True:
             x_pos = randint(1,34) * MOVE_INCREMENT
             y_pos = randint(3,35) * MOVE_INCREMENT
             foodpos = (x_pos,y_pos)

             if foodpos not in self.snakepos:
                 return foodpos
     def end_game(self):
         self.delete(tk.ALL)
         self.create_text(
             self.winfo_width()/2,
             self.winfo_height()/2,
             text=f"Game over!Your score was {self.score}!",
             fill = "#fff",
             font =("TkDefaultFont",24)


         )

root=tk.Tk()

root.title("Snakeo")
root.resizable(False, False)

board = Snakeo()
board.pack()




root.mainloop()