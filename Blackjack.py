import random

# Global variables
suits = suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}
playing = True
# Classes
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_composition = " "
        for card in self.deck:
            deck_composition += "\n" + card.__str__()
        return "The deck has: " + deck_composition

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


# test_deck = Deck()
# print(test_deck)
# test_deck.shuffle()
# print(test_deck)
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # Aces can be 1 or 11 in Blackjack

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# test_deck = Deck()
# test_deck.shuffle()
# test_player = Hand()
# pulled_card = test_deck.deal()
# print(pulled_card)
# test_player.add_card(pulled_card)
# print(test_player.value)
class Chips:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(
                input("You have 100 chips. How many chips would you like to bet? ")
            )
        except:
            print("Sorry, please provide an integer")
        else:
            if chips.bet > chips.total:
                print(
                    "Sorry, you do not have enough chips! You have {}".format(
                        chips.total
                    )
                )
            else:
                break


def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input("Hit or Stand? 'h' or 's' ")
        if x[0].lower() == "h":
            hit(deck, hand)
        elif x[0].lower() == "s":
            print("Player Stands, Dealer's Turn")
            playing = False
        else:
            print("Sorry, please try again")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand: ")
    print("(First card hidden)")
    print(dealer.cards[1])
    print("\nPlayer's Hand:")
    for card in player.cards:
        print(card)


def show_all(player, dealer):
    print("\nDealer's Hand: ")
    for card in dealer.cards:
        print(card)
    print(f"Value of Dealer's Hand is: {dealer.value}")
    print("\nPlayer's Hand:")
    for card in player.cards:
        print(card)
    print(f"Value of Player's Hand is: {player.value}")


# End game scenarios
def player_busts(player, dealer, chips):
    print("     Player busts!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("     Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("     Player wins! Dealer busts!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("     Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    print("     Dealer and player tie, push!")


while True:
    print("Welcome to Blackjack")
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    player_chips = Chips()
    take_bet(player_chips)
    show_some(player_hand, dealer_hand)
    while playing:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    if player_hand.value <= 21:
        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    print("\nPlayer total chips are at: {}".format(player_chips.total))
    new_game = input("Would you like to play another hand? 'y' or 'n' ")
    if new_game[0].lower() == "y":
        playing = True
        continue
    else:
        print("Thanks for playing")
