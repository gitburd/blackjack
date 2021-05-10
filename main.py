import numpy as np
from random import shuffle
import emoji

class Player:
    def __init__(self, Hand=np.array([]), Money=1000):
        self.Hand = Hand
        self.Score = self.set_score()
        self.Money = Money
        self.Bet = 0
 
    def __str__(self):
        currentHand = ""
        for card in self.Hand:
            currentHand += f"{card['Value']}{card['Suit']} "
        currentHand += f"\nScore: {self.Score}"

        return(emoji.emojize(f"{currentHand}"))

    def print_money(self):
        return(f"${self.Money}")
    
    def print_house_info(self):
        return(f"Score: {self.Score}")

    def set_score(self):
        score = 0
        cardValues = {            
            "A" : 11, "K" : 10, "Q" : 10, "J" : 10, 
            "10":10, "9":9, "8":8, "7":7, "6":6, 
            "5":5, "4":4, "3":3, "2":2
        }
        
        aces = 0
        for card in self.Hand:
            score += cardValues[str(card['Value'])]
            # aces can be 1 or 11
            if card['Value'] == "A":
                aces += 1
            if score > 21 and aces != 0:
                score -=10
                aces -= 1
        self.Score = score
        return score

    def hit(self, card):
        self.Hand = np.append(self.Hand, card)
        self.score = self.set_score()
    
    # this should be called draw
    def play(self, new_hand):
        self.Hand = new_hand
        self.score = self.set_score()
    
    def bet_money(self,money):
        self.Money -= money
        self.Bet += money

    def win(self, result):
        if result:
            if self.Score == 21 and len(self.Hand == 2):
                self.Money += int(self.Bet * 2.5)
            else:
                self.Money += self.Bet * 2

        self.Bet = 0
    
    def draw(self):
        self.Money += self.Bet
        self.bet = 0

    def has_black_jack(self):
        if self.Score == 21 and len(self.Hand == 2):
            return True
        else:
            return False

def create_deck():
    Deck = np.array([])
    for card in range(2,11): # add 2-10
        heart={"Value":card, "Suit": ":heart_suit:"}
        spade={"Value":card, "Suit": ":spade_suit:"}
        club={"Value":card, "Suit": ":club_suit:"}
        dimond={"Value":card, "Suit": ":diamond_suit:"}
        Deck = np.append(Deck, [heart,spade,club,dimond])
    
    faceValues = ["J", "Q", "K", "A"]
    for card in faceValues: # add face values
        heart={"Value":str(card), "Suit":":heart_suit:"}
        spade={"Value":str(card), "Suit":":spade_suit:"}
        club={"Value":str(card), "Suit":":club_suit:"}
        dimond={"Value":str(card), "Suit":":diamond_suit:"}
        Deck = np.append(Deck, [heart,spade,club,dimond])
    shuffle(Deck)
    return Deck

def get_hand():
    global Deck
    hand = np.array([])
    for i in range (2):
        card = Deck[0]
        hand = np.append(hand,card)
        Deck = np.delete(Deck,0)
    return hand

def draw_card():
    global Deck
    card = Deck[0]
    Deck = np.delete(Deck,0)
    return card

def print_house(House):
    for i in range(len(House.Hand)):
        if i == 0:
            print("\nHouse: X", end = " ")
        elif i == len(House.Hand) - 1:
            print(emoji.emojize(f"{House.Hand[i]['Value']}{House.Hand[i]['Suit']}"))
        else:
            print(emoji.emojize(f"{House.Hand[i]['Value']}{House.Hand[i]['Suit']}", end=" "))

Deck = create_deck()
Human_Player = Player()
House = Player()
while Human_Player.Money > 0:
    if len(Deck) < 20:
        print("Shuffling...")
        Deck = create_deck()

    Human_Player.Hand = get_hand()
    Human_Player.set_score()
    House.Hand = get_hand()
    House.set_score()

    while True:
        try:
            Bet = int(input(f"You have {Human_Player.print_money()}\nHow much would you like to bet?: "))
            if Bet <= 0:
                raise Exception("Bet more than $0")
            if Bet <= Human_Player.Money:
                break
            raise Exception(f"You don't have that much money.")
        except ValueError:
            print("Enter a whole number.")
        except Exception as error:
            print(error)

    Human_Player.bet_money(Bet)

    print('\nYou: ', Human_Player)
    print_house(House)

    if Human_Player.has_black_jack():
        if House.has_black_jack():
            Human_Player.draw()
            print("\nPUSH")
        else:
            Human_Player.win(True)
            print("\nBLACKJACK!")
            print("YOU WIN")
    elif House.has_black_jack():
        print("\nBLACKJACK!")
        print("HOUSE WINS")
    else:
        while (Human_Player.Score < 21):
            action = input("\nHit or stay?(h/s): ")
            try:
                if action.lower() == "h":
                    Human_Player.hit(draw_card())
                    print("\nYou: ", Human_Player)
                    print(Human_Player.print_money())
                elif action.lower() == "s":
                    break
                else:
                    print('Enter "h" to HIT or "s" to STAY.')
            except Exception as e:
                print('Enter "h" to HIT or "s" to STAY.')
        while(House.Score < 16):
            House.hit(draw_card())
            print("\nHouse:", House)
        if len(House.Hand) == 2:    
            print("\nHouse:", House)

        if Human_Player.Score > 21:
            if House.Score > 21:
                print("\nPUSH\n")
                Human_Player.draw()
            else:
                print("\nBUST")
                print("HOUSE WINS\n")
                Human_Player.win(False)
        elif Human_Player.Score > House.Score:
            print("\nYOU WIN\n")
            Human_Player.win(True)
        elif Human_Player.Score == House.Score:
            print("\nPUSH\n")
            Human_Player.draw()
        else:
            if House.Score > 21:
                print("\nHOUSE BUSTS")
                print("YOU WIN\n")
                Human_Player.win(True)    
            else:
                print("\nHOUSE WINS\n")
                Human_Player.win(False)
print("You are out of money.\nGOODBYE.")
