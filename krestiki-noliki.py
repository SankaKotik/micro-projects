from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from random import randrange
import pygame
import json

def play ():
    def bot_move ():
        global current_index
        row_rand = randrange (0, rows)
        column_rand = randrange (0, columns)
        if all_buttons[row_rand][column_rand].text () == " ":
            all_buttons[row_rand][column_rand].setText (sym[2])
            history.addItem (f"Компьютер поставил O на {[row_rand, column_rand]}")
            if game_over_check (2) == False:
                if draw_check () == False:
                    current_index = 0
        else:
            bot_move ()
    
    def game_over_check (gamer_index):
        for column in range (columns):
            i = 0
            for row in range (rows):
                if all_buttons[row][column].text () == sym[gamer_index]:
                    i += 1
            if i >= rows:
                game_over (gamer_index, "по вертикали")
                return True
        for row in range (rows):
            i = 0
            for column in range (columns):
                if all_buttons[row][column].text () == sym[gamer_index]:
                    i += 1
            if i >= columns:
                game_over (gamer_index, "по горизонтали")
                return True
        if rows == columns:
            i = 0
            for row in range (rows):
                for column in range (columns):
                    if row == column:
                        if all_buttons[row][column].text () == sym[gamer_index]:
                            i += 1
            if i >= rows:
                game_over (gamer_index, "по диагонали")
                return True
            
            i = 0
            for row in range (rows):
                for column in range (columns):
                    if row == rows - column - 1:
                        if all_buttons[row][column].text () == sym[gamer_index]:
                            i += 1
            if i >= rows:
                game_over (gamer_index, "по обратной диагонали")
                return True
        return False
    
    def draw_check ():
        i = 0
        for row in range (rows):
            for column in range (columns):
                if all_buttons[row][column].text () == " ":
                    i += 1
        if i < 1:
            game_over (-1, "не осталось клеток")
            return True
        return False
    
    def game_over (winner_index, win_type):
        global all_stats
        game_window.close ()
        
        game_over_window = QDialog ()
        game_over_layout = QVBoxLayout (game_over_window)
        
        game_over_title = QLabel ()
        game_over_title_font = game_over_title.font ()
        game_over_title_font.setPointSize (12)
        game_over_title.setFont (game_over_title_font)
        game_over_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        game_over_layout.addWidget (game_over_title)
        
        game_over_reason = QLabel ()
        game_over_reason.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        game_over_layout.addWidget (game_over_reason)
        
        close_game_over_window = QPushButton ("Закрыть")
        close_game_over_window.clicked.connect (game_over_window.close)
        game_over_layout.addWidget (close_game_over_window)
        
        if winner_index != -1:
            game_over_title.setText (f"Победа за {username[winner_index]}")
            game_over_reason.setText (f"{sym[winner_index]} обыграли {win_type}")
            all_stats [winner_index][0] += 1
            if enable_bot == True:
                all_stats [2 - winner_index][1] += 1
            else:
                all_stats [not winner_index][1] += 1
            try:
                pygame.mixer.music.load ("tada.wav")
                pygame.mixer.music.play ()
            except:
                print ("Невозможно проиграть мелодию")
        else:
            game_over_title.setText ("Ничья")
            game_over_reason.setText (f"Ничья: {win_type}")
            all_stats [0][2] += 1
            if enable_bot == True:
                all_stats [2][2] += 1
            else:
                all_stats [1][2] += 1
            try:
                pygame.mixer.music.load ("chord.wav")
                pygame.mixer.music.play ()
            except:
                print ("Невозможно проиграть мелодию")
        
        game_over_window.exec ()
    
    def search_button (obj):
        for column in range (columns):
            for row in range (rows):
                if all_buttons[row][column] == obj:
                    return [row, column]
    
    def button_clicked ():
        global current_index, current_username
        if QObject().sender().text() == " ":
            QObject().sender().setText (sym[current_index])
            history.addItem (f'{username[current_index]} поставил {sym[current_index]} на {search_button (QObject().sender())}')
            if game_over_check (current_index) == False:
                if draw_check () == False:
                    if enable_bot == True:
                        current_index = 2
                        bot_move ()
                    else:
                        current_index = not current_index
                    status.setText (f'Ходит {username[current_index]}')
                            
    
    game_window = QDialog ()
    game_layout = QVBoxLayout (game_window)
    
    global current_index
    current_index = 0
    
    all_buttons = []
    buttons = QGridLayout ()
    
    for row in range (rows):
        current_row = []
        for column in range (columns):
            button = QPushButton (" ")
            button.clicked.connect (button_clicked)
            current_row.append (button)
            buttons.addWidget (button, row, column)
        all_buttons.append (current_row)
    
    game_layout.addLayout (buttons)
    
    status_title = QLabel ("Информация")
    status_title_font = status_title.font ()
    status_title_font.setPointSize (12)
    status_title.setFont (status_title_font)
    status_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    game_layout.addWidget (status_title)
    
    status = QLabel (f"Ходит {username[current_index]}")
    status.setAlignment (Qt.AlignmentFlag.AlignHCenter)
    game_layout.addWidget (status)
    
    history = QListWidget ()
    game_layout.addWidget (history)
    
    game_window.exec ()

