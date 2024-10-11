import random

def evaluate_guess(word, guess, correct_guesses):
  if guess.lower() == word.lower():
    correct_guesses.update(word)
    print("correct_guesses222", correct_guesses)
    return True
  else:
    for letter in guess.lower():
      if letter in word.lower():
        correct_guesses.add(letter)
  return False

def display_word(word, correct_guesses):
  displayed_word = ""
  print("word", word)
  for letter in word:
    if letter in correct_guesses:
      displayed_word += letter
    else:
      displayed_word += "_"
  print("correct_guesses***", correct_guesses)
  return displayed_word

def game_status(word, correct_guesses):
  if set(word.lower()) == correct_guesses:
    return "win"
  return "ongoing"

def challenge_word(words):
  return random.choice(words)

