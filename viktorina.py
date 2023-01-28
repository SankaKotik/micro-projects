from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pygame

def play ():
    def load_question (question_number):
        question.setText (questions_asks[question_number][0])
        option_1.setText (questions_asks[question_number][1][0])
        option_2.setText (questions_asks[question_number][1][1])
        option_3.setText (questions_asks[question_number][1][2])
        option_4.setText (questions_asks[question_number][1][3])
        status.setText ("Пользователь " + username + " Очки " + str(score) + " Жизни " + str(lifes))
    
    def complexity_checker ():
        global current_question_number, complexity
        if current_question_number < len (questions_asks) - 1:
            current_question_number += 1
            if questions_asks[current_question_number][3] <= complexity:
                load_question (current_question_number)
            else:
                complexity_checker ()
        else:
            game_over (True)
    
    def game_over (is_win):
        global current_question_number, score, lifes
        game_window.close ()
        
        game_over_window = QDialog ()
        game_over_layout = QVBoxLayout (game_over_window)
        
        score_display = QLCDNumber ()
        score_display.display (score)
        game_over_layout.addWidget (score_display)
        
        game_over_reason = QLabel ()
        game_over_reason_font = game_over_reason.font ()
        game_over_reason_font.setPointSize (12)
        game_over_reason.setFont (game_over_reason_font)
        game_over_reason.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        game_over_layout.addWidget (game_over_reason)
        
        close_game_over_window = QPushButton ("Закрыть")
        close_game_over_window.clicked.connect (game_over_window.close)
        game_over_layout.addWidget (close_game_over_window)
        
        if is_win == True:
            game_over_reason.setText ("Поздравляем, вы победили!")
            pygame.mixer.music.load ("tada.wav")
            pygame.mixer.music.play ()
        else:
            game_over_reason.setText ("Закончились жизни")
            pygame.mixer.music.load ("chord.wav")
            pygame.mixer.music.play ()
        
        game_over_window.exec ()
    
    def option_clicked (number):
        global current_question_number, score, lifes, username, complexity
        if number == questions_asks[current_question_number][2] - 1:
            score += questions_asks[current_question_number][3]
            lifes += 1
        else:
            lifes -= 1
        
        if lifes == 0:
            game_over (False)
        
        complexity_checker ()
    
    def option_1_clicked ():
        option_clicked (0)
    
    def option_2_clicked ():
        option_clicked (1)
    
    def option_3_clicked ():
        option_clicked (2)
    
    def option_4_clicked ():
        option_clicked (3)
    
    game_window = QDialog ()
    game_layout = QVBoxLayout (game_window)
    
    question = QLabel ()
    question_font = question.font ()
    question_font.setPointSize (12)
    question.setFont (question_font)
    question.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    game_layout.addWidget (question)
    
    status = QLabel ()
    status.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    game_layout.addWidget (status)
    
    answers_buttons = QHBoxLayout ()
    
    option_1 = QPushButton ()
    option_1.clicked.connect (option_1_clicked)
    answers_buttons.addWidget (option_1)
    
    option_2 = QPushButton ()
    option_2.clicked.connect (option_2_clicked)
    answers_buttons.addWidget (option_2)
    
    option_3 = QPushButton ()
    option_3.clicked.connect (option_3_clicked)
    answers_buttons.addWidget (option_3)
    
    option_4 = QPushButton ()
    option_4.clicked.connect (option_4_clicked)
    answers_buttons.addWidget (option_4)
    
    game_layout.addLayout (answers_buttons)
    
    global current_question_number, lifes, score
    current_question_number = -1
    lifes = 3
    score = 0
    complexity_checker ()
    
    game_window.exec ()

