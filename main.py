import pygame
import pyautogui
import random
import time

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["C", "D", "H", "S"]
back_colors = ["blue", "gray", "green", "purple", "red", "yellow"]

back_color = "purple"
size = pyautogui.size()
width = 800
height = 600
black = (0, 0, 0)
light_green = (144, 238, 144)
green = (5, 48, 5)
screen = pygame.display.set_mode((width, height))
space = 30
card_width = 75
card_height = 105
next_slot = space + card_width


class Card:
    def __init__(self, rank, value, suit, color, front, back, is_ace):
        self.rank = rank
        self.value = value
        self.suit = suit
        self.color = color
        self.front = front
        self.back = back
        self.is_ace = is_ace
        self.in_play = False
        self.face_up = False
        self.dragging = False
        self.x = 0
        self.y = 0
        self.width = 75
        self.height = 105

    def is_hovered(self, cursorX, cursorY):
        if self.x < cursorX < (self.x + self.width) and self.y < cursorY < (self.y + self.height):
            return True
        return False


def shuffle_deck():
    deck = []
    for suit in suits:
        for rank in ranks:
            if rank == "J":
                value = 11
            elif rank == "Q":
                value = 12
            elif rank == "K":
                value = 13
            elif rank == "A":
                value = 14
            else:
                value = int(rank)

            if suit == "C" or suit == "S":
                color = "black"
            else:
                color = "red"

            if rank == "A":
                is_ace = True
            else:
                is_ace = False

            card_front = pygame.image.load(f"Playing-cards/{rank}{suit}.png")
            card_front = pygame.transform.scale(card_front, (card_width, card_height))
            card_back = pygame.image.load(f"Playing-cards/{back_color}_back.png")
            card_back = pygame.transform.scale(card_back, (card_width, card_height))
            deck.append(Card(rank, value, suit, color, card_front, card_back, is_ace))
    random.shuffle(deck)
    return deck


def deal(deck, pile_top, cursorX, cursorY):
    x = 50
    layer = 0
    pile = []
    board = []
    for i, card in enumerate(deck):
        if layer < 7:
            card.in_play = True
            board.append(card)

        if card.dragging:
            card.x = cursorX - (card.x + cursorX)
            card.y = cursorY - (card.y + cursorY)
            screen.blit(card.front, (card.x, card.y, card_width, card_height))
        else:
            if layer == 0:
                card.x = x
                card.y = 150
                if i == 0:
                    card.face_up = True
                    screen.blit(card.front, (card.x, card.y, card_width, card_height))
                else:
                    screen.blit(card.back, (card.x, card.y, card_width, card_height))
                if i == 6:
                    x = 50 + next_slot
                    layer = 1
                    continue
                else:
                    x += next_slot

            if layer == 1:
                card.x = x
                card.y = 160
                if i == 7:
                    card.face_up = True
                    screen.blit(card.front, (card.x, card.y, card_width, card_height))
                else:
                    screen.blit(card.back, (card.x, card.y, card_width, card_height))
                if i == 12:
                    x = 50 + (next_slot * 2)
                    layer = 2
                    continue
                else:
                    x += next_slot

            if layer == 2:
                card.x = x
                card.y = 170
                if i == 13:
                    card.face_up = True
                    screen.blit(card.front, (card.x, card.y, card_width, card_height))
                else:
                    screen.blit(card.back, (card.x, card.y, card_width, card_height))
                if i == 17:
                    x = 50 + (next_slot * 3)
                    layer = 3
                    continue
                else:
                    x += next_slot

            if layer == 3:
                card.x = x
                card.y = 180
                if i == 18:
                    card.face_up = True
                    screen.blit(card.front, (card.x, card.y, card_width, card_height))
                else:
                    screen.blit(card.back, (card.x, card.y, card_width, card_height))
                if i == 21:
                    x = 50 + (next_slot * 4)
                    layer = 4
                    continue
                else:
                    x += next_slot

            if layer == 4:
                card.x = x
                card.y = 190
                if i == 22:
                    card.face_up = True
                    screen.blit(card.front, (card.x, card.y, card_width, card_height))
                else:
                    screen.blit(card.back, (card.x, card.y, card_width, card_height))
                if i == 24:
                    x = 50 + (next_slot * 5)
                    layer = 5
                    continue
                else:
                    x += next_slot

            if layer == 5:
                card.x = x
                card.y = 200
                if i == 25:
                    card.face_up = True
                    screen.blit(card.front, (card.x, card.y, card_width, card_height))
                else:
                    screen.blit(card.back, (card.x, card.y, card_width, card_height))
                if i == 26:
                    x = 50 + (next_slot * 6)
                    layer = 6
                    continue
                else:
                    x += next_slot

            if layer == 6:
                card.x = x
                card.y = 210
                card.face_up = True
                screen.blit(card.front, (x, 210, card_width, card_height))
                layer = 7

            if layer == 7:
                if len(pile) < pile_top:
                    card.in_play = False
                pile.append(card)

    return pile, board


