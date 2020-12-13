from tkinter import *
from pandas import *
from random import *

def next_card():
    global counter
    global current_image
    global to_learn
    to_learn = choice(data_list)
    title = "Deutsch"
    original_word = to_learn["Deutsch"]
    card_canvas.itemconfig(current_image, image=card_front_image)
    card_canvas.itemconfig(card_title, text=title, fill="black")
    card_canvas.itemconfig(card_word, text=original_word, fill="green")
    card_canvas.itemconfig(card_word2, text="", fill="green")
    counter = window.after(4000, func=flip_card)


def word_is_known():
    global to_learn
    global data_list
    window.after_cancel(counter)
    data_list.remove(to_learn)
    data = DataFrame(data_list)
    data.to_csv("data/to_learn.csv", index=False)
    next_card()


def flip_card():
    global current_image
    global to_learn
    global card
    title = "Translation"
    translated_word = to_learn["English"]
    translated_word2 = to_learn["Arabic"]
    card_canvas.itemconfig(current_image, image=card_back_image)
    card_canvas.itemconfig(card_title, text=title, fill="brown")
    card_canvas.itemconfig(card_word, text=translated_word, fill="white")
    card_canvas.itemconfig(card_word2, text=translated_word2, fill="blue")

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
counter = None

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

card_canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
current_image = card_canvas.create_image(400, 265, image=card_front_image)
card_title = card_canvas.create_text(400, 100, text="Title", font=("Arial", 40, "italic"))
card_word = card_canvas.create_text(400, 200, text="Word", font=("Arial", 60, "bold"))
card_word2 = card_canvas.create_text(400, 300, text="", font=("Arial", 60, "bold"))
card_canvas.grid(row=0, column=0, columnspan=2)


try:
    data = pandas.read_csv("data/to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/german_words.csv")
    data_list = data.to_dict(orient="records")
else:
    data_list = data.to_dict(orient="records")


next_card()

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=word_is_known)
right_button.grid(row=1, column=1)


wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)



window.mainloop()
