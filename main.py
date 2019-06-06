from random import randint

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

Builder.load_file('GuessWordUI.kv')


class GuessWord(BoxLayout):
    lb_msg: Label
    rv_words: RecycleView
    pb_score: ProgressBar

    with open("words.txt") as file:
        words = file.read().split("\n")
    num = randint(0, len(words)-1)
    word = list(words[num])
    mutatedWord = list(word)
    for i in range(len(word) // 3):
        idx = randint(0, len(word) - 1)
        mutatedWord[idx] = ""

    def checkAnswer(self):
        if "".join(self.mutatedWord) in self.words:
            self.pb_score.value += 10
            self.playAgain()
        elif self.pb_score.value >= 5:
            self.lb_msg.text = "Wrong, try again"
            self.pb_score.value -= 5
        else:
            self.lb_msg.text = "Game Over!!"
        Window.release_all_keyboards()

    def showAnswer(self):
        if self.pb_score.value >= 25:
            popup = MyPopup()
        else:
            popup = Popup(title='Warning!', content=Label(text="You don't have enough points"))
            popup.size_hint = 0.4, 0.4

        popup.open()


    def confirmShowAnswer(self, popup:Popup):
        self.mutatedWord = self.word
        self.rv_words.data = self.populateData()
        self.pb_score.value -= 25
        popup.dismiss()

    def playAgain(self):
        self.lb_msg.text = "Guess The Word"
        self.num = randint(0, len(self.words) - 1)
        self.word = list(self.words[self.num])
        self.mutatedWord = list(self.word)
        for i in range(len(self.word) // 3):
            idx = randint(0, len(self.word) - 1)
            self.mutatedWord[idx] = ""

        self.rv_words.data = self.populateData()

    def restartGame(self):
        self.pb_score.value = 0
        self.playAgain()

    def populateData(self):
        data = []
        for idx, letter in enumerate(self.mutatedWord):
            temp = {"idx": idx, "text": letter}
            if letter == "":
                temp["bg_color"] = (241/256, 196/256, 15/256)
            else:
                temp["bg_color"] = (1, 1, 1)
            data.append(temp)

        return data

class Cell(BoxLayout):

    def didSelectCell(self, idx, mutatedWord):
        tb : TextInput = self.children[0]
        mutatedWord[idx] = tb.text
        print(mutatedWord)


class MyPopup(Popup):
    pass


class GuessWordApp(App):
    def build(self):
        return GuessWord()


GuessWordApp().run()