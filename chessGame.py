import pygame
import random
import copy
import os
import tkinter as tk
from tkinter import messagebox
from pygame.rect import Rect

HEIGHT = 750
WIDTH = 750
PARTITION = HEIGHT/8

pygame.font.init()
COORD_FONT = pygame.font.SysFont("comicsans", 35)
SUBSCRIPT_FONT = pygame.font.SysFont("comicsans", 18)

AN_left = [8, 7, 6, 5, 4, 3, 2, 1]
AN_bottom = ['a','b','c','d','e','f','g','h']
AN_system = {}

BLACK = (0,0,0)
WHITE = (255,255,255)
OTHERWHITE = (232,235,239)
GREY = (51,51,51)
BLUE = (125,130,150)
DFASJD = (58, 73, 102)
GREEN = (20,85,30,100)

GAMESTATE = []
moveHistory = []
PREVIOUS = None
TURN = 0

class Board:

    def __init__(self):
        self.showCoordinates = False
        self.showAxes = True
        self.initialize_partitions()
        self.initialize_tiles()
        self.initialize_pieces()
        self.Sound = pygame.mixer.Sound('move-noise.wav')


    def transform(self):
        self.BG = pygame.transform.scale(self.IMG, (WIDTH, HEIGHT))

    def initialize_partitions(self):
        cnt_x = 0
        cnt = 0
        for x in AN_bottom:
            cnt_x += 1
            cnt_y = 0
            for y in AN_left:
                cnt_y += 1
                notation = str(x) + str(y)
                x_min = (cnt_x - 1) * PARTITION
                x_max = x_min + PARTITION
                y_min = (cnt_y - 1) * PARTITION
                y_max = y_min + PARTITION
                cnt += 1
                d = {'x_min': x_min, 'x_max': x_max, 'y_min': y_min, 'y_max': y_max}
                AN_system[notation] = d


    # Draws coordinates on window of screen
    def draw_coordinates(self, win):
        for k, v in AN_system:
            id = k + v
            text = COORD_FONT.render(id, 1, GREY)
            x_avg = (AN_system[id]['x_min'] + AN_system[id]['x_max'])/2
            y_avg = (AN_system[id]['y_min'] + AN_system[id]['y_max'])/2
            win.blit(text,(x_avg - text.get_width()/2 ,y_avg - text.get_height()/2))

    # Draws coordinate axes on window of screen in bottom and right portion
    def draw_coordinate_axes(self, win):
        cnt = 0
        PAD = 2
        # Handles edge case in which the h1 file needs both the h and 1 drawn.
        for k, v in AN_system:
            if v == str(1) and k == 'h':
                text = COORD_FONT.render(str(v), 1, BLUE)
                x = AN_system[k+v]['x_max'] - text.get_width() - PAD
                y = AN_system[k+v]['y_min'] + PAD

                text1 = COORD_FONT.render(str(k), 1, BLUE)
                x1 = AN_system[k+v]['x_min'] + PAD
                y1 = AN_system[k+v]['y_max'] - text.get_height()
                win.blit(text, (x, y))
                win.blit(text1, (x1, y1))

            elif v == str(1):
                if cnt % 2 == 0:
                    text = COORD_FONT.render(str(k), 1, OTHERWHITE)
                else:
                    text = COORD_FONT.render(str(k), 1, BLUE)

                x = AN_system[k+v]['x_min'] + PAD
                y = AN_system[k+v]['y_max'] - text.get_height()
                win.blit(text, (x, y))
                cnt += 1

            elif k == 'h':
                if int(v) % 2 == 0:
                    text = COORD_FONT.render(str(v), 1, OTHERWHITE)
                else:
                    text = COORD_FONT.render(str(v), 1, BLUE)

                x = AN_system[k+v]['x_max'] - text.get_width() - PAD
                y = AN_system[k+v]['y_min'] + PAD
                win.blit(text, (x, y))

    # Creates all the tiles in the window
    def initialize_tiles(self):
        color = None
        indices = {'a': 1,'b': 2, 'c': 3, 'd': 4, 'e':5, 'f':6, 'g':7, 'h':8}
        for k,v in AN_system:
            x = indices[k]
            y = int(v)

            if (x + y) % 2 == 0:
                color = BLUE
            else:
                color = OTHERWHITE

            id = k + v
            tile = Tile(id, AN_system[id]['x_min'], AN_system[id]['y_min'], AN_system[id]['x_max'],
                             AN_system[id]['y_max'], color)

            GAMESTATE.append(tile)






    def initialize_pieces(self):
        white_queen = Queen("queen",'d1',"whitequeen.png", family='white')
        white_king = King("king",'e1',"whiteking.png",  family='white')
        white_bishop_left = Bishop("bishop", 'c1',"whitebishop.png", family='white')
        white_bishop_right = Bishop("bishop", 'f1', "whitebishop.png", family='white')
        white_knight_left = Knight("knight", 'b1', "whiteknight.png",   family='white')
        white_knight_right = Knight("knight", 'g1',"whiteknight.png",  family='white')
        white_rook_left = Rook("rook", 'a1', "whiterook.png",   family='white')
        white_rook_right = Rook("rook",'h1', "whiterook.png",  family='white')
        black_queen = Queen("queen", 'd8', "blackqueen.png",  family='black')
        black_king = King("king",'e8',"blackking.png", family='black')
        black_bishop_left = Bishop("bishop",'c8', "blackbishop.png", family='black')
        black_bishop_right = Bishop("bishop",'f8', "blackbishop.png", family='black')
        black_knight_left = Knight("knight",'b8', "blackknight.png",  family='black')
        black_knight_right = Knight("knight",'g8', "blackknight.png",  family='black')
        black_rook_left = Rook("rook",'a8', "blackrook.png",  family='black')
        black_rook_right = Rook("rook",'h8', "blackrook.png",  family='black')


        pawns = []

        for v in AN_bottom:
            white_cnt = 2
            black_cnt = 7
            white_id = str(v) + str(white_cnt)
            black_id = str(v) + str(black_cnt)
            white_pawn = Pawn('pawn', white_id,"whitepawn.png", family='white')
            black_pawn = Pawn('pawn', black_id, "blackpawn.png", family='black')

            pawns.append(white_pawn)
            pawns.append(black_pawn)

        PIECES = [
            white_queen, white_king, white_bishop_left, white_bishop_right,
            white_knight_left, white_knight_right, white_rook_left, white_rook_right,
            black_queen, black_king, black_bishop_left, black_bishop_right,
            black_knight_left, black_knight_right, black_rook_left, black_rook_right
            ]

        for item in pawns:
            PIECES.append(item)

        # associate pieces with tiles
        for piece in PIECES:
            for tile in GAMESTATE:
                if piece.pos == tile.id:
                    tile.occupied = True
                    tile.Piece = piece
    def playSound(self):
        self.Sound.play(loops=0,maxtime=0)

    def draw(self, win):
        for tile in GAMESTATE:
            tile.draw(win)


