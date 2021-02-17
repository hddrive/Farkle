import random
import time
from collections import deque

PLAYABLE_DICE = [[1], 100, [5], 50,
                 [2, 2, 2], 200, [3, 3, 3], 300, [4, 4, 4], 400, [5, 5, 5], 500, [6, 6, 6], 600, [1, 1, 1], 1100,
                 [2, 2, 2, 2], 300, [3, 3, 3, 3], 400, [4, 4, 4, 4], 500, [5, 5, 5, 5], 600, [6, 6, 6, 6], 700,
                 [1, 1, 1, 1], 1200, [2, 2, 2, 2, 2], 400, [3, 3, 3, 3, 3], 500, [4, 4, 4, 4, 4], 600,
                 [5, 5, 5, 5, 5], 700, [6, 6, 6, 6, 6], 800, [1, 1, 1, 1, 1], 1300,
                 [1, 2, 3, 4, 5, 6], 1500
                 ]
OPPONENTS = ["Bill", "Ted", "Greg", "James", "Carl", "Tim", "Kyle", "Doug", "Peter", "Al", "Eddy"]
DIFFICULTY = {"easy": [1, 2, 3], "medium": [1, 2, 3, 4, 5, 6], "hard": [1, 2, 3, 4, 5, 6, 7, 8, 9]}

MIN_SCORE = 450
WINNING_SCORE = 10000

ROLL_DICE = "roll dice"
UPDATE_SCORE = "update score"
CURRENT_SCORE = "current score"
FARKLED = "farkled"
WINNER = "winner"
SUDDEN_DEATH = "sudden death"
CURRENT_ROLLER = "current roller"
COMP_KEEP_ROLLING = "comp_keep_rolling"
IF_OVER_WINNING_SCORE = "if over winning score"
IS_ON_BOARD = "is on board"

def display_rules():
    """Displays the rules"""
    rules_file = open("FarkleRules.txt", "r", encoding="utf-8")
    for i in rules_file.readlines():
        print(i.strip("\n"))
    rules_file.close()

def keeping_dice():
    """Displays the rules for keeping dice to play the game"""
    keeping_dice_file = open("KeepingDice.txt", "r", encoding="utf-8")
    for i in keeping_dice_file.readlines():
        print(i.strip("\n"))
    keeping_dice_file.close()

def score_board():
    """Displays the score board"""
    display_score = "".join([f"{key}: {value}, " for key, value in player.score_sheet.items()])
    print("Score Board")
    print(display_score.strip(", "), "\n")
    time.sleep(1)

