#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 23:44:32 2019

"""

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11}
playing = True #False when player decided to leave the game


###############################################################################
class Card:
    '''
    each Card has suit and rank
    '''
    
    def __init__(self,suit,rank):
        self.suit= suit  #which suit is this card
        self.rank = rank #which rank(str) is this card
 
    def __str__(self):
        return self.rank + ' of ' + self.suit  
    
    
class Deck:
    '''
    a list of all cards in a deck (card(suit,rank))
    
    '''
    
    def __init__(self):
        self.deck = []  # a deck of card is a list of cards(suit,rank)
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                 
    def __str__(self):
        deck_comp = ''  
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp                

    def shuffle(self):
        '''
        shuffle all cards in deck(list)
        '''
        random.shuffle(self.deck)
        
    def deal(self):
        '''
        pop a card from Deck.deck
        '''
        return self.deck.pop()
   
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.cardstr = '' #for __str__ method.
        
    
    def add_card(self,card):
        self.cards.append(card) #card is a string
        self.value += values[card.rank] #check up dictionary 
        #card.rank act as key of dict values
        #values is a dict, card.rank is a str that is called as a dict key
        #print('\n')
        #print('player\'s hand: ')
        #for i in self.cards:
        #    print(i)
        if card.rank == 'Ace': #count no of ace cards
            self.aces += 1
        print('hands total value: ', self.value)
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces>0: 
            self.value -= 10 
            self.aces -=1
            print ('ace adjusted') #reporter print 
            print('total value (after adjustment: ',self.value)
    
    
            
class Chips:
    '''
    keep track of the money of player
    '''
    def __init__(self):
        self.total = 100   
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet*2
        
    def lost_bet(self):
        self.total -= self.bet

###############################################################################

def take_bet(Chips):
    #chips are chips of the player
    '''
    ask for the user for an integer
    use try/except for input type control
    rmb to check that a player's bet can be covered by their available chips
    '''  
    while True:
        #type control
        try:
            Chips.bet = int(float(input('how much would you like to bet?')))
        except ValueError: #user input non-numeral character 
            print('please input a number')
            continue
        else: #no exception is thrown
            if Chips.bet > Chips.total:
                print('mate you are broken. place a smaller bet la')
                continue
            else:
                break
            
def hit(deck_,hand_):
    '''
    either player can take hits until they bust
    this func will be called anytime a player requests a hit, 
    or dealer<17
    
    take in attri deck and hand.value
    
    '''
    
    hand_.add_card(deck_.deal())#add value to hand from deck list i.e. card is removed from deck 
    print('card added')
    print('total value (before adjustment: ',hand_.value)

    
def hit_or_stand(deck_,hand_):
    '''
    accept the deck and player's hand
    assign playing as global bool
    if player hits, employ hit()
    if player stands, set playing as False to control while loop
    '''
    
    global playerhit 
    playerhit  = True
  
    while playerhit:
        h_or_s = input ('press h to hit, press s to stand: ')
        if h_or_s.lower() == 's':
            print('you have chosen to stand. Dealer\'s turn.')
            playerhit = False
            break
        elif h_or_s.lower() == 'h':
            hit(deck_,hand_)  #calls add_card method 
            hand_.adjust_for_ace()
            if hand_.value >= 21:
                playerhit = False
                break
        elif h_or_s.lower() == 'e': #cheatcode for testing
            break
        else:
            print('please enter either h or s')
            continue
    
    
def show_some(player,dealer):
    '''
    when the games starts
    and after each time player takes a card 
    dealer's first card is hidden and all player's card are visible
    '''
    print ('player hands:')
    print (player.cards[0],' & ', player.cards[1])
    print('\n')
    print ('dealer hands:')
    print (' **hidden** & ', dealer.cards[1] )

            
def show_all(player,dealer):   
    '''
    at the end of the hand: all cards are shown
    also show each hand's total value
    '''         
    #if playing == False:
    print ('player\'s hand:')
    for i in player.cards:
        print (i)
    print ('player\'s score: ', player.value )
    print('dealer\'s hand: ')
    for i in dealer.cards:
        print(i)
    print ('dealer\'s score: ', dealer.value)
            
def player_bust(player,dealer,chips):
    print('player bust')
    chips.lost_bet()
    print ('player now hv ', player.value)

def dealer_bust(player,dealer, chips):
    print('dealer bust')
    chips.win_bet()
    
def player_wins(player,dealer, chips):
    print('player wins')
    chips.win_bet()
    print('player now hv ', player.value)
    
def dealer_wins(player, dealer, chips): 
    print('dealer wins')
    chips.lost_bet()
    
def tie(player,dealer,chips):
    print('tie! no one wins')
    
###############################################################################

secondplay = False 
player = True
global secondplay_bankroll
secondplay_bankroll = 0

while playing:
    
    player = Hand()
    dealer = Hand()
    endgame = False #this rd is finished, but as long as playing is True the player can continue to bet in another round
    #intialization of the deck
    realdeck = Deck() #create an instance of a deck
    #print(realdeck)
    realdeck.shuffle() #shuffle all cards in the deck
    #print(realdeck)
    
    
    #player bet (first play)
    if secondplay  == False: 
        playerchip = Chips() #playerchips stores total money and bet of player
        while True: 
            try:
                playerchip.total = int(float(input ('how much money do you have?')))
            except ValueError:
                print('please only enter numeric value')
            else:
                break
        print ('you have ',playerchip.total, ' dollars.')    
        take_bet(playerchip)
        print('your current bet is ', playerchip.bet, ' dollars.')
    
    #player bet (add money to bank roll?)
    if secondplay == True:
        playerchip = Chips()
        playerchip.total = secondplay_bankroll #overwrite chip class instance initialisation
        print ('the amount of money left from last game: ', playerchip.total, ' dollars')
        while True:
            try:
                playerchip.total += int(float(input('how much money do you wanna add to the bankroll?')))
            except:
                print('please only enter numeric value')
            else:
                break
        print('new bankroll is ', playerchip.total,' dollars')
        take_bet(playerchip)
        print('your current bet is ', playerchip.bet, ' dollars')
        
    
    
    player.add_card(realdeck.deal())
    player.add_card(realdeck.deal())
    dealer.add_card(realdeck.deal())
    dealer.add_card(realdeck.deal())
    print('\n')
    print('---*--- HANDS ---*---')
    show_some(player, dealer)
    
    
    
    #player hit loop
    print('\n')
    print ('---*--- PLAYER\'S TURN ---*---')
    hit_or_stand(realdeck, player)
    if player.value > 21: 
        player_bust (player, dealer, playerchip)
        endgame = True 
    elif player.value == 21:
        player_wins (player, dealer, playerchip)
        endgame = True 
    print (' ')
    
    
    
    while playerhit == False and endgame == False: 
        print('\n')
        print ('---*--- DEALER\'S TURN ---*---')
        print ('\n')
        while dealer.value < 17:
            hit(realdeck, dealer)
        if dealer.value >= 21:
            dealer_bust(player, dealer, playerchip)
            endgame = True 
        else: #dealer 17 <= value < 21 
            if player.value > dealer.value:
                player_wins(player, dealer, playerchip) 
                endgame = True
            elif player.value == dealer.value:
                dealer_wins(player, dealer, playerchip)
                endgame = True
            else: 
                tie(player, dealer, playerchip)
                endgame = True
        print ('dealer\'s total value = ' ,dealer.value )
            
    if endgame == True:
        contin = ''
        while True:
            print('player now have: ', playerchip.total, ' dollars')
            contin = input ('press c to continue, press e to exit').lower()
            if contin == 'c':
                secondplay = True
                secondplay_bankroll = playerchip.total #stored to avoid initialisation of bankroll 
                #set secondplay_bankroll to global to override instance intitalisation
                break
            elif contin =='e':
                print('you have chosen to quit the game')
                playing = False
                break   
    
    #show_all(player,dealer)

    if contin == 'c':
        continue 
    elif contin == 'e':
        break
    
###############################################################################            
            

#test_deck = Deck()
#print(test_deck)