def settings ():
    def apply_settings ():
        global username, complexity
        username = username_field.text ()
        complexity = complexity_dial.value ()
    
    global username, complexity
    settings_window = QDialog ()
    settings_layout = QVBoxLayout (settings_window)
    
    settings_title = QLabel ("Настройки")
    settings_title_font = settings_title.font ()
    settings_title_font.setPointSize (16)
    settings_title.setFont (settings_title_font)
    settings_title.setAlignment (Qt.AlignmentFlag.AlignHCenter)
    settings_layout.addWidget (settings_title)
    
    username_layout = QHBoxLayout ()
    
    username_label = QLabel ("Имя пользователя")
    username_layout.addWidget (username_label)
    username_field = QLineEdit ()
    username_field.setText (username)
    username_field.textChanged.connect (apply_settings)
    username_layout.addWidget (username_field)
    
    settings_layout.addLayout (username_layout)
    
    complexity_label = QLabel ("Сложность вопросов")
    settings_layout.addWidget (complexity_label)
    
    complexity_dial = QDial ()
    complexity_dial.setRange (1, 7)
    complexity_dial.valueChanged.connect (apply_settings)
    complexity_dial.setValue (complexity)
    settings_layout.addWidget (complexity_dial)
    
    apply_button = QPushButton ("Закрыть")
    apply_button.clicked.connect (settings_window.close)
    settings_layout.addWidget (apply_button)
    
    settings_window.exec ()

def rules ():
    rules_window = QDialog ()
    rules_layout = QVBoxLayout (rules_window)
    
    rules_title = QLabel ("Правила")
    rules_title_font = rules_title.font ()
    rules_title_font.setPointSize (16)
    rules_title.setFont (rules_title_font)
    rules_title.setAlignment (Qt.AlignmentFlag.AlignHCenter)
    rules_layout.addWidget (rules_title)
    
    rules_label = QLabel ("Основные и главные правила:\n - Игрок получает очки за правильный ответ на вопрос;\n - Игрок проходит дальше за правильный ответ;\n - Игрок теряет жизнь при неправильном ответе.")
    rules_layout.addWidget (rules_label)
    
    close_button = QPushButton ("Закрыть")
    close_button.clicked.connect (rules_window.close)
    rules_layout.addWidget (close_button)
    
    rules_window.exec ()

def info ():
    info_window = QDialog ()
    info_layout = QVBoxLayout (info_window)
    
    info_title = QLabel ("Информация")
    info_title_font = info_title.font ()
    info_title_font.setPointSize (16)
    info_title.setFont (info_title_font)
    info_title.setAlignment (Qt.AlignmentFlag.AlignHCenter)
    info_layout.addWidget (info_title)
    
    info_label = QLabel ("Мой гитхаб: github.com/SankaKotik")
    info_layout.addWidget (info_label)
    
    close_button = QPushButton ("Закрыть")
    close_button.clicked.connect (info_window.close)
    info_layout.addWidget (close_button)
    
    info_window.exec ()

app = QApplication ([])
main_window = QWidget ()
main_layout = QVBoxLayout (main_window)

pygame.init ()

questions_asks = [["Вопрос1", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 1], ["Вопрос2", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 2], ["Вопрос3", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 3], ["Вопрос4", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 4], ["Вопрос5", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 5], ["Вопрос6", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 6], ["Вопрос7", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 7], ["Вопрос8", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 1], ["Вопрос9", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 2], ["Вопрос10", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 3], ["Вопрос11", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 4], ["Вопрос12", ["Ответ1", "Ответ2", "Ответ3", "Ответ4"], 1, 5]]
username = ""
current_question_number = -1
complexity = 7
score = 0
lifes = 3

title = QLabel ("Викторина")
title_font = title.font ()
title_font.setPointSize (24)
title.setFont (title_font)
title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
main_layout.addWidget (title)

play_button = QPushButton ("Играть")
play_button.clicked.connect (play)
main_layout.addWidget (play_button)

buttons_layout = QHBoxLayout ()

settings_button = QPushButton ("Настройки")
settings_button.clicked.connect (settings)
buttons_layout.addWidget (settings_button)

rules_button = QPushButton ("Правила")
rules_button.clicked.connect (rules)
buttons_layout.addWidget (rules_button)

info_button = QPushButton ("Информация")
info_button.clicked.connect (info)
buttons_layout.addWidget (info_button)

main_layout.addLayout (buttons_layout)

main_window.show ()
app.exec ()
