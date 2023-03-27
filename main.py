"""
Premier League match predictor iunie 2020 pentru sezonul 2020-2021
De Florian Mihalcioiu

Cerinte:
--------------
pip3 install pillow
pip3 install wget

gui.py si imaginea SafeGuardingLead.jpg
ambele in acelasi fisier de unde este rulat main.py

-------------------
Ratingurile echipelor sunt updatate pentru a reflecta cat mai bine forma curenta, pozitia din clasament, rezultatele din ultimele 5 meciuri etc.
"""
import os
from random import randint
import sys
from tkinter import Button, E, LabelFrame, messagebox, Label, Menu, W, Tk
from tkinter.ttk import Combobox
from typing import Optional, Any

import PIL
from PIL import Image, ImageTk
import webbrowser
import wget
import gui

root = Tk()

# Setarea ferestrei principale
root.title('Premier League match predictor')
root.resizable(False, False)

# Inserare logo.
logo_frame = LabelFrame(root)
logo_frame.grid(padx=8, pady=8)
logo_image = Image.open('SafeGuardingLead.jpg')
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(logo_frame, image=logo_photo)
logo_label.logo_image = logo_photo
logo_label.grid(padx=2, pady=2, row=0, column=0)


def info_menu():
    """Submeniul 'Info'."""
    messagebox.showinfo('Informatii despre aplicatie', 'Premier League match predictor '
                        'iunie 2020\n'
                        '\nPentru sezonul 2020-2021 din Premier League - Anglia.\n\n'
                        'de Florian Mihalcioiu.\n\n')
def help_menu():
    """Cum se foloseste programul - submeniul Ajutor."""
    messagebox.showinfo('Cum se foloseste...', 'Premier League match predictor\n' ' 2020\n\n'
                        'Pentru a obtine o predictie pentru orice meci din sezonul 2019-2020 de Premier League'
                        'mai intai selectati echipa gazda din lista din partea stanga, '
                        'apoi selectati echipa oaspete din lista din dreapta\n\n'
                        'Acum apasati pe butonul rosu <=-Predictie rezultat-=> \n'
                        'pentru a primi o predictie.\n\n'
                        'Puteti apasa de asemenea pe \n<=- Consultati statisticile echipei -=> '
                        'pentru a fi directionat catre o pagină web cu ultimele statistici ale echipei.'
                        '\n\nDaca apasati pe Meniu (in coltul stanga sus) puteti vedea informatii despre aceasta aplicatie')

def exit_app():
    """Iesire din program: Da-NU."""
    ask_yn = messagebox.askyesno('Atentie',
                                 'Doriti sa parasiti Premier League match predictor?')
    if ask_yn is False:
        return
    root.destroy()
    sys.exit()

def view_pl_stats():
    """Deschidere browser pentru a vedea ultimele informatii despre echipe si jucatori."""
    webbrowser.open('https://fbref.com/en/comps/9/Premier-League-Stats')

# Drop-down menu.
MENU_BAR = Menu(root)
FILE_MENU = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='Meniu', menu=FILE_MENU)
FILE_MENU.add_command(label='Ajutor', command=help_menu)
FILE_MENU.add_command(label='Info', command=info_menu)
FILE_MENU.add_separator()
FILE_MENU.add_command(label='Iesire', command=exit_app)
root.config(menu=MENU_BAR)

# Setare dictionar, echipe, greutati.
# Rating-urile au fost updatate in august 2020 in functie de pozitia din clasament din sezonul
# 2019-2020, de rezultatul ultimelor 10 meciuri (forma de moment) si de valoarea clubului
TEAM = {
    'Arsenal': 6,
    'Aston Villa': 1,
    'Brighton': 1,
    'Burnley': 3,
    'Chelsea': 7,
    'Crystal Palace': 1,
    'Everton': 3,
    'Fulham': 1,
    'Leicester': 4,
    'Leeds United': 1,
    'Liverpool': 9,
    'Manchester City': 9,
    'Manchester Utd': 8,
    'Newcastle': 1,
    'Sheff Utd': 2,
    'Southampton': 3,
    'Tottenham': 7,
    'West Brom': 1,
    'West Ham': 2,
    'Wolves': 5
}

