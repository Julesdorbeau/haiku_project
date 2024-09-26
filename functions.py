import numpy as np
import syllables
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random

def count_syllables(word):
    # Use the syllables library to estimate the number of syllables in the word
    return syllables.estimate(word)

def count_words(text):
    # Split the text by whitespace and count the number of resulting words
    words = text.split()
    return len(words)

def get_next_word(seed_text, tokenizer, model, max_sequence_len):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    predicted = model.predict(token_list, verbose=0)
    predicted_word_index = np.argmax(predicted, axis=1)[0]
    return tokenizer.index_word[predicted_word_index]

def select_random_seed_word_from_tokenizer(tokenizer):
    # Get the list of words from the tokenizer's word index
    word_list = list(tokenizer.word_index.keys())
    if not word_list:
        raise ValueError("The tokenizer's word list is empty.")
    return random.choice(word_list)

def generate_haiku_from_params(params):
    # Parse parameters from the dictionary
    model_path = params.get('model_path', 'haiku_model.keras')
    seed_text = params.get('seed_text', 'A beach')
    syllables_mode = params.get('syllables_mode', False)
    words_mode = params.get('words_mode', True)
    haikus_pattern = params.get('haikus_pattern', [5, 7, 5])
    max_sequence_len = params.get('max_sequence_len', 21)
    tokenizer = params.get('tokenizer')

    # Handle potential errors with the tokenizer
    if tokenizer is None:
        raise ValueError("Tokenizer is not provided in the parameters.")

    # Load the model with error handling
    try:
        model = tf.keras.models.load_model(model_path)
    except (OSError, IOError) as e:
        raise RuntimeError(f"Failed to load the model from path '{model_path}': {e}")

    # Variables to store the generated haiku
    haiku = []

    # If in syllables mode, we count the syllables of the seed text
    # otherwise we count the words for the pattern
    current_line = seed_text 
    line_index = 0

    # Word and syllable count
    syllables_count = count_syllables(seed_text)
    word_count = count_words(seed_text)

    is_haiku_generated = False
    while not is_haiku_generated:
        # If we are in syllable mode we check if we have reached the syllable count
        if syllables_mode and (syllables_count >= haikus_pattern[line_index]) :
            # Adding the line to the haiku
            haiku.append(current_line)
            # Resetting the current line and syllables
            current_line = ""
            syllables_count = 0
            # Changing the line index
            line_index += 1

        # If we are in word mode we check if we have reached the word count
        elif words_mode and (word_count >= haikus_pattern[line_index]):
            # Adding the line to the haiku
            haiku.append(current_line)
            # Resetting the current line and syllables
            current_line = ""
            word_count = 0
            # Changing the line index
            line_index += 1

        # If we have reached the end of the haiku pattern
        if line_index >= len(haikus_pattern):
            is_haiku_generated = True
            break

        # Get the next word from the model and add it to the seed text
        new_word = get_next_word(seed_text, tokenizer, model, max_sequence_len)
        seed_text += " " + new_word

        # Counting the syllables of the new word and adding it to the current line
        # If this is in word mode, we only count the words
        if syllables_mode:
            syllables_count += count_syllables(new_word)
        elif words_mode:
            word_count += 1
        
        current_line += " " + new_word

    return seed_text, haiku