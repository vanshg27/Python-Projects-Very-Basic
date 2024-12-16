import doctest
import random
import mysql.connector
class Hangman:
    def __init__(self, word: str) -> None:
        self.word = word.upper()  # Store the word in uppercase
        self.mistake = 0  # Track mistakes
        self.lis = [] # Initialize empty progress list
        for i in self.word:
            if i.isalpha():
                self.lis.append('')
            else:
                self.lis.append(i)

    def initialize_game(self):
        """
        :return: empty list with the number of characters in word
        """
        return self.lis

    def print_word(self) -> str:
        """
        :return: word progress
        >>> hang = Hangman("hello")
        >>> hang.print_word()
        '_____'
        """
        for i in range(len(self.lis)):
            if self.lis[i] == '':
                self.lis[i] = '_'
            elif self.lis[i] == ' ':
                self.lis[i] == ' '
        return "".join(self.lis)

    def build_hangman(self):
        HANGMANPICS = [
            r"""
                  +---+
                  |   |
                      |
                      |
                      |
                      |
                =========
            """,
            r"""
                  +---+
                  |   |
                  O   |
                      |
                      |
                      |
                =========
            """,
            r"""
                  +---+
                  |   |
                  O   |
                  |   |
                      |
                      |
                =========
            """,
            r"""
                  +---+
                  |   |
                  O   |
                 /|   |
                      |
                      |
                =========
            """,
            r"""
                  +---+
                  |   |
                  O   |
                 /|\  |
                      |
                      |
                =========
            """,
            r"""
                  +---+
                  |   |
                  O   |
                 /|\  |
                 /    |
                      |
                =========
            """,
            r"""
                  +---+
                  |   |
                  O   |
                 /|\  |
                 / \  |
                      |
                =========
            """
        ]

        print(HANGMANPICS[self.mistake -1])

    def update_guess(self, guess: str) -> None:
        """
        Update the progress list if the guess is correct.
        Increment mistakes if the guess is incorrect.
        """
        guess = guess.upper()
        if guess in self.word:
            for i, char in enumerate(self.word):
                if char == guess:
                    self.lis[i] = guess
        else:
            self.mistake += 1
            self.build_hangman()

    def is_game_over(self) -> bool:
        """
        Check if the game is over due to a win or loss.
        """
        return self.mistake >= 7 or "_" not in self.print_word()


def word_selection() -> str:
    topic = input("""-- Pick a topic by selecting the assigned number next to its name --
    -- Business : 1, Science : 2, Countries: 3, TV shows : 4, Songs : 5 --
    Enter Selection: """)
    t_d = {'1':'business','2':'science','3':'countries','4':'tv','5':'songs'}
    con1 = mysql.connector.connect(user = 'root',password = 'password1234',
                                    host = 'localhost', database = 'hangman')
    cur = con1.cursor()
    query = f"SELECT name from {t_d[topic]};"
    cur.execute(query)
    data = cur.fetchall()
    d_l = []
    for i in data:
        d_l.append(i[0])
    word = random.choice(d_l)
    return word


# Initialize game
word = word_selection()
hang = Hangman(word)

# Game loop
while not hang.is_game_over():
    print(hang.print_word())
    guess = input("Enter your guess: ").strip()

    # Validate input
    if len(guess) != 1 or not guess.isalpha():
        print("Invalid input. Please enter a single alphabetic character.")
        continue

    hang.update_guess(guess)

# End of game
if "_" not in hang.print_word():
    print(f"Congratulations! You've guessed the word: {word}")
else:
    print(f"Game over! The word was: {word}")