class Farkle:
    def __init__(self):
        self.score_sheet = {}
        self.comp_players = {}
        self.whos_first = []
        self.player_order = []
        self.current_player = ""
        self.human_roller = ""
        self.choice_of_comp_players = {}

    def opponents_difficulty(self):
        """Sets random difficulty for all possible opponents"""
        num = 1
        for name in OPPONENTS:
            for diff in random.choice(list(DIFFICULTY.items())):
                self.choice_of_comp_players[name] = diff
        difficulty = list(DIFFICULTY.keys())
        comp_player = list(self.choice_of_comp_players.values())
        diff_val = list(DIFFICULTY.values())
        for pl in comp_player:
            diff_position = diff_val.index(pl)
            print(f"{num}:", OPPONENTS[num - 1], "-", difficulty[diff_position])
            num += 1

    @staticmethod
    def choose_opponents():
        """This let's player choose their opponents"""
        select_opponent = input("From the list above, choose up to 5 opponents using the "
                                "number next to their names with spaces between\n").split()
        if not select_opponent:
            return False
        for i in select_opponent:
            if i.isnumeric():
                j = int(i)
                if j < 1 or j > 11:
                    print("Please only use numbers between 1 and 11\n")
                    return False
                else:
                    continue
            elif not i.isnumeric() or i.isspace():
                print("Please only use numbers when selecting opponents\n")
                return False
        if len(select_opponent) > 5 or len(select_opponent) < 1:
            return False
        return select_opponent

    def opponent_update(self, select_opponent):
        """Adds the selected opponents to the score sheet"""
        for i in select_opponent:
            op = OPPONENTS[int(i) - 1]
            self.comp_players[op] = self.choice_of_comp_players[op]
            self.score_sheet[op] = 0

    def roll_for_first(self):
        """Automatically rolls a die for each comp including player and establishes who goes first"""
        for _ in self.score_sheet:
            dice = random.randrange(1, 7)
            self.whos_first.append(dice)
        highest_num = max(self.whos_first)
        highest_num_count = self.whos_first.count(max(self.whos_first))
        highest_rolls_index = {}
        # If two or more highest rolls exists, re-roll for first roller
        for roller, die in enumerate(self.whos_first):
            if die == highest_num and highest_num_count > 1:
                highest_rolls_index[player] = die
        if highest_rolls_index:
            for index, _ in highest_rolls_index.items():
                # The next line checks if only one player rolled the highest die to break out of loop
                if self.whos_first.count(max(highest_rolls_index.values())) <= 1:
                    break
                else:
                    dice = random.randrange(1, 7)
                    self.whos_first.pop(index)
                    self.whos_first.insert(index, dice)
                    highest_rolls_index[index] = dice
            return highest_rolls_index
        else:
            # Sets the player order based on the highest die rolled
            rotate_player_order = deque(self.score_sheet)
            rotate_player_order.rotate(len(self.whos_first) - self.whos_first.index(max(self.whos_first)))
            rotate_player_order = list(rotate_player_order)
            for i in rotate_player_order:
                self.player_order.append(i)
            self.current_player = self.player_order[0]
            # Displays who rolls first
            if self.player_order[0] == self.human_roller:
                score_board()
                print("You are first.")
                return highest_rolls_index
            else:
                score_board()
                print(f"{self.player_order[0]} rolls first.")
                return highest_rolls_index

    def playing_order(self, highest_rolls_index):
        """Sets up the playing order based on which player rolled the highest die"""
        if highest_rolls_index:
            c = max(highest_rolls_index, key=lambda key: highest_rolls_index[key])
            rotate_player_order = deque(self.score_sheet)
            rotate_player_order.rotate(len(self.whos_first) - c)
            rotate_player_order = list(rotate_player_order)
            for i in rotate_player_order:
                self.player_order.append(i)
            self.current_player = self.player_order[0]
            if self.player_order[0] == self.human_roller:
                print("You are first.\n")
            else:
                print(f"{self.player_order[0]} rolls first.\n")
        else:
            return