class Slot:
    def __init__(self, n_cards, x, y):
        self.n_cards = n_cards
        self.x = x
        self. y = y
        self.width = 75
        self.height = 105


def build_board():
    x = 50
    pile_slot = None
    ace_slots = []
    board_slots = []
    for i in range(7):
        if i == 0:
            pile_slot = Slot(0, x, 20)
            pygame.draw.rect(screen, light_green, (x, 20, card_width, card_height), 1)
        if i >= 3:
            ace_slots.append(Slot(0, x, 20))
            pygame.draw.rect(screen, light_green, (x, 20, card_width, card_height), 1)
        board_slots.append(Slot(0, x, 150))
        pygame.draw.rect(screen, light_green, (x, 150, card_width, card_height), 1)
        x += next_slot
    return pile_slot, ace_slots, board_slots


def gameLoop():

    deck = shuffle_deck()
    pygame.display.set_caption("Solitaire")
    pygame.font.init()
    pygame.mixer.init()
    pygame.font.SysFont("comicsans", 50, bold=True)
    dealSound = pygame.mixer.Sound('deal.mp3')
    drawSound = pygame.mixer.Sound('draw.mp3')
    dealSound.play()
    icon = pygame.image.load('Playing-Cards/aces.png')
    icon = pygame.transform.scale(icon, (50, 32))
    pygame.display.set_icon(icon)
    pile_top = 24
    clock = pygame.time.Clock()
    mouse_pressed = False
    recent_click = False
    double_clicked = False
    dragging = False
    click_timer = 0
    hold_timer = 0
    run = True
    while run:
        clock.tick(27)
        screen.fill(green)
        cursorX, cursorY = pygame.mouse.get_pos()
        pile_slot, ace_slots, board_slots = build_board()
        pile, board = deal(deck, pile_top, cursorX, cursorY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                hold_timer = time.time()
                mouse_pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                for card in board:
                    card.dragging = False

                if not recent_click:
                    recent_click = True
                    click_timer = time.time()
                else:
                    if time.time() - click_timer < 0.5:
                        double_clicked = True
                mouse_pressed = False

        if mouse_pressed and time.time() - hold_timer > 0.5:
            for card in board:
                if card.is_hovered(cursorX, cursorY) and card.face_up:
                    already_dragging = False
                    for card in board:
                        if card.dragging:
                            already_dragging = True
                    if not already_dragging:
                        card.dragging = True
                        print(card.x)

        for card in pile:
            if pile_top > 0:
                card.x = 50
                card.y = 20
                screen.blit(card.back, (card.x, card.y, card_width, card_height))

        if mouse_pressed and 50 < cursorX < 125 and 20 < cursorY < 125:
            pile[pile_top].in_play = True
            if pile_top > 0:
                drawSound.play()
                pile_top -= 1
            mouse_pressed = False

        if double_clicked:
            for card in board:
                if card.is_hovered(cursorX, cursorY) and card.face_up:
                    print(card.is_ace)
                    recent_click = False
                    double_clicked = False

        for card in reversed(pile):
            if card.in_play:
                card.x = 155
                card.y = 20
                screen.blit(card.front, (155, 20, card_width, card_height))

        pygame.display.update()

    pygame.quit()


gameLoop()
