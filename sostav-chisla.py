from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from threading import Timer
from time import sleep
import random
import pygame

def play ():
    def bg_timer ():
        try: timer ()
        except: pass
        
    def timer ():
        question.setText (f'{true_answer}')
        pygame.mixer.music.load ("tick.wav")
        pygame.mixer.music.play ()
        sleep (5)
        load_question (True)
    
    def load_question (killproc):
        global true_answer, proc
        if enable_timer.isChecked () and killproc:
            proc.cancel ()
        x = random.randint (1, 19)
        y = random.randint (1, 20 - x)
        question.setText (f'{x} + {y} = ')
        true_answer = x + y
        if enable_timer.isChecked ():
            proc = Timer (5, bg_timer)
            proc.start ()
    
    def answer_changed ():
        if answer.text () == str (true_answer):
            pygame.mixer.music.load ("tada.wav")
            pygame.mixer.music.play ()
        else:
            pygame.mixer.music.load ("chord.wav")
            pygame.mixer.music.play ()
        
        answer.setText ('')
        load_question (True)
    
    game_window = QDialog ()
    game_layout = QVBoxLayout (game_window)
    
    question = QLabel ()
    question_font = question.font ()
    question_font.setPointSize (96)
    question.setFont (question_font)
    question.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    game_layout.addWidget (question)
    
    answer = QLineEdit ()
    answer.returnPressed.connect (answer_changed)
    game_layout.addWidget (answer)
    
    load_question (False)
    
    game_window.exec ()

app = QApplication ([])
main_window = QWidget ()
main_layout = QVBoxLayout (main_window)

pygame.init ()

title = QLabel ("Состав числа")
title_font = title.font ()
title_font.setPointSize (24)
title.setFont (title_font)
title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
main_layout.addWidget (title)

play_button = QPushButton ("Играть")
play_button.clicked.connect (play)
main_layout.addWidget (play_button)

enable_timer = QCheckBox ("На время")
main_layout.addWidget (enable_timer)

main_window.show ()
app.exec ()
