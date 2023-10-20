

##----------------------------import modules------------------------#
import random

from tkinter import *
import pandas as pd


#--------------------------------constants------------------------#
BACKGROUND_COLOR = "#B1DDC6"
FRENCH_WORD=""
ENGLISH_WORD=""
new_pair=""

#---------------CARD MECHANISM------------------#

#----Only run the line below to make the words to learn list from scratch----#
#french_words = pd.read_csv("data/french_words.csv")


#--------only run the line below to resume practice from where you left off-----#
try:
    french_words = pd.read_csv("data/words_to_learn.csv")
    
except FileNotFoundError:
    french_words = pd.read_csv("data/french_words.csv")
    french_dict = {row.French: row.English for (index, row) in french_words.iterrows()}

else:
    french_dict = {row.French: row.English for (index, row) in french_words.iterrows()}


print(french_dict)

words_to_learn = []


#this would be better with list comprehension, but whatever. 
for item in french_dict:
    words_to_learn.append({item:french_dict[item]})

#--------------Define Functions-----------
def new_card():
    global FRENCH_WORD, ENGLISH_WORD, flip_timer, new_pair
    flip_to_front()
    screen.after_cancel(flip_timer)
    new_pair=random.choice(words_to_learn)
    
#I just googled the [*new_pair] thing. i have no idea how to do it. 
    FRENCH_WORD=[*new_pair]
    ENGLISH_WORD=[*new_pair.values()]
    canvas.itemconfig(word_text, text=FRENCH_WORD)
    flip_timer=screen.after(3000, func=flip_to_back)


#---------this function is a nightmare and an embarrassment. i have no idea how angela got to where she did....----#
def refresh_words_to_learn():
    french_list=[]
    english_list=[]
    for item in words_to_learn:
        for key in item.keys():
            french_list.append(key)
        
    for item in words_to_learn:
        for value in item.values():
            english_list.append(value)

    words_to_learn_df_dict={"French": french_list, "English": english_list}       
    df=pd.DataFrame(words_to_learn_df_dict)
    df.to_csv("data/words_to_learn.csv")

def word_known():
    global new_pair
    words_to_learn.remove(new_pair)
    refresh_words_to_learn()
    
def correct():
    word_known()
    new_card()
    
def incorrect():
    new_card()

def flip_to_back():
    canvas.itemconfig(canvas_image, image=back_card_img)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=ENGLISH_WORD, fill="white")

def flip_to_front():
    canvas.itemconfig(canvas_image, image=front_card_img)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, fill="black")

#----------------Build UI---------------#
screen = Tk()
screen.title("Let's Learn!")
screen.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer=screen.after(3000, func=flip_to_back)

canvas=Canvas(width=900, height=700, bg=BACKGROUND_COLOR, highlightthickness=0)

front_card_img = PhotoImage(file="images/card_front.png")
canvas_image=canvas.create_image(450, 350, image=front_card_img)

back_card_img = PhotoImage(file="images/card_back.png")

canvas.grid(column=0, row=0, columnspan=2)

language_text=canvas.create_text(450, 230, font=("Snell Roundhand", 40, "italic"), text="French", fill="black")

word_text=canvas.create_text(450, 350, font=("Avenir", 60, "bold"), text=FRENCH_WORD)


#----------------------make buttons------------------#
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=correct, height=100, width=100)
right_button.grid(row=1, column = 0)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button=Button(image=wrong_image, highlightthickness=0, command=incorrect)
wrong_button.grid(row=1, column=1)

new_card()

#-------------------keep tkinter running ad nauseum!-------------------#

screen.mainloop()
