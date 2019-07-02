from random import randint

from datetime import date, datetime
from time import sleep
from typing import List

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.graphics.context_instructions import Color
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition, WipeTransition, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget

Builder.load_file('GuessWordUI.kv')
Builder.load_file('TitleBar.kv')
Builder.load_file('TabBar.kv')
Builder.load_file('ScoresHistory.kv')


class GuessWord(BoxLayout, Screen):
    lb_msg: Label
    rv_words: RecycleView
    pb_score: ProgressBar
    main_tree = None

    with open("words.txt") as file:
        words = file.read().split("\n")
    num = randint(0, len(words)-1)
    word = list(words[num])
    mutatedWord = list(word)
    for i in range(len(word) // 3):
        idx = randint(0, len(word) - 1)
        mutatedWord[idx] = ""

    # wrong_sound = SoundLoader.load('sounds/bad_news.wav')
    # correct_sound = SoundLoader.load('sounds/correct.wav')


    with open("scores_history.txt") as file:
        scores = []
        for line in file:
            idx, date, score = line.split(",")[:-1]
            scores.append({"idx": int(idx), "date": date, "score": int(score)})
        scores.sort(key= lambda x: x["score"], reverse=True)

    def checkAnswer(self):
        Window.release_all_keyboards()
        if "".join(self.mutatedWord) in self.words:
            # self.correct_sound.play()
            self.pb_score.value += 10
            if self.pb_score.value >= 500:
                self.lb_msg.text = "You Win The Game!!"
                self.save_score()
            else:
                # self.correct_sound.on_stop = self.playAgain
                self.playAgain()
        elif self.pb_score.value >= 5:
            # self.wrong_sound.play()
            self.lb_msg.text = "Wrong, try again"
            self.pb_score.value -= 5
        else:
            # self.wrong_sound.play()
            self.lb_msg.text = "Game Over!!"


    def showAnswer(self):
        if self.pb_score.value >= 25:
            popup = MyPopup()
        else:
            popup = Popup(title='Warning!', content=Label(text="You don't have\nenough points"))
            popup.size_hint = 0.4, 0.4

        popup.open()


    def confirmShowAnswer(self, popup:Popup):
        self.mutatedWord = self.word
        self.rv_words.data = self.populateData()
        self.pb_score.value -= 35
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
                temp["is_readonly"] = False
            else:
                temp["bg_color"] = (1, 1, 1)
                temp["is_readonly"] = True
            data.append(temp)

        return data

    def show_scores_history(self):
        if self.manager.current == "game":
            self.manager.current = "history"
            self.manager.current_screen.data = self.scores
        else:
            self.manager.current = "game"


    def save_score(self):
        current_score = {"idx": len(self.scores),
                         "date": datetime.now().strftime("%H:%M %d-%b-%y"),
                         "score": int(self.pb_score.value)}
        self.scores.append(current_score)
        self.scores.sort(key=lambda x: x["score"])
        with open("scores_history.txt", "w") as file:
            for row in self.scores:
                for value in row.values():
                    file.write(str(value) + ",")
                file.write("\n")



class Cell(BoxLayout):

    def didSelectCell(self, idx, mutatedWord):
        tb: TextInput = self.children[0]
        mutatedWord[idx] = tb.text
        if len(tb.text) == 1:
            next = tb.get_focus_next()
            if next is not None and next.is_focusable:
                next.focus = True
        print(mutatedWord)


class MyPopup(Popup):
    pass


sm = ScreenManager(transition=SlideTransition(direction="down"))
sm.add_widget(GuessWord(name='game'))
sm.add_widget(Factory.ScoresHistory(name='history'))


class GuessWordApp(App):
    def build(self):
        return sm


GuessWordApp().run()