class Player(Farkle):
    def __init__(self):
        super().__init__()
        self.num_dice = 6
        self.kept_dice = []
        self.face_off = []
        self.face_off_rounds = 1
        self.dice_count = {}
        self.selected_dice = []
        self.face_off_check = []

    def roll_dice(self):
        """This rolls the dice"""
        dice = [random.randrange(1, 7) for _ in range(self.num_dice)]
        return dice

    @staticmethod
    def show_dice(dice):
        """Displays dice rolled by player"""
        print(*dice, "\n", sep=" ")

    def count_dice(self, dice):
        """Counts how many of each die rolled"""
        self.dice_count.clear()
        for i in range(len(dice)):
            self.dice_count[dice[i]] = dice.count(dice[i])

    def farkle_check(self, dice):
        """Checks to see if any player has playable dice or if farkle"""
        if len(dice) == 6 and len(self.dice_count) == 1:
            print("You Win!")
            exit()
        elif (1 in self.dice_count or 5 in self.dice_count) or max(self.dice_count.values()) >= 3 or\
                len(self.dice_count) == 6 or\
                (len(self.dice_count) == 3 and all(x == 2 for x in self.dice_count.values()) is True):
            return False
        else:
            return True

    def is_on_board(self, score):
        """Checks to see if player is on the board/score sheet"""
        if (self.current_player == self.human_roller or self.current_player != self.human_roller)\
           and score < MIN_SCORE and self.score_sheet[self.current_player] == 0:
            print(f"You are not on the board yet and need {MIN_SCORE} to stop")
            return ROLL_DICE
        else:
            remaining_dice = 6 - self.num_dice
            self.num_dice = self.num_dice + remaining_dice
            return UPDATE_SCORE

    def current_score(self):
        """Goes through all the kept dice and adds them to the score board. Also checks if score is at least 450
        before allowing player to stop rolling"""
        score = 0
        for i in self.kept_dice:
            if i in PLAYABLE_DICE:
                score += PLAYABLE_DICE[PLAYABLE_DICE.index(i) + 1]
            elif i not in PLAYABLE_DICE and len(i) == 6 and \
                    ((i.count(1) or i.count(2) or i.count(3) or i.count(4) or i.count(5) or i.count(6)) > 1):
                score += 500
        return score

    def if_over_winning_score(self, score):
        """Checks to see if current player has higher score than player that reached the winning score"""
        if self.score_sheet[self.current_player] + score > max(self.score_sheet.values()):
            return IS_ON_BOARD
        else:
            print(f"Sorry, {max(self.score_sheet, key=lambda key: self.score_sheet[key])} is over {WINNING_SCORE}."
                  f" You must keep rolling.")
            return ROLL_DICE

    def farkled(self):
        """Resets the conditions for next player after current player farkled"""
        remaining_dice = 6 - self.num_dice
        self.num_dice = self.num_dice + remaining_dice
        if self.current_player in self.face_off:
            self.face_off.remove(self.current_player)
        if self.current_player == self.human_roller:
            print("You Farkled\n")
            time.sleep(1)
        else:
            print(f"{self.current_player} Farkled\n")
        self.kept_dice.clear()

    def update_score(self, score):
        """Adds score of current player to score sheet"""
        self.score_sheet[self.current_player] += score
        self.kept_dice.clear()
        print(f"{self.current_player} scored {score} this turn\n")

    def winning_conditions(self, score):
        """Checks to see if current player passed winning score"""
        # Adds first player to reach winning score to face off list
        if not self.face_off and (self.score_sheet[self.current_player] + score >= WINNING_SCORE) and\
                self.face_off_rounds >= 1:
            # Adds current winning score player to face off list
            if self.score_sheet[self.current_player] + score > max(self.score_sheet.values()) and\
                    self.face_off_rounds == 1:
                self.face_off.append(self.current_player)
            else:
                # This sets the first person who got over the goal score
                self.face_off.append(self.current_player)
        # Adds players that beat current winning score to face off list
        elif self.face_off:
            if self.current_player != self.face_off[0] and self.current_player not in self.face_off and\
                    self.score_sheet[self.current_player] + score > max(self.score_sheet.values()):
                self.face_off.append(self.current_player)

    def facing_off(self):
        """Counts how many rounds of sudden death when more than one person surpass the winning score and the current
        highest score"""
        if self.face_off and player.player_order[1] == self.face_off[0]:
            self.face_off_rounds += 1

    def next_player(self):
        """Changes players to the next player"""
        deck = deque(self.player_order)
        deck.rotate(-1)
        deck = list(deck)
        self.player_order.clear()
        for i in deck:
            self.player_order.append(i)
        self.current_player = self.player_order[0]

    def check_for_winner(self):
        """Checks next player to see if there is a winner only after winning score is reached and one more round is
        played"""
        # The player met highest score after winning one or more rounds of sudden death
        if player.player_order[1] in self.face_off and len(self.face_off) == 1 and self.face_off_rounds >= 1:
            return WINNER
        # Brings player to sudden death rounds
        elif player.player_order[1] in self.face_off and len(self.face_off) > 1 and self.face_off_rounds > 1:
            return SUDDEN_DEATH
        # The player met the highest score and no other player passed it
        elif player.player_order[1] in self.face_off and len(self.face_off) == 1 and self.face_off_rounds == 1:
            return WINNER
        return CURRENT_ROLLER

    def current_roller(self):
        """Tells the new player it is their turn"""
        if self.current_player == self.human_roller:
            print("It is your turn")
        else:
            print(f"It is {self.current_player}'s turn")

    def sudden_death(self):
        """Sets up play for those who scored over winning score and then beat the highest score"""
        for i in self.face_off:
            self.face_off_check.append(i)
        # Rotates face off check list then adds it to player order
        if self.current_player == self.face_off[0]:
            deck = deque(self.face_off_check)
            deck.rotate(-1)
            deck = list(deck)
            self.player_order.clear()
            for i in deck:
                self.player_order.append(i)
            self.current_player = self.player_order[0]
            self.face_off_check.clear()
        # Adds face off check elements to player order
        else:
            self.player_order.clear()
            for i in self.face_off_check:
                self.player_order.append(i)
            self.current_player = self.face_off_check[0]
            self.face_off_check.clear()
        return ROLL_DICE

    def winner(self):
        """Resets the game but keeps the human player"""
        self.score_sheet = {}
        self.player_order = []
        self.whos_first = []
        self.comp_players = {}
        self.choice_of_comp_players = {}

        self.num_dice = 6
        self.face_off = []
        self.face_off_rounds = 1
        self.kept_dice = []

        computer_player.organize = []
        computer_player.sift = []

        if self.current_player == self.human_roller:
            self.score_sheet[self.human_roller] = 0
            self.current_player = ""
            print(f"You win!! :) :)")
            time.sleep(1.13)

        else:
            print(f"{self.current_player} wins! Sorry for the loss :(")
            self.score_sheet[self.human_roller] = 0
            self.current_player = ""
            time.sleep(1.13)

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def human_player(self):
        """Displays human player roll"""
        roll = input("Press r to roll\n")
        if roll != "r":
            print("Please, press r")
            self.human_player()
        else:
            print("rolling...\n")
            time.sleep(1.25)
            print("You rolled:")

    @staticmethod
    def player_select_dice(dice):
        """Let's human player select their dice"""
        stop_rolling = "roll"
        keep_dice = [str(input("What dice do you want to keep?\n")).split()]
        # Checks for incorrect inputs
        for sub_list in keep_dice:
            for dice_group in sub_list:
                if not dice_group.isalnum():
                    print("Please only use numbers for picking dice and letters to spell stop if you wish to stop\n")
                    print("Your roll was:")
                    print(*dice, "\n", sep=" ")
                    return False
                elif dice_group.isalnum() and not dice_group.isnumeric() and dice_group != "stop":
                    print("Please spell stop correctly\n")
                    print("Your roll was:")
                    print(*dice, "\n", sep=" ")
                    return False
                elif dice_group == "stop":
                    stop_rolling = sub_list.pop(sub_list.index(dice_group))
                elif len(dice_group) == 6:
                    for die in dice_group:
                        if dice_group == "123456":
                            continue
                        elif dice.count(int(die)) == 2 and int(die) in dice:
                            continue
                        else:
                            print(f"You've entered the wrong dice")
                            print("Your roll was:")
                            print(*dice, "\n", sep=" ")
                            return False
                elif len(dice_group) > 1:
                    for die in dice_group:
                        if len(dice_group) > dice.count(int(die)) == 3:
                            print(f"You've selected too many {die}s\n")
                            print("Your roll was:")
                            print(*dice, "\n", sep=" ")
                            return False
                        elif len(dice_group) > dice.count(int(die)):
                            print(f"You've selected a non playable set\n")
                            print("Your roll was:")
                            print(*dice, "\n", sep=" ")
                            return False
                        elif len(dice_group) < 3:
                            print(f"You don't have enough {die}s for a set\n")
                            print("Your roll was:")
                            print(*dice, "\n", sep=" ")
                            return False
                        elif int(die) not in dice:
                            print("Please pick numbers from rolled dice only\n")
                            print("Your roll was:")
                            print(*dice, "\n", sep=" ")
                            return False
                elif len(dice_group) == 1:
                    for die in dice_group:
                        if int(dice_group[0]) not in dice:
                            print("Please pick numbers from rolled dice only\n")
                            print("Your roll was:")
                            print(*dice, "\n", sep=" ")
                            return False
                        elif sub_list.count(die) > dice.count(int(die)):
                            print(f"You've selected more {die}s than available\n")
                            print("Your roll was:")
                            print(*dice, "\n", sep=" ")
                            return False
                        elif int(die) != 1 and int(die) != 5:
                            print("Please select playable dice\n")
                            return False
                else:
                    return False
        return keep_dice, stop_rolling

    @staticmethod
    def dice_conversion(keep_dice):
        """Converts the dice, updates the kept dice, and decreases number of dice"""
        add_spaces = [[" ".join(j)] if len(j) > 1 else [j] for i in keep_dice for j in i]
        split_multiples = [sub.split() for subl in add_spaces for sub in subl]
        int_conversion = [[int(x) for x in lst] for lst in split_multiples]
        for dice in int_conversion:
            player.kept_dice.append(dice)
            for _ in dice:
                player.num_dice -= 1

    @staticmethod
    def player_dice_playable():
        """Checks to see if the kept dice are actually playable"""
        for i in player.kept_dice:
            if i in PLAYABLE_DICE:
                continue
            elif i not in PLAYABLE_DICE and len(i) == 6 and \
                    ((i.count(1) or i.count(2) or i.count(3) or i.count(4) or i.count(5) or i.count(6)) > 1):
                continue
            else:
                return False

    @staticmethod
    def player_turn(stop_rolling):
        """Checks if human player has stopped rolling, resets dice as necessary, checks if on score sheet and if
        higher than the current high score that surpassed the winning score"""
        if player.num_dice == 0 and stop_rolling == "roll":
            player.num_dice += 6
            return ROLL_DICE
        elif player.num_dice > 0 and stop_rolling == "roll":
            return ROLL_DICE
        elif player.num_dice == 0 and stop_rolling == "stop":
            player.num_dice += 6
            print("You rolled all the dice. You must continue rolling.\n")
            return ROLL_DICE
        # When winning score is reached, player must keep rolling if not above current highest score
        elif player.num_dice > 0 and stop_rolling == "stop" and player.score_sheet[player.current_player] >= MIN_SCORE:
            if max(player.score_sheet.values()) >= WINNING_SCORE:
                return IF_OVER_WINNING_SCORE
            remaining_dice = 6 - player.num_dice
            player.num_dice = player.num_dice + remaining_dice
            return CURRENT_SCORE
        # When winning score is reached, player must keep rolling if not above current
        #   highest score and not currently on board
        elif player.num_dice > 0 and stop_rolling == "stop" and player.score_sheet[player.current_player] == 0:
            if max(player.score_sheet.values()) >= WINNING_SCORE:
                return IF_OVER_WINNING_SCORE
            return CURRENT_SCORE

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()
        self.organize = []
        self.sift = []

    @staticmethod
    def comp_player():
        """Displays the act of rolling for the computer player"""
        print("Press r to roll")
        time.sleep(.25)
        print("r")
        print("rolling...\n")
        time.sleep(1.25)
        print(f"{player.current_player} rolled:")

    def comp_turn(self, dice):
        """Checks to see if comp player has """
        print("What dice do you want to keep?\n")
        time.sleep(1.75)
        if len(dice) == 6:
            for i in dice:
                # For straights
                if len(player.dice_count) == 6:
                    self.organize.append(i)
                    player.selected_dice.append(i)
                    player.num_dice -= 1
                # For three sets of pairs
                elif len(player.dice_count) == 3 and player.dice_count[i] == 2 and all(player.dice_count[i] == 2 for i in player.dice_count):
                    self.organize.append(i)
                    player.selected_dice.append(i)
                    player.num_dice -= 1
                # For two threes of a kind
                elif len(player.dice_count) == 2 and player.dice_count[i] == 3:
                    self.sift.append(i)
                    player.selected_dice.append(i)
                    player.num_dice -= 1
                    if i != self.sift[0]:
                        num = self.sift.pop()
                        self.organize.append(num)
                # For triples and possible single playable dice
                elif dice.count(i) >= 3:
                    self.organize.append(i)
                    player.selected_dice.append(i)
                    player.num_dice -= 1
                # For 1s and/or 5s non-sets
                elif i == 1 or i == 5 in player.dice_count:
                    player.kept_dice.append([i])
                    player.selected_dice.append(i)
                    player.num_dice -= 1
        elif len(dice) == 5:
            for i in dice:
                # For triples and possible single playable dice
                if player.dice_count[i] >= 3:
                    self.organize.append(i)
                    player.selected_dice.append(i)
                    player.num_dice -= 1
                # For 1s and/or 5s non-sets
                elif i == 1 or i == 5 in player.dice_count:
                    player.kept_dice.append([i])
                    player.selected_dice.append(i)
                    player.num_dice -= 1
        elif len(dice) == 4:
            for i in dice:
                # For triples and possible single playable dice
                if player.dice_count[i] >= 3:
                    self.organize.append(i)
                    player.selected_dice.append(i)
                    player.num_dice -= 1
                # For 1s and/or 5s non-sets
                elif i == 1 or i == 5 in player.dice_count:
                    player.kept_dice.append([i])
                    player.selected_dice.append(i)
                    player.num_dice -= 1
        elif len(dice) == 3 or len(dice) == 2 or len(dice) == 1:
            for i in dice:
                # For triples
                if player.dice_count[i] == 3:
                    self.organize.append(i)
                    player.selected_dice.append(i)
                    player.num_dice -= 1
                # For 1s and/or 5s non-sets
                elif i == 1 or i == 5 in player.dice_count:
                    player.kept_dice.append([i])
                    player.selected_dice.append(i)
                    player.num_dice -= 1

    def comp_turn_finalize(self):
        """Displays which dice or die the computer kept for each turn"""
        self.organize.sort()
        if self.organize:
            player.kept_dice.append(self.organize[:])
        elif not self.organize and self.sift:
            player.kept_dice.append(self.sift[:])
        self.organize.clear()
        self.sift.clear()
        print(f"{player.current_player} selected:")
        print(*player.selected_dice, sep=" ")
        player.selected_dice.clear()

    @staticmethod
    def comp_out_of_dice():
        """If the computer runs out of dice while selecting playable dice, the dice amount is reset"""
        if player.num_dice == 0:
            player.num_dice += 6
            return ROLL_DICE
        else:
            return COMP_KEEP_ROLLING

    @staticmethod
    def comp_chance():
        """Random int used to determine computer player stopping or rolling"""
        chance = random.randint(1, 15)
        return chance

    @staticmethod
    def comp_keep_rolling(chance):
        """Checks to see if the computer will stop its turn or even can"""
        if (chance in player.comp_players[player.current_player]) and\
                player.score_sheet[player.current_player] >= MIN_SCORE or player.score_sheet[player.current_player] == 0:
            print(f"{player.current_player} is stopping their turn.")
            # Checks if the if winning score was surpassed
            if max(player.score_sheet.values()) >= WINNING_SCORE:
                return IF_OVER_WINNING_SCORE
            else:
                remaining_dice = 6 - player.num_dice
                player.num_dice = player.num_dice + remaining_dice
                return CURRENT_SCORE
        # Trying to end turn
        elif (chance in player.comp_players[player.current_player]) and player.score_sheet[player.current_player] == 0:
            return CURRENT_SCORE
        else:
            return ROLL_DICE