def settings ():
    def gamers_changed (index):
        if index == 0:
            username_field.setText (username[0])
            sym_field.setText (sym[0])
        elif index == 1:
            username_field.setText (username[1])
            sym_field.setText (sym[1])
    
    def lock_gamers (state):
        global enable_bot
        gamers.setCurrentIndex (0)
        enable_bot = bool(state)
        gamers.setEnabled (not enable_bot)
    
    def username_update (val):
        global username
        if gamers.currentIndex () == 0:
            username[0] = val
            gamers.setItemText (0, val)
        else:
            username[1] = val
            gamers.setItemText (1, val)
    
    def sym_update (val):
        global sym
        if gamers.currentIndex () == 0:
            sym[0] = val
        else:
            sym[1] = val
    
    def rows_update (val):
        global rows
        rows = val
        size_label.setText (f"Поле: {rows}x{columns}")
    
    def columns_update (val):
        global columns
        columns = val
        size_label.setText (f"Поле: {rows}x{columns}")
    
    settings_window = QDialog ()
    settings_layout = QVBoxLayout (settings_window)
    
    settings_title = QLabel ("Настройки")
    settings_title_font = settings_title.font ()
    settings_title_font.setPointSize (16)
    settings_title.setFont (settings_title_font)
    settings_title.setAlignment (Qt.AlignmentFlag.AlignHCenter)
    settings_layout.addWidget (settings_title)
    
    play_with_bot = QCheckBox ("Играть с компьютером")
    play_with_bot.setChecked (int (enable_bot))
    play_with_bot.stateChanged.connect (lock_gamers)
    play_with_bot.setToolTip ("Если вы играете с компьютером, вместо второго игрока будет играть бот на основе генератора случаных чисел")
    settings_layout.addWidget (play_with_bot)
    
    gamers = QComboBox ()
    gamers.addItems ([username[0], username[1]])
    gamers.setEnabled (not enable_bot)
    gamers.currentIndexChanged.connect (gamers_changed)
    gamers.setToolTip ("Выбор настраиваемого игрока")
    settings_layout.addWidget (gamers)
    
    form_layout = QFormLayout ()
    
    username_field = QLineEdit ()
    username_field.setText (username[0])
    username_field.textEdited.connect (username_update)
    username_field.setToolTip ("Псевдоним настраиваемого игрока, отображаемый в статистике")
    
    sym_field = QLineEdit ()
    sym_field.setText (sym[0])
    sym_field.setMaxLength (1)
    sym_field.textEdited.connect (sym_update)
    sym_field.setToolTip ("Символ, который будет появляться на поле, когда настраиваемый игрок будет ходить")
    
    form_layout.addRow ("Ник: ", username_field)
    form_layout.addRow ("Символ: ", sym_field)
    
    settings_layout.addLayout (form_layout)
    
    size_label = QLabel (f"Поле: {rows}x{columns}")
    size_label.setAlignment (Qt.AlignmentFlag.AlignHCenter)
    settings_layout.addWidget (size_label)
    
    size_layout = QHBoxLayout ()
    
    rows_dial = QDial ()
    rows_dial.setRange (2, 20)
    rows_dial.setValue (rows)
    rows_dial.valueChanged.connect (rows_update)
    rows_dial.setToolTip ("Количество рядов на поле")
    
    columns_dial = QDial ()
    columns_dial.setRange (2, 20)
    columns_dial.setValue (columns)
    columns_dial.valueChanged.connect (columns_update)
    columns_dial.setToolTip ("Количество колонок на поле")
    
    size_layout.addWidget (rows_dial)
    size_layout.addWidget (columns_dial)
    
    settings_layout.addLayout (size_layout)
    
    apply_button = QPushButton ("Закрыть")
    apply_button.clicked.connect (settings_window.close)
    settings_layout.addWidget (apply_button)
    
    settings_window.exec ()

