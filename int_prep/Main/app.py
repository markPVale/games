from flask import Flask, render_template, request, redirect, url_for
from rich.console import Console
from rich.table import Table
from utils import evaluate_guess, display_word, game_status, challenge_word
from challenge_word_list import word_list
import random

app = Flask(__name__)
app.jinja_env.cache = {}
app.config['TEMPLATES_AUTO_RELOAD'] = True
console = Console()
app.secret_key = 'my_secret_key'

word_to_guess = challenge_word(word_list)
correct_guesses = set()
remaining_chances = 5

def reset_game():
    global word_to_guess, correct_guesses, remaining_chances
    word_to_guess = challenge_word(word_list)
    correct_guesses = set()
    remaining_chances = 5
    print("resetting***")

@app.route("/", methods=["GET", "POST"])
def index():
    global word_to_guess, correct_guesses, remaining_chances
    message = None
    message_class = None

    if request.method == "POST":
        guess = request.form.get("guess", "").strip().lower()
        if guess:
          print("guessing***")
          if not evaluate_guess(word_to_guess["word"], guess, correct_guesses):
              remaining_chances -= 1
              correct_guesses.add(guess)  # Update the set of correct guesses
              status = game_status(word_to_guess["word"], correct_guesses)
              if status == "win":
                  message = "you win"
                  message_class = "congratulations"
                  reset_game()
              else:
                  print("remaining", remaining_chances)
                  if remaining_chances == 0:
                      message = "game over"
                      message_class = "game-over"
                      reset_game()

    status = game_status(word_to_guess["word"], correct_guesses)
    displayed_word = display_word(word_to_guess["word"], correct_guesses)
    print("displayed_word", displayed_word)
    table = Table(title="wordle", show_lines=True)
    table.add_row(displayed_word)
    console.print(table)

    incorrect_boxes = ["green" if i < remaining_chances else "red" for i in range(5)]

    return render_template("index.html",
                           word=displayed_word,
                           hint=word_to_guess["hint"],
                           remaining_chances=remaining_chances,
                           message=message,
                           message_class=message_class)

@app.route("/reset")
def reset():
    global word_to_guess, correct_guesses, remaining_chances
    word_to_guess = random.choice(word_list)
    correct_guesses = set()
    remaining_chances = 5
    print("reset***")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