def prediction():
    """Afiseaza predictii."""
    home_team = ht_combo.get()
    away_team = at_combo.get()

    # Daca se alege aceeasi echipa pentru si pentru gazde si pentru oaspeti.
    if away_team == home_team:
        messagebox.showinfo("Avertisment","Va rugăm alegeți două echipe diferite...")
        return

    # htw = home team weighting
    htw = TEAM[home_team]
    htw += 1 # 1pct adaugat pentru gazde
    atw = TEAM[away_team]

    # Calculare predictie scor.
    # functia 'abs' da rezultatul absolut al diferentei dintre rating-uri.
    home_score = 0
    away_score = 0
    orig_diff = 0
    ratings_diff = abs(htw-atw)

    # Limitare maxim 4 goluri inscrise de o echipa.
    if ratings_diff > 4:
        orig_diff = ratings_diff
        ratings_diff = 4

    # Daca ambele echipe au acelasi ranking rezultatul va fi unul random
    # Am limitat ca scorul sa scorul sa nu depaseasca 2-2, intrucat un rezultat precum 3-3 sau 4-4 sunt destul de neobisnuite.
    if htw == atw:
        result = 'Egalitate'
        rnd_drawscore = (randint(0, 2)) #Limitare la rezultate de 0-0, 1-1 or 2-2.
        away_score = rnd_drawscore
        home_score = rnd_drawscore

    if htw > atw:
        result = 'Victorie gazde'
        away_score = 0
        home_score = ratings_diff
        if abs(ratings_diff-orig_diff) > 2:
            away_score = (randint(0, 1))

    if htw < atw:
        result = 'Victorie oaspeti'
        home_score = 0
        away_score = ratings_diff
        if abs(ratings_diff-orig_diff) > 2:
            home_score = 1

    predicted_score = (str(home_score)+' - '+str(away_score))

    result_msg = ' Ati selectat:\n {} V {} \n\n Predictia este:\n {}'  \
                 '\n\n Scorul prezis : {}'  \
                 .format(home_team, away_team, result, predicted_score)

    messagebox.showinfo('PL Predictor', 'Rating ajustat:\n'
                        'Echipa gazda: ' +str(htw)+'pct,\nEchipa oaspete: '
                        +str(atw)+'pct.\n\n'+str(result_msg))

# Dict to lists.
team_list = (list(TEAM.keys()))
team_values = (list(TEAM.values()))

# Label texts.
msg_frame = LabelFrame(root)
msg_frame.grid(padx=8, pady=8)
sel_ht_label = Label(msg_frame, bg='skyblue', text='Selectati echipa gazda')
sel_ht_label.grid()
sel_at_label = Label(msg_frame, bg='yellow', text='Selectati echipa oaspete')
sel_at_label.grid(row=0, column=1)

# Combo boxes.
ht_combo = Combobox(msg_frame)
ht_combo['values'] = (team_list)
ht_combo.current(16)
ht_combo.grid(padx=5, pady=5)

at_combo = Combobox(msg_frame)
at_combo['values'] = (team_list)
at_combo.current(9)
at_combo.grid(padx=5, pady=5, row=1, column=1)

# Frame for the predict and stats buttons.
btns_frame = LabelFrame(root)
btns_frame.grid(padx=8, pady=8)

# Predict button.
predict_btn = Button(btns_frame, bg='indianred',
                     text='<=- Predictie rezultat -=>',
                     command=prediction)
predict_btn.grid(sticky=W+E, padx=5, pady=5)

# Stats button.
stats_btn = Button(btns_frame, bg='cornflowerblue',
                   text='<=- Statistici echipe -=>',
                   command=view_pl_stats)
stats_btn.grid(sticky=W+E, padx=5, pady=5)

# Tooltips.
gui.Create(ht_combo, 'Selectati echipa gazda')
gui.Create(at_combo, 'Selectati echipa oaspete')

gui.Create(stats_btn, 'Vedeti statisticile tuturor echipelor si jucatorilor din Premier League.', showtime=6)

gui.Create(predict_btn, 'Click pentru predictie rezultat')
gui.Create(logo_frame, 'PL predictor iunie 2020',
             bgcol='salmon', showtime=6)

# Verifica daca s-a apasat click pe icon-ul X de inchidere.
root.protocol("WM_DELETE_WINDOW", exit_app)

root.mainloop()