class Tile:
    def __init__(self, id, x_min, y_min, x_max, y_max, color):
        self.id = id
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.color = color
        self.occupied = False
        self.clicked = False
        self.Piece = None


    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x_min, self.y_min, PARTITION, PARTITION))
        if self.Piece is not None and self.occupied:
            win.blit(self.Piece.IMG, (self.x_min, self.y_min, PARTITION, PARTITION))




class Piece():
    def __init__(self, id, pos, imgName, family):
        self.id = id
        self.pos = pos
        self.family = family
        self.moved = False #For rooks, pawns, kings who have special first move capabilities
        self.RAW_IMG = pygame.image.load(os.path.join("chessImgs", imgName))
        self.IMG = self.convertIMG()
        self.attacked = []
        self.attacking = []
        self.potentialSquares = []
        self.xList = []
        self.yList = []
        self.captured = False
        self.MAP = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.REVMAP = { 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}

    def checkGamestate(self, values):
        alg = str(self.REVMAP[values[0]])
        notation = str(values[1])
        finalCoordinates = alg + notation
        for tile in GAMESTATE:
            if tile.id == finalCoordinates:
                if not tile.occupied:
                    return 'unoccupied'
                else:
                    return tile.Piece.family

    ''' Takes a tile id in tuple form and checks if the tile is occupied by a family or nonfamily
    if empty returns None
    '''
    def checkFamily(self, tileid):
        id = str(tileid[0]) + str(tileid[1])
        for tile in GAMESTATE:
            if tile.id == id:
                if tile.occupied:
                    return tile.Piece.family
                else:
                    return None



    def convertCoordinates(self):
        temp = copy.deepcopy(self.potentialSquares)
        self.clear()
        for coordinates in temp:
            alg = str(self.REVMAP[coordinates[0]])
            notation = str(coordinates[1])
            finalCoordinate = alg + notation
            self.potentialSquares.append(finalCoordinate)

    def convert(self, values):
        alg = str(self.REVMAP[values[0]])
        notation = str(values[1])
        finalCoordinate = alg + notation
        return finalCoordinate


    def convertIMG(self):
        return pygame.transform.scale(self.RAW_IMG, (int(PARTITION),int(PARTITION)))

    def checkBounds(self, values):
        x = values[0]
        y = values[1]
        if x < 1 or x > 8:
            return False
        if y < 1 or y > 8:
            return False
        else:
            return True

    def filterMoves(self, squares):
        # function to remap squares and only put in valid tiles
        # updates self.potentialSquares
        temporary = []
        for coordinates in squares:
            if coordinates[0] >= 1 and coordinates[0] <= 8:
                if coordinates[1] >= 1 and coordinates[1] <= 8:
                    if self.checkFamily(self.convert(coordinates)) != self.family:
                        temporary.append(coordinates)

        self.potentialSquares = temporary


    def clear(self):
        self.potentialSquares.clear()



