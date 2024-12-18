import random
from z3 import Solver, Distinct, Int, Or, And
from english_words import get_english_words_set

def load_word_list():
    # Load a set of 5-letter words from a library.
    words_set = get_english_words_set(["web2"], lower=True)
    return [word for word in words_set if len(word) == 5]

def pick_random_word(word_list):
    return random.choice(word_list)

def play_wordle():
    word_list = load_word_list()
    target_word = pick_random_word(word_list)
    attempts = 6

    print("Welcome to Wordle! Guess the 5-letter word.")

    while attempts > 0:
        guess = input(f"Enter your guess ({attempts} attempts left): ").lower()

        if len(guess) != 5 or guess not in word_list:
            print("Invalid guess. Make sure it's a 5-letter word from the word list.")
            continue

        if guess == target_word:
            print("Congratulations! You guessed the word!")
            return

        feedback = []
        for g_char, t_char in zip(guess, target_word):
            if g_char == t_char:
                feedback.append("G")  # Green: correct letter and position
            elif g_char in target_word:
                feedback.append("Y")  # Yellow: correct letter, wrong position
            else:
                feedback.append("B")  # Black: incorrect letter

        print(f"Feedback: {''.join(feedback)}")
        attempts -= 1

    print(f"Sorry, you're out of attempts! The word was: {target_word}")

def solve_wordle_with_z3():
    word_list = load_word_list()
    target_word = pick_random_word(word_list)
    attempts = 6

    print("Welcome to Wordle Solver with Z3! Solving the 5-letter word.")

    solver = Solver()

    # Define variables for each position in the word
    vars = [Int(f"c{i}") for i in range(5)]
    for var in vars:
        solver.add(var >= ord('a'), var <= ord('z'))

    # Encode the word list into constraints
    word_constraints = []
    for word in word_list:
        word_constraints.append(And([vars[i] == ord(word[i]) for i in range(5)]))
    solver.add(Or(word_constraints))

    while attempts > 0:
        guess = pick_random_word(word_list)
        print(f"Z3 Solver guesses: {guess}")

        if guess == target_word:
            print("Solver found the word correctly!")
            return

        feedback = []
        for i, char in enumerate(guess):
            if char == target_word[i]:
                feedback.append("G")
                solver.add(vars[i] == ord(char))
            elif char in target_word:
                feedback.append("Y")
                solver.add(vars[i] != ord(char))  # Correct letter, wrong position
            else:
                feedback.append("B")
                solver.add(And([vars[j] != ord(char) for j in range(5)]))

        print(f"Feedback for {guess}: {''.join(feedback)}")
        attempts -= 1

        if solver.check() == "unsat":
            print("No possible words match the constraints. Exiting.")
            return

    print(f"Solver failed to find the word. The word was: {target_word}")

if __name__ == "__main__":
    print("Part 1: Play Wordle")
    play_wordle()
    print("\nPart 2: Solve Wordle with Z3")
    solve_wordle_with_z3()



