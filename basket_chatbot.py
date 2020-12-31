import nltk
import numpy as np
import random
import string

import bs4 as bs
import urllib.request
import re

nltk.download('punkt')
nltk.download('wordnet')
raw_html = urllib.request.urlopen('https://en.wikipedia.org/wiki/Basketball')
raw_html = raw_html.read()

article_html = bs.BeautifulSoup(raw_html, 'lxml')

article_paragraphs = article_html.find_all('p')

article_text = ''

for para in article_paragraphs:
    article_text += para.text

article_text = article_text.lower()

article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

article_sentences = nltk.sent_tokenize(article_text)
article_words = nltk.word_tokenize(article_text)

wnlemmatizer = nltk.stem.WordNetLemmatizer()

def perform_lemmatization(tokens):
    return [wnlemmatizer.lemmatize(token) for token in tokens]

punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)

def get_processed_text(document):
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))

greeting_inputs = ("hey", "good morning", "good evening", "morning", "evening", "hi", "whatsup")
greeting_responses = ["hey", "hey hows you?", "*nods*", "hello, how you doing", "hello", "Welcome, I am good and you"]

def generate_greeting_response(greeting):
    for token in greeting.split():
        if token.lower() in greeting_inputs:
            return random.choice(greeting_responses)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_response(user_input):
    basketrobo_response = ''
    article_sentences.append(user_input)

    word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
    all_word_vectors = word_vectorizer.fit_transform(article_sentences)
    similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    similar_sentence_number = similar_vector_values.argsort()[0][-2]

    matched_vector = similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]

    if vector_matched == 0:
        basketrobo_response = basketrobo_response + "I am sorry, I could not understand you"
        return basketrobo_response
    else:
        basketrobo_response = basketrobo_response + article_sentences[similar_sentence_number]
        return basketrobo_response


continue_dialogue = True
print("Hello, I am your friend BasketRobo. You can ask me any question regarding Basket:")
while(continue_dialogue == True):
    human_text = input()
    human_text = human_text.lower()
    if human_text != 'bye':
        if human_text == 'thanks' or human_text == 'thank you very much' or human_text == 'thank you':
            continue_dialogue = False
            print("BasketRobo: Most welcome")
        else:
            if generate_greeting_response(human_text) != None:
                print("BasketRobo: " + generate_greeting_response(human_text))
            else:
                print("BasketRobo: ", end="")
                print(generate_response(human_text))
                article_sentences.remove(human_text)
    else:
        continue_dialogue = False
        print("BasketRobo: Good bye and take care of yourself...")