class King(Piece):
    def __init__(self, id, pos, imgName, family):
        self.check = False
        super().__init__(id, pos, imgName, family)

    def checkMoves(self):
        x = int(self.MAP[self.pos[0]])
        y = int(self.pos[1])

        rawSquares = [[x-1, y+1], [x-1, y], [x-1, y-1], [x, y+1], [x, y-1], [x+1, y+1], [x+1, y], [x+1, y-1]]
        if self.family == 'white':
            if not self.moved or not self.check:
                pass
        else:
            pass
        self.filterMoves(rawSquares) # updates potential move list
        self.convertCoordinates()



class Knight(Piece):
    def __init__(self, id, pos, imgName, family):
        super().__init__(id, pos, imgName, family)

    def checkMoves(self):
        x = int(self.MAP[self.pos[0]])
        y = int(self.pos[1])

        squares = [(x-1, y+2), (x+1, y+2), (x+2, y+1), (x+2, y-1),(x+1, y-2), (x-1, y-2), (x-2, y-1), (x-2, y+1)]

        self.filterMoves(squares)
        self.convertCoordinates()



class Rook(Piece):
    def __init__(self, id, pos, imgName, family):
        super().__init__(id, pos, imgName, family)

    def checkMoves(self):
        x = int(self.MAP[self.pos[0]])
        y = int(self.pos[1])

        for cnt in range(1,8):
            values = (x, y + cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1,8):
            values = (x, y - cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x + cnt, y)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x-cnt, y)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        print(self.potentialSquares)

class Queen(Piece):
    def __init__(self, id, pos, imgName, family):
        super().__init__(id, pos, imgName, family)

    def checkMoves(self):
        x = int(self.MAP[self.pos[0]])
        y = int(self.pos[1])

        for cnt in range(1,8):
            values = (x, y + cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1,8):
            values = (x, y - cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x + cnt, y)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x-cnt, y)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x + cnt, y + cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x - cnt, y - cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x + cnt, y - cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x - cnt, y + cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break


