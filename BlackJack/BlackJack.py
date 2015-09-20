# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
player_score = 0
dealer_score = 0
deck = ""
player_hands = ""
dealer_hands = ""
status = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        ##pass	# create Hand object
        self.card_list = []

    def __str__(self):
        #pass	# return a string representation of a hand
        str_rep = "#Hand contains "
        for item in self.card_list:
            str_rep += str(item) + " "
            
        return str_rep

    def add_card(self, card):
        #pass	# add a card object to a hand
        self.card_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        #pass	# compute the value of the hand, see Blackjack video
        handValue = 0
        haveAces = False
        for card in self.card_list:
            handValue += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                haveAces = True
        
        if haveAces == False:
            return handValue
        else:
            if handValue + 10 <= 21:
                return handValue + 10
            else:
                return handValue
        
    def draw(self, canvas, pos):
        #pass	# draw a hand on the canvas, use the draw method for cards
        counter = -1
        for card in self.card_list:
            counter += 1
            card.draw(canvas , [pos[0] + counter * (CARD_SIZE[0] + 10) , pos[1]])
 
        
# define deck class 
class Deck:
    def __init__(self):
        #pass	# create a Deck object
        self.index = 52
        self.list_of_cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.list_of_cards.append(Card(suit, rank))
        

    def shuffle(self):
        # shuffle the deck 
        #pass    # use random.shuffle()
        random.shuffle(self.list_of_cards)

    def deal_card(self):
        #pass	# deal a card object from the deck
        self.index -= 1
        return self.list_of_cards[self.index]
    
    def __str__(self):
        #pass	# return a string representing the deck
        str_rep = "#Deck contains "
        for card in self.list_of_cards:
            str_rep += str(card) + " "
        
        return str_rep



#define event handlers for buttons
def deal():
    global outcome, in_play, player_hands, dealer_hands, deck, status, dealer_score
    
    # your code goes here
    if in_play:
        dealer_score += 1
    
    status = ""
    deck = Deck()
    deck.shuffle()
    player_hands = Hand()
    player_hands.add_card(deck.deal_card())
    player_hands.add_card(deck.deal_card())
    #print "Player ",player_hands
    
    dealer_hands = Hand()
    dealer_hands.add_card(deck.deal_card())
    dealer_hands.add_card(deck.deal_card())
    #print "Dealer ",dealer_hands
    
    outcome = "Hit or stand?"
    in_play = True

def hit():
    #pass	# replace with your code below
    global player_hands , outcome, in_play, status, dealer_score
    # if the hand is in play, hit the player
    if player_hands.get_value() <= 21:
        player_hands.add_card(deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score
    if player_hands.get_value() > 21:
        #print "you have busted"
        status = "you went bust and lose."
        dealer_score += 1
        outcome = "New deal?"
        in_play = False
        
def stand():
    pass	# replace with your code below
    global player_hands, dealer_hands, in_play, status, dealer_score , player_score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    in_play = False
    outcome = "New deal?"
    
    if player_hands.get_value() > 21:
        #print "you have busted"
        status = "You went bust and lose."
        dealer_score += 1
    else:
        while dealer_hands.get_value() < 17:
            dealer_hands.add_card(deck.deal_card())
    
    if dealer_hands.get_value() > 21:
        #print "dealer busted"
        status = "Dealer went bust and you win."
        player_score += 1
    elif player_hands.get_value() > dealer_hands.get_value():
        #print "Player wins"
        status = "You win."
        player_score += 1
    else:
        #print "Dealer wins"
        status = "You lose."
        dealer_score += 1
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global in_play, score, status
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    global dealer_hands, player_hands
    
    canvas.draw_text("Blackjack" , [120 , 80] , 50 , "Black")
    canvas.draw_text("Scores" , [500 , 25] , 30 , "Black")
    canvas.draw_text("Dealer: "+str(dealer_score) , [500 , 50] , 20 , "Black")
    canvas.draw_text("You: "+str(player_score) , [500 , 70] , 20 , "Black")
    
    canvas.draw_text(status , [210 , 120] , 20 , "White")
    
    canvas.draw_text("Dealer" , [100 , 170] , 20 , "Black")
    dealer_hands.draw(canvas , [100, 200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    
    canvas.draw_text("Player" , [100 , 370] , 20 , "Black")
    canvas.draw_text(outcome , [200 , 370] , 20 , "Black")
    player_hands.draw(canvas , [100, 400])
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
