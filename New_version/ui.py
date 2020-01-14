# import numpy as np
import sys
import pygame as pg


class Reversi(object):

    def __init__(self, board_length=700, board_width=540, grid_size=60,
                 square_no=8, first_execu_color='Black'):
        self.length = board_length
        self.width = board_width
        self.square_no = square_no
        self.grid_size = grid_size

        self.excu = -1 if first_execu_color == 'Black' else 1
        self.name = {1: 'White', -1: 'Black'}

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.orange = (255, 128, 0)
        self.grey = (192, 192, 192)
        self.red = (255, 0, 0)
        self.background = (51, 153, 255)
        self.checker = (21, 114, 21)

    def play_game(self):

        self.initialize_interface()
        mode = self.mode_choice()

        if mode == 'PVP':
            self.PVP()
        else:
            self.PVE()

    def initialize_interface(self):
        pg.init()
        self.screen = pg.display.set_mode((self.length, self.width))
        pg.display.set_caption("Reversi")

    def display_mode_choices(self, rec1, rec2, choice1, choice2):
        '''
        rec1 and rec2: 4-element tuples, representing the position and size of
                       the rectangular buttons to choose mode
        choice1 and choice2: String, printed in rectangular choice buttons
        '''
        self.screen.fill(self.background)

        font = pg.font.Font(None, 60)

        pg.draw.rect(self.screen, self.white, rec1)
        pg.draw.rect(self.screen, self.black, rec1, 2)
        mode1 = font.render(choice1, True, self.black)
        self.screen.blit(mode1, (145, 255))

        pg.draw.rect(self.screen, self.white, rec2)
        pg.draw.rect(self.screen, self.black, rec2, 2)
        mode2 = font.render(choice2, True, self.black)
        self.screen.blit(mode2, (470, 255))

        pg.display.update()

    def mode_choice(self):
        '''
        get mouse click position, check chosen mode, return mode type
        '''
        PVE_rec = (100, 210, 175, 125)
        PVP_rec = (425, 210, 175, 125)

        self.display_mode_choices(PVE_rec, PVP_rec)

        event_happened = False
        while not event_happened:
            event = pg.event.wait()
            self.exit_check(event)

            if event.type == pg.MOUSEBUTTONDOWN:

                click_col, click_row = event.pos

                if PVE_rec[0] < click_col < PVE_rec[0]+PVE_rec[2] and PVE_rec[1] < click_row < PVE_rec[1]+PVE_rec[4]:
                    return 'PVE'
                elif PVP_rec[0] < click_col < PVP_rec[0]+PVP_rec[2] and PVP_rec[1] < click_row < PVP_rec[1]+PVP_rec[4]:
                    return 'PVP'

    def exit_check(self, event):
        '''
        End the game if the EXIT instruction is made
        !!! NEED assertion to check event type
        '''
        if event.type == pg.QUIT:
            sys.exit()

    def draw_board(self):
        pass

    def PVP(self):
        pass

    def PVE(self):
        color = self.select_checker_color()
        self.draw_board()

        human_first = True if color == 'Black' else False

        avail_space = self.square_no ** 2
        while avail_space:
            if human_first:
                click_pos = self.human_click()
            else:
                matx_pos = self.computer_player()
                click_pos = self.matx_p_2_board_p(matx_pos)
            # How about when the clicked pos is not an available space (either
            # occupied or cannot reverse others)
            self.put_check(click_pos)
            self.reverse_checker(click_pos)
            human_first = not human_first
            avail_space -= 1
        pass

    def test(self):
        a = True
        a = a
        print(a)


if __name__ == '__main__':
    main = Reversi()
    main.test()