player = Player()
h_player = HumanPlayer()
computer_player = ComputerPlayer()


def main_menu():
    """Starts the game and acts as the main menu"""
    print("Hello. Welcome to Farkle.")
    run = True
    while run:
        if not player.human_roller:
            name = input("What is your name?\n").capitalize()
            if not name:
                print("Must enter a name")
                continue
            elif not name.isalpha():
                print("Name can only consist of letters")
                continue
            player.score_sheet[name] = 0
            player.human_roller = name
        show_rules = input("Would you like to know how to play? (y/n)?\n")
        if show_rules == "y":
            display_rules()
        elif show_rules == "n":
            keeping_dice()
        else:
            print("Please type y for yes or n for no")
            continue
        while True:
            start = input("Would you like to start? (y/n)\n")
            if start == "y":
                main()
            elif start == "n":
                stop = input("Would you like to exit? (y/n)\n")
                if stop == "y":
                    exit()
                elif stop == "n":
                    continue
                else:
                    print("Please type y for yes or n for no\n")
                    continue
            else:
                print("Please type y for yes or n for no\n")
                continue

def main():
    """The main loop of the game"""
    player.opponents_difficulty()
    choosing_opponents = player.choose_opponents()
    while True:
        if choosing_opponents is False:
            choosing_opponents = player.choose_opponents()
        else:
            break
    player.opponent_update(choosing_opponents)
    player.playing_order(player.roll_for_first())

    run = True
    while run:
        if player.player_order[0] == player.human_roller:
            h_player.human_player()
            human_rolling = True
            while human_rolling:
                dice = player.roll_dice()
                player.count_dice(dice)
                player.show_dice(dice)
                did_farkle = player.farkle_check(dice)

                if did_farkle:
                    player.farkled()
                    player.facing_off()
                    score_board()
                    check_winner = player.check_for_winner()
                    if check_winner == WINNER:
                        player.next_player()
                        player.winner()
                        human_rolling = False
                        run = False

                    elif check_winner == SUDDEN_DEATH:
                        sud_death = player.sudden_death()

                        if sud_death == ROLL_DICE:
                            player.current_roller()
                            human_rolling = False

                    elif check_winner == CURRENT_ROLLER:
                        player.next_player()
                        player.current_roller()
                        human_rolling = False

                elif not did_farkle:
                    player_sel_dice = h_player.player_select_dice(dice)
                    while True:
                        if player_sel_dice is False:
                            player_sel_dice = h_player.player_select_dice(dice)
                            continue

                        else:
                            break
                    keep_dice = player_sel_dice[0]
                    stop_rolling = player_sel_dice[1]
                    h_player.dice_conversion(keep_dice)
                    playable_dice = h_player.player_dice_playable()
                    while True:
                        if playable_dice is False:
                            player_sel_dice = h_player.player_select_dice(dice)
                            continue
                        else:
                            break
                    h_turn = h_player.player_turn(stop_rolling)
                    if h_turn == ROLL_DICE:
                        human_rolling = False
                    elif h_turn == CURRENT_SCORE:
                        score = player.current_score()
                        on_board = player.is_on_board(score)

                        if on_board == ROLL_DICE:
                            human_rolling = False
                        elif on_board == UPDATE_SCORE:
                            player.winning_conditions(score)
                            player.update_score(score)
                            player.facing_off()
                            score_board()
                            check_winner = player.check_for_winner()

                            if check_winner == WINNER:
                                player.next_player()
                                player.winner()
                                human_rolling = False
                                run = False

                            elif check_winner == SUDDEN_DEATH:
                                sud_death = player.sudden_death()

                                if sud_death == ROLL_DICE:
                                    player.current_roller()
                                    human_rolling = False

                            elif check_winner == CURRENT_ROLLER:
                                player.next_player()
                                player.current_roller()
                                human_rolling = False

                    elif h_turn == IF_OVER_WINNING_SCORE:
                        score = player.current_score()
                        if_over_win_score = player.if_over_winning_score(score)

                        if if_over_win_score == IS_ON_BOARD:
                            on_board = player.is_on_board(score)

                            if on_board == ROLL_DICE:
                                human_rolling = False
                            elif on_board == UPDATE_SCORE:
                                player.winning_conditions(score)
                                player.update_score(score)
                                player.facing_off()
                                score_board()
                                check_winner = player.check_for_winner()

                                if check_winner == WINNER:
                                    player.next_player()
                                    player.winner()
                                    human_rolling = False
                                    run = False

                                elif check_winner == SUDDEN_DEATH:
                                    sud_death = player.sudden_death()

                                    if sud_death == ROLL_DICE:
                                        player.current_roller()
                                        human_rolling = False

                                elif check_winner == CURRENT_ROLLER:
                                    player.next_player()
                                    player.current_roller()
                                    human_rolling = False

                        elif if_over_win_score == ROLL_DICE:
                            human_rolling = False

        elif player.player_order[0] != player.human_roller:
            computer_player.comp_player()
            comp_rolling = True
            while comp_rolling:
                dice = player.roll_dice()
                player.count_dice(dice)
                player.show_dice(dice)
                did_farkle = player.farkle_check(dice)
                if did_farkle:
                    player.farkled()
                    player.facing_off()
                    score_board()
                    check_winner = player.check_for_winner()
                    if check_winner == WINNER:
                        player.next_player()
                        player.winner()
                        comp_rolling = False
                        run = False

                    elif check_winner == SUDDEN_DEATH:
                        sud_death = player.sudden_death()

                        if sud_death == ROLL_DICE:
                            player.current_roller()
                            comp_rolling = False

                    elif check_winner == CURRENT_ROLLER:
                        player.next_player()
                        player.current_roller()
                        comp_rolling = False

                elif not did_farkle:
                    computer_player.comp_turn(dice)
                    computer_player.comp_turn_finalize()
                    comp_no_dice = computer_player.comp_out_of_dice()

                    if comp_no_dice == ROLL_DICE:
                        comp_rolling = False
                    elif comp_no_dice == COMP_KEEP_ROLLING:
                        comp_keep_roll = computer_player.comp_keep_rolling(computer_player.comp_chance())

                        if comp_keep_roll == CURRENT_SCORE:
                            score = player.current_score()
                            on_board = player.is_on_board(score)


                            if on_board == ROLL_DICE:
                                comp_rolling = False
                            elif on_board == UPDATE_SCORE:
                                player.winning_conditions(score)
                                player.update_score(score)
                                player.facing_off()
                                score_board()
                                check_winner = player.check_for_winner()

                                if check_winner == WINNER:
                                    player.next_player()
                                    player.winner()
                                    comp_rolling = False
                                    run = False

                                elif check_winner == SUDDEN_DEATH:
                                    sud_death = player.sudden_death()

                                    if sud_death == ROLL_DICE:
                                        player.current_roller()
                                        comp_rolling = False

                                elif check_winner == CURRENT_ROLLER:
                                    player.next_player()
                                    player.current_roller()
                                    comp_rolling = False

                        elif comp_keep_roll == ROLL_DICE:
                            comp_rolling = False
                        elif comp_keep_roll == IF_OVER_WINNING_SCORE:
                            score = player.current_score()
                            if_over_win_score = player.if_over_winning_score(score)

                            if if_over_win_score == ROLL_DICE:
                                comp_rolling = False
                            elif if_over_win_score == IS_ON_BOARD:
                                on_board = player.is_on_board(score)

                                if on_board == ROLL_DICE:
                                    comp_rolling = False
                                elif on_board == UPDATE_SCORE:
                                    player.winning_conditions(score)
                                    player.update_score(score)
                                    player.facing_off()
                                    score_board()
                                    check_winner = player.check_for_winner()

                                    if check_winner == WINNER:
                                        player.next_player()
                                        player.winner()
                                        comp_rolling = False
                                        run = False

                                    elif check_winner == SUDDEN_DEATH:
                                        sud_death = player.sudden_death()

                                        if sud_death == ROLL_DICE:
                                            player.current_roller()
                                            comp_rolling = False

                                    elif check_winner == CURRENT_ROLLER:
                                        player.next_player()
                                        player.current_roller()
                                        comp_rolling = False


main_menu()
