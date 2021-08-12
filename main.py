import easygui
import random

easygui.msgbox(
    "Setzen Sie Ihre Markierung in ein freies Feld. Der Spieler, der als Erstes drei gleiche Farben in eine Zeile, Spalte oder Diagonale setzt gewinnt.",
    title="Willkommen zum Tic Tac Toe"
)

import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QButtonGroup, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# ein Beispiel, bei dem neun Buttons einer BuutonGroup zugeordnet werden und die Group auf die Klicks reagiert

player = True
win = False

def grp_click(btn):
    global player
    if(player):
      btn.setStyleSheet("background-color: yellow")
      btn.setText("yellow")
      btn.setEnabled(False)
      print("Player A hat " + str(btn.text()) + " geklickt")
    else:
      btn.setStyleSheet("background-color: blue")
      btn.setText("blue")
      btn.setEnabled(False)
      print ("Player B hat " + str(btn.text()) + " geklickt")
    player = not(player)


class TikTakTok(QMainWindow):
    def __init__(self, player1=None, player2=None):
        super().__init__()

        self.setWindowTitle("Tik Tak Tok Game")
        
        # set the players
        self._define_players(player1, player2)

        # get the windows size
        self.setGeometry(100, 100, 300, 500)

        # set the GUI
        self._define_ui()

        if self.player['is_computer']:
            self._computer_play()


    def _define_players(self, player1, player2):
        if not player1:
            self.player_1 = {
                "name": "Payer 1",
                "value": "X",
                "color": "yellow"
            }
        else:
            self.player_1 = player1

        if not player2:
            self.player_2 = {
                "name": "Payer 2",
                "value": "X",
                "color": "blue"
            }
        else:
            self.player_2 = player2

        # set player to player 1

        self.player = self.player_1

    def _switch_player(self):
        if self.player == self.player_1:
            self.player = self.player_2
        else:
            self.player = self.player_1

    def _define_ui(self):
        # turn
        self.turn = 0

        # times
        self.times = 0

        self.buttons = []

        # create the grid(3x3 grid) that content 9 buttons
        for i in range(3):
            row = []
            for j in range(3):
                row.append(QPushButton(self))
            self.buttons.append(row)

        # x and y co-ordinate
        x = 90
        y = 90

        for i in range(3):
            for j in range(3):
                # set the text to ""
                self.buttons[i][j].setText("")

                # set the buttons sizes
                self.buttons[i][j].setGeometry(x*i + 20, y*j + 20, 80, 80)

                # setting font to the button
                self.buttons[i][j].setFont(QFont(QFont('Times', 17)))

                # add the function to call when the button is clicked
                self.buttons[i][j].clicked.connect(self._play)

        # creating label to tel the score
        self.label = QLabel(self)
  
        # setting geometry to the label
        self.label.setGeometry(20, 300, 260, 60)
  
        # setting style sheet to the label
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 3px solid grey;"
                                 "background : white;"
                                 "}")
  
        # setting label alignment
        self.label.setAlignment(Qt.AlignCenter)

        # setting font to the label
        self.label.setFont(QFont('Times', 15))

        self.label.setText(f"{self.player['name']} turn")

        # creating push button to restart the score
        self.reset_game = QPushButton("Reset-Game", self)
  
        # setting geometry
        self.reset_game.setGeometry(50, 380, 200, 50)
  
        # adding action action to the reset push button
        self.reset_game.clicked.connect(self._reset_the_game)


    def _play(self):
        self.times += 1

        # get the button that the user clicked on
        btn = self.sender()

        # change the text of the btn
        btn.setText(self.player.get("value"))

        # change the size of the btn
        btn.setStyleSheet(f"background-color: {self.player.get('color')}")

        # desable the button
        btn.setEnabled(False)

        game_is_win = self._check_winner()

        # the text that will be schow
        text = ""

        if game_is_win:
            text = f"{self.player['name']} has win the game"

            # desable all the buttons in cas one player win so that it will not be possible to play
            for btns in self.buttons:
                for btn in btns:
                    btn.setEnabled(False)

            # setting text to the label
            self.label.setText(text)
            return

        # if winner is not decided and total times is 9, the game has no issue
        elif self.times == 9:
            print(self.times)
            text = "This Game has no issue"

            # setting text to the label
            self.label.setText(text)
            return

        # change the current player
        self._switch_player()

        # change the text for the player
        self.label.setText(f"{self.player['name']} turn")

        ### if the player is a computer and play automatic
        if self.player['is_computer']:
            self._computer_play()

    def _computer_play(self):
        frei_buttton = []
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].text() == "":
                    frei_buttton.append((i,j))
            
        size = len(frei_buttton)

        if size <= 1:
            idx = 0
        else:
            idx = random.randint(0, size-1)

        btn_i, btn_j = frei_buttton[idx]

        self.buttons[btn_i][btn_j].clicked.emit()

    def _check_winner(self):
        # check the all the rows (if the row has the same text)
        for i in range(3):
            if self.buttons[0][i].text() == self.buttons[1][i].text() \
                    and self.buttons[0][i].text() == self.buttons[2][i].text() \
                    and self.buttons[0][i].text() != "":
                return True

        # check the all the columns (if the column has the same text)
        for i in range(3):
            if self.buttons[i][0].text() == self.buttons[i][1].text() \
                    and self.buttons[i][0].text() == self.buttons[i][2].text() \
                    and self.buttons[i][0].text() != "":
                return True

        # check the first diagonal
        if self.buttons[0][0].text() == self.buttons[1][1].text() \
                and self.buttons[0][0].text() == self.buttons[2][2].text() \
                and self.buttons[0][0].text() != "":
            return True

        # check the second diagonal
        if self.buttons[0][2].text() == self.buttons[1][1].text() \
                and self.buttons[0][2].text() == self.buttons[2][0].text() \
                and self.buttons[0][2].text() != "":
            return True

        # when any of there condition is true then we continue
        return False
        
    def _reset_the_game(self):
        # resetting values
        self.times = 0
  
        # making label text empty:
        self.label.setText("")
  
        # traversing push list
        for buttons in self.buttons:
            for button in buttons:
                # making all the button enabled
                button.setEnabled(True)
                # removing text of all the buttons
                button.setText("")

                # removing text'stylesheet of all the buttons
                button.setStyleSheet("")

        self.player = self.player_1

        # change the text for the player
        self.label.setText(f"{self.player['name']} turn")

        if self.player['is_computer']:
            self._computer_play()


def main():
    player_1 = {
        "name": "Alex",
        "value": "X",
        "color": "blue",
        "is_computer": True
    }

    player_2 = {
        "name": "Computer",
        "value": "O",
        "color": "yellow",
        "is_computer": True
    }

    app = QApplication(sys.argv)

    game = TikTakTok(player1=player_1, player2=player_2)

    game.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()