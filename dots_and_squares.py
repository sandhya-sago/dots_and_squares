import sys
import pygame
import time
import itertools
import os

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
yellow = (240, 240,20)
dark_yellow = (240, 240,200)

class dots_and_squares_game():
    def __init__(self):
        self.screen = pygame.display.set_mode((800,800))
        self.screen.fill(white)
        self.grid_range = range(100,600,50)
        self.undo_button = (650,500,100,50)
        self.player_loc = (700,200)
        self.score_loc = (700, 350)
        self.total_num_segments = len(self.grid_range)*(len(self.grid_range)-1)*2
        self.undo_button_rect = ((self.undo_button[0],self.undo_button[1]),\
            (self.undo_button[0]+self.undo_button[2],\
            self.undo_button[0]+self.undo_button[3]))
        grid = [(x,y) for x in self.grid_range for y in self.grid_range]
        for x,y in grid:
            pygame.draw.circle(self.screen, darkBlue, (x,y), 3, 0)
        self.done = False
        list_of_players = ["A","B"]
        self.score = {p:0 for p in list_of_players}
        self.player_iter = itertools.cycle(list_of_players)
        self.player = next(self.player_iter)
        self.playing = True
        self.old_score = 0
        self.undo_count = 0 
        self.list_of_lines = []
        self.smallfont = pygame.font.Font("freesansbold.ttf",20)
        self.bigfont = pygame.font.Font("freesansbold.ttf",30)
        self.draw_player()
        self.draw_score()
        self.draw_undo_button(yellow)

    def status(self):
        return self.playing

    def quit(self):
        self.playing = False

    def click(self, pos):
        if self.locate(pos, self.undo_button_rect, False):
            self.process_undo()
        else:
            pointlist = self.get_end_points(pos)
            if pointlist:
                if pointlist in self.list_of_lines:
                    return None
                self.process_line(pointlist)
                if len(self.list_of_lines) == self.total_num_segments:
                    self.declare_winner()
        return None

    def process_undo(self):
        if self.undo_count:
            print("ERROR! Undo can be done only once!")
            return None
        try:
            old_line = self.list_of_lines.pop()
            self.undo_old_line(old_line)
            self.undo_count = 1
        except IndexError:
            return None
        if self.old_score:
            # We just added a score, undo it.
            # But the player remains the same
            self.score[self.player] -= self.old_score
            self.draw_score()
            #  TODO: cleanup the square
            self.check_square(old_line,True)
            self.old_score = 0
        else:
            self.player = next(self.player_iter)   
        self.draw_player()
        self.undo_count = 1
        return None
    
    def process_line(self, pointlist):
        pygame.draw.lines(self.screen, blue, True, pointlist, 2)
        self.list_of_lines.append(pointlist)
        self.old_score = self.check_square(pointlist)
        if self.old_score:
            self.score[self.player] += self.old_score
            self.draw_score()
        else:
            self.player = next(self.player_iter)
            self.draw_player()
        self.undo_count = 0

    def mouse(self, pos):
        if self.locate(pos, self.undo_button_rect, False):
            self.draw_undo_button(dark_yellow)
            pygame.display.update()
            time.sleep(1)
            self.draw_undo_button(yellow)
        return None

    def undo_old_line(self, old_line):
        pygame.draw.lines(self.screen, white, True, old_line, 2)
        for x,y in old_line:
            pygame.draw.circle(self.screen, darkBlue, (x,y), 3, 0)
        return None

    def locate(self, pos, pair,ingrid = True):
        ''' Is the pair of points within the grid? If yes,
        Is the point pos roughly between the pair of points
        (within 10 pixels on either side)'''
        if  self.grid_range[0] <= pair[0][0] <= self.grid_range[-1] and \
            self.grid_range[0] <= pair[0][1] <= self.grid_range[-1] and \
            self.grid_range[0] <= pair[1][0] <= self.grid_range[-1] and \
            self.grid_range[0] <= pair[1][1] <= self.grid_range[-1]:
            pass
        elif not ingrid:
            pass
        else:
            return False
        if pair[0][0]-10 < pos[0] < pair[1][0]+10 and \
            pair[0][1]-10 < pos[1] < pair[1][1]+10:
            return True
        else:
            return False

    def get_end_points(self, pos):
        '''Figure out the nearest 2 points for the line'''
        size = self.grid_range[1] - self.grid_range[0]
        snap_x, snap_y = pos[0]//size*size, pos[1]//size*size
        points = [(snap_x, snap_y), (snap_x, snap_y+size), \
            (snap_x+size, snap_y), (snap_x+size, snap_y+size)]
        for pair in [(points[0],points[1]), (points[0], points[2]), \
            (points[1],points[3]),(points[2], points[3])]:
            if self.locate(pos, pair,self.grid_range):
                return pair
        return None

    def draw_undo_button(self, color):
        pygame.draw.rect(self.screen, color ,self.undo_button)
        text = self.smallfont.render("Undo", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.center = ( self.undo_button[0]+self.undo_button[2]/2, \
                            self.undo_button[1]+self.undo_button[3]/2 )
        self.screen.blit(text, textpos)
        return None

    def draw_player(self):
        """Erase the current text at player_loc
        and put in the next player's name
        """
        remove_loc = [i-50 for i in self.player_loc] + [200,100]
        self.screen.fill(white, remove_loc)
        text = self.smallfont.render("Player: "+ self.player, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.center = self.player_loc
        self.screen.blit(text, textpos)
        return None

    def draw_score(self):
        """Erase the current text at player_loc
        and put in the next player's name
        """
        remove_loc = [i-50 for i in self.score_loc] + [200,100]
        text_loc = [(self.score_loc[0],self.score_loc[1]+i*20) for i in range(0,3)]
        self.screen.fill(white, remove_loc)
        lines = []
        lines.append("Scores")
        for p in self.score.keys(): 
            lines.append(p + " : " + str(self.score[p]))
        for i,line in enumerate(lines):
            text = self.smallfont.render(line, 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.center = text_loc[i]
            self.screen.blit(text, textpos)
        return None

    def mark_player (self,square, player=""):
        '''Label the square with the player who won it'''
        x = sum([i[0] for i in square])/4
        y = sum([i[1] for i in square])/4
        if player:
            text = self.smallfont.render(player[0], 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.center = [x,y]
            self.screen.blit(text, textpos)
        else:
            self.screen.fill(white, [x-10,y-10,25,25])
        return None

    def check_square(self, line, clear=False):
        x1, y1, x2, y2 = line[0][0],line[0][1],line[1][0], line[1][1] 
        v = y1-y2
        h = x1-x2
        if v:
            # verical line
            neighbors1= [(x1,y1),(x1-v,y1),(x2-v,y2),(x2,y2)]
            neighbors2 = [(x1,y1),(x1+v,y1),(x2+v,y2),(x2,y2)]
        else:
            #horizontal line
            neighbors1 = [(x1,y1),(x1,y1-h),(x2,y1-h),(x2,y2)]
            neighbors2 = [(x1,y1),(x1,y1+h),(x2,y1+h),(x2,y2)]
        # We know (x1,y1)(x2,y2) already has a line, so not checking
        # for it
        score = 0
        for n in [neighbors1,neighbors2]:
            for i in range(0,3):
                if (n[i],n[i+1]) in self.list_of_lines:
                    pass
                elif (n[i+1],n[i]) in self.list_of_lines:
                    pass
                else:
                    # one of the segments does not have a line, 
                    # so not a square
                    break
            else:
                if clear:
                    self.mark_player(n)
                else:
                    self.mark_player(n, self.player)
                    score += 1
        return score

    def declare_winner(self):
        '''Figure out the winner and declare'''
        winner = "Both"
        player = list(self.score.keys())
        if self.score[player[0]] > self.score[player[1]]:
            winner = player[0]
        elif self.score[player[1]] > self.score[player[0]]:
            winner = player[1]
        winner_loc = [300,300,200,100]
        self.screen.fill(white, winner_loc)
        text = self.bigfont.render("Winner: "+winner, 1, darkBlue)
        textpos = text.get_rect()
        textpos.center = (400,350)
        self.screen.blit(text, textpos)
        pygame.display.update()
        return None

def main():
    pygame.init()
    ds_game = dots_and_squares_game()
    while ds_game.status():
        for event in pygame.event.get():
            pygame.display.update()
            try:
                if event.type == pygame.QUIT:
                    ds_game.quit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    ds_game.click(pos)
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    ds_game.mouse(pos)
            except Exception as exp:
                raise(exp)
    return None

if __name__ == "__main__":
    main()
    print ("Good Game!!!")