class Bishop(Piece):
    def __init__(self, id, pos, imgName, family):
        super().__init__(id, pos, imgName, family)

    def checkMoves(self):
        x = int(self.MAP[self.pos[0]])
        y = int(self.pos[1])

        for cnt in range(1, 8):
            values = (x + cnt, y + cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x - cnt, y - cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x + cnt, y - cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        for cnt in range(1, 8):
            values = (x - cnt, y + cnt)
            if self.checkBounds(values):
                ret = self.checkGamestate(values)
                if ret == 'unoccupied':
                    self.potentialSquares.append(self.convert(values))
                elif ret != self.family:
                    self.potentialSquares.append(self.convert(values))
                    break
                elif ret == self.family:
                    break
            else:
                break

        print(self.potentialSquares)


class Pawn(Piece):
    def __init__(self, id, pos, imgName, family):
        super().__init__(id, pos, imgName, family)

    def checkMoves(self):
        # Only piece who's logic changes based on family
        # two different sets of logic, one set advances up board, other set down board.
        x = int(self.MAP[self.pos[0]])
        y = int(self.pos[1])
        squares = []
        if self.family == 'white':
            f1 = self.checkFamily(self.convert((x, y + 1)))

            if f1 is None:
                squares.append((x, y + 1))
            if not self.moved:
                f2 = self.checkFamily(self.convert((x, y + 2)))
                if f2 is None:
                    squares.append((x, y + 2))

            if self.checkBounds((x - 1,  y + 1)):
                l1 = self.checkFamily(self.convert((x - 1, y + 1)))
                if l1 == 'black':
                    squares.append((x - 1, y + 1))

            if self.checkBounds((x + 1, y + 1)):
                r1 = self.checkFamily(self.convert((x + 1, y + 1)))
                if r1 == 'black':
                    squares.append((x + 1, y + 1))


        if self.family == 'black':
            f1 = self.checkFamily(self.convert((x, y - 1)))
            if f1 is None:
                squares.append((x, y - 1))
            if not self.moved:
                f2 = self.checkFamily(self.convert((x, y - 2)))
                if f2 is None:
                    squares.append((x, y - 2))

            if self.checkBounds((x - 1, y - 1)):
                l1 = self.checkFamily(self.convert((x - 1, y - 1)))
                if l1 == 'white':
                    squares.append((x - 1, y - 1))

            if self.checkBounds((x + 1, y - 1)):
                r1 = self.checkFamily(self.convert((x + 1, y - 1)))
                if r1 == 'white':
                    squares.append((x + 1, y - 1))


        self.filterMoves(squares)
        self.convertCoordinates()

def updateTile(x, y, board):
    global PREVIOUS, TURN

    if TURN % 2 == 0:
        turn = 'white'
    else:
        turn = 'black'

    for tile in GAMESTATE:
        if (x >= tile.x_min) and (x < tile.x_max):
            if (y >= tile.y_min) and (y < tile.y_max):
                # click on tile and nothing has been clicked on before, set tile
                if tile.occupied and PREVIOUS is None and tile.Piece.family == turn:
                    PREVIOUS = tile
                    tile.Piece.checkMoves()

                # click on tile and previous click does exist
                elif PREVIOUS is not None:
                    if tile.occupied:
                        if tile.Piece.family == PREVIOUS.Piece.family:
                            PREVIOUS = tile
                            tile.Piece.checkMoves()
                        else:
                            if tile.id in PREVIOUS.Piece.potentialSquares:
                                move(PREVIOUS.id, tile.id)
                                board.playSound()
                    else:
                        if tile.id in PREVIOUS.Piece.potentialSquares:
                            moveHistory.append([PREVIOUS.id, tile.id])
                            move(PREVIOUS.id, tile.id)
                            board.playSound()




def printGAMESTATE():
    for tile in GAMESTATE:
        print('{} {} {}'.format(tile.id, tile.Piece, tile.occupied))


# only call after the move has checked out and is valid
def move(src, dest):
    global PREVIOUS, TURN
    src = getTile(src)
    dest = getTile(dest)
    src.Piece.pos = dest.id
    dest.Piece = src.Piece
    dest.Piece.moved = True
    dest.Piece.potentialSquares.clear()
    src.Piece = None
    src.occupied = False
    dest.occupied = True

    PREVIOUS = None
    TURN += 1



def getTile(id):
    for tile in GAMESTATE:
        if tile.id == id:
            return tile

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()

    msg = 'I predict your number to be ' + str(content)
    messagebox.showinfo(subject, msg)
    try:
        root.destroy()
    except:
        pass

def draw_window(window, base):
    base.draw(window)

    if PREVIOUS is not None:
        rect = Rect(PREVIOUS.x_min, PREVIOUS.y_min, PARTITION - 1, PARTITION -1)
        pygame.draw.rect(window, (0, 0, 190), rect, 4)
        if PREVIOUS.Piece.potentialSquares is not None:
            for tile in PREVIOUS.Piece.potentialSquares:
                id = getTile(tile)
                pygame.draw.circle(window, DFASJD , (int(id.x_min + PARTITION/2), int(id.y_min + PARTITION/2)), int(PARTITION/6))


    if base.showCoordinates:
        base.draw_coordinates(window)

    if base.showAxes:
        base.draw_coordinate_axes(window)

def main():
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode((WIDTH,HEIGHT))

    run = True
    base = Board()

    while run:

        pygame.mouse.set_visible(True)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False

            if events.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                # Main function that checks tiles and etc.
                updateTile(x,y, base)

            # Code that displays coordinate system on grid
            if events.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_s]:
                    if base.showCoordinates:
                        base.showCoordinates = False
                        print('Removing Coordinates')
                    else:
                        base.showCoordinates = True
                        print('Showing Coordinates')

                if pressed[pygame.K_a]:
                    if base.showAxes:
                        base.showAxes = False
                        print('Removing Axes')
                    else:
                        base.showAxes = True
                        print('Showing Axes')

                if pressed[pygame.K_c]:
                    pass

                if pressed[pygame.K_LEFT]:
                    if len(moveHistory) != 0:
                        lastmove = moveHistory.pop()
                        move(lastmove[1], lastmove[0])



        draw_window(window, base)
        pygame.display.update()


    pygame.quit()
    quit()

main()







