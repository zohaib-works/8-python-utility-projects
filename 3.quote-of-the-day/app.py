from flask import Flask, render_template, request, redirect, url_for
import random


app = Flask(__name__)

def get_random_quote():
    with open('quotes.txt', 'r', encoding='utf-8') as file:
        quotes = file.readlines()
        random_quote = random.choice(quotes)
        return random_quote.strip()

@app.route('/')
def index():
    quote = get_random_quote()
    return render_template('/website/index.html', quote=quote)


if __name__ == '__main__':
    app.run(debug=True)
