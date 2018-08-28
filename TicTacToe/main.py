# following the Build tic-tac-toe with Kivy guide by Alexander Taylor:
# https://www.gadgetdaily.xyz/build-tic-tac-toe-with-kivy/

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import (ListProperty, NumericProperty)
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label

class TicTacToeApp(App):

    def build(self):
        return TicTacToeGrid()

class TicTacToeGrid(GridLayout):
    status = ListProperty([0 for _ in range(9)])  # list that keeps state of the board
    current_player = NumericProperty(1)  # number representing the current player (1 for 'O', -1 for 'X')

    def __init__(self, *args, **kwargs):
        super(TicTacToeGrid, self).__init__(*args, **kwargs)  # calls the __init__ method of the superClass of
        # TicTacToeGrid which is GridLayout
        # super().__init__(*args, **kwargs) <--- for Python 3
        self.SIZE = 3
        self.GRID = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]  # self.SIZE x self.SIZE 2d list

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                grid_entry = GridEntry(coords=(row, col))
                grid_entry.bind(on_release=self.button_pressed)  # when pressed, the button_pressed method is called
                self.add_widget(grid_entry)  # adds the grid_entry widget to the TicTacToeGrid widget

    def button_pressed(self, button):
        # player symbols and colour lookups
        player = {1: 'O', -1: 'X'}
        colours = {1: (1, 0, 0, 1), -1: (0, 1, 0, 1)}  # 'O' is red, 'X' is green

        row, col = button.coords

        # 2D grid index into 1D status index
        status_index = 3*row + col
        already_played = self.status[status_index]

        # If nobody played here yet, make a new move
        if not already_played:
            self.status[status_index] = self.current_player
            button.text = player[self.current_player]
            button.background_color = colours[self.current_player]
            self.current_player *= -1  # switch current player

        print('{} button clicked'.format(button.coords))

    # when status property changes the on_status (on_propertyname) is called (works with every property)
    def on_status(self, instance, new_value):
        status = new_value  # updates the status property with new value

        # Sum each row, column and diagonal.
        # Could be shorter, but let’s be extra
        # clear what’s going on
        sums = [sum(status[0:3]), sum(status[3:6]), sum(status[6:9]),  # rows
                sum(status[0::3]), sum(status[1::3]), sum(status[2::3]),  # columns
                sum(status[0::4]), sum(status[2:7:2])  # diagonals
                ]

        winner = None

        if 3 in sums:
            winner = 'Kolečka vítězí!'
        elif -3 in sums:
            winner = 'Křížky vítězí!'
        elif 0 not in status:
            winner = 'Remíza ... nikdo nezvítězil!'

        if winner:
            popup = ModalView(size_hint=(0.75, 0.5))
            victory_label = Label(text=winner, font_size=50)
            popup.add_widget(victory_label)
            popup.bind(on_dismiss=self.reset)
            popup.open()

    def reset(self, *args):
        self.status = [0 for _ in range(9)]

        # self.children == list containing all child widgets
        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1)

        self.current_player = 1


class GridEntry(Button):
    coords = ListProperty([0, 0])

if __name__ == '__main__':
    tttApp = TicTacToeApp()
    tttApp.run()

