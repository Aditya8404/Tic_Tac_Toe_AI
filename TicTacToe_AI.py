import sys
import pygame
import copy
import random
import numpy as np

from Variables_Values import *

import streamlit as st

st.set_page_config(page_title="My Data App", layout="wide")

st.header("Hi, I'm Aditya Punia :wave:")
st.title("Welcome to my Tic-Tac-Toe Game!")

st.write("---")

# Controls
st.subheader("Controls")
st.text("Default Diffuculty is HARD")
st.text("To Change Difficulty level to Easy => Press 'E'")
st.text("To Change Difficulty level to Hard again => Press 'H'")
st.text("To Change Game Mode to Human vs Human => Press 'G'")
st.text("To Restart the Game => Press 'R'")

# PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE AI-BOT")
screen.fill(BG_Color)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLUMNS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            return 0 if there is no win yet
            return 1 if player 1 win
            return 2 if player 2 win
        '''
        # vertical wins
        for col in range(COLUMNS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    if self.squares[0][col] == 2:
                        color = CIRCLE_COLOR
                    else:
                        color = CROSS_COLOR

                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)

                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    if self.squares[row][0] == 2:
                        color = CIRCLE_COLOR
                    else:
                        color = CROSS_COLOR

                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # descending diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                if self.squares[1][1] == 2:
                    color = CIRCLE_COLOR
                else:
                    color = CROSS_COLOR

                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # ascending diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                if self.squares[1][1] == 2:
                    color = CIRCLE_COLOR
                else:
                    color = CROSS_COLOR

                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # if no win yet
        return 0

    def mark_sq(self, row, column, player):
        self.squares[row, column] = player
        self.marked_sqrs += 1

    def empty_sq(self, row, column):
        return self.squares[row][column] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.empty_sq(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs ==  9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player

    def random(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        
        return empty_sqrs[idx]         # (row, column)

    def minimax(self, board, maximizing):

        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sq(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sq(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move
                

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.random(main_board)

        else:
            # mini-max algo choice
            eval, move = self.minimax(main_board, False)

        print(f"AI has chosen to mark at the position {move} with an evaluation of {eval}")

        return move     # row, col

class GAME:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1          # player 1 => CROSS and player 2 => CIRCLE
        self.gamemode = 'ai'     # pvp mode or AI mode
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sq(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        # background
        screen.fill( BG_Color )

        # Vertical line
        pygame.draw.line(screen, LINE_Color, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_Color, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal line
        pygame.draw.line(screen, LINE_Color, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_Color, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, column):
        if self.player == 1:
            # draw cross
            # descending line
            start_desc = (column * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (column * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # ascending line
            start_asc = (column * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (column * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            #draw circle
            center = (column * SQSIZE + SQSIZE//2 , row * SQSIZE + SQSIZE//2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def next_turn(self):
        self.player = (self.player % 2) + 1

    def change_gamemode(self):
        if self.gamemode == 'pvp':
            self.gamemode = 'ai'
        else:
            self.gamemode = 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()


def main():

    game = GAME()
    board = game.board
    ai = game.ai
    
    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # g => Game Mode (PvP to AI or AI to pvp)
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r => Restart Game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # e => Random AI (Easy mode)
                if event.key == pygame.K_e:
                    ai.level = 0

                # h => Minimax AI (Hard mode)
                if event.key == pygame.K_h:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                column = pos[0] // SQSIZE

                if board.empty_sq(row, column) and game.running:
                    game.make_move(row, column)  

                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # update the screen
            pygame.display.update()

            # AI methods
            row, column = ai.eval(board)
            game.make_move(row, column)

            if game.isover():
                game.running = False

        pygame.display.update()

main()