def stats ():
    stats_window = QDialog ()
    stats_layout = QVBoxLayout (stats_window)
    
    stats_title = QLabel ("Статистика")
    stats_title_font = stats_title.font ()
    stats_title_font.setPointSize (16)
    stats_title.setFont (stats_title_font)
    stats_title.setAlignment (Qt.AlignmentFlag.AlignHCenter)
    stats_layout.addWidget (stats_title)
    
    stats_table = QTableWidget (3, 4)
    
    stats_table.setHorizontalHeaderLabels (["Победа", "Поражение", "Ничья", "Очки"])
    stats_table.setVerticalHeaderLabels (username)
    stats_table.horizontalHeaderItem(0).setToolTip ("Количество побед игрока")
    stats_table.horizontalHeaderItem(1).setToolTip ("Количество поражений игрока")
    stats_table.horizontalHeaderItem(2).setToolTip ("Количество ничьих игрока")
    stats_table.horizontalHeaderItem(3).setToolTip ("Общее количество очков")
    
    stats_table.verticalHeaderItem(0).setToolTip ("1 (основной) игрок, назначенный в настройках")
    stats_table.verticalHeaderItem(1).setToolTip ("2 (дополнительный) игрок, назначенный в настройках")
    stats_table.verticalHeaderItem(2).setToolTip ("Бот на базе генератора случайных чисел")
    
    for i in range (3):
        for j in range (3):
            item = QTableWidgetItem (str (all_stats[i][j]))
            stats_table.setItem (i, j, item)
        item = QTableWidgetItem (str (int (all_stats[i][0] * 5 + all_stats[i][1] * -6 + all_stats[i][2] * -1.2)))
        stats_table.setItem (i, 3, item)
    
    stats_layout.addWidget (stats_table)
    
    close_button = QPushButton ("Закрыть")
    close_button.clicked.connect (stats_window.close)
    stats_layout.addWidget (close_button)
    
    stats_window.exec ()

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

try:
    with open ("config.json", "r") as read_config:
        [username, all_stats, enable_bot, sym, rows, columns] = json.load (read_config)
except:
    username = ["Gamer", "Gamer 2", "Компьютер"]
    all_stats = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    enable_bot = False
    sym = ["X", "O", "O"]
    rows = 3
    columns = 3

title = QLabel ("Крестики - Нолики")
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

stats_button = QPushButton ("Статистика")
stats_button.clicked.connect (stats)
buttons_layout.addWidget (stats_button)

info_button = QPushButton ("Информация")
info_button.clicked.connect (info)
buttons_layout.addWidget (info_button)

main_layout.addLayout (buttons_layout)

main_window.show ()
app.exec ()

with open ("config.json", "w") as write_config:
    json.dump ([username, all_stats, enable_bot, sym, rows, columns], write_config)
