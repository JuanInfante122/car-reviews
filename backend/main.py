from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from collections import Counter
from flask_cors import CORS
from datetime import datetime

nltk.download('punkt')
nltk.download('stopwords')

analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)
CORS(app)

stopwords_es = set(nltk.corpus.stopwords.words('spanish'))

def clean_text(text):
    text = re.sub(r'\d+', '', text)  # Eliminar números
    text = re.sub(r'\s+', ' ', text)  # Reemplazar múltiples espacios por uno solo
    text = re.sub(r'[^\w\s]', '', text)  # Eliminar símbolos y puntuación
    return text.strip()

def remove_stopwords(text):
    words = nltk.word_tokenize(text, language='spanish')
    filtered_words = [word for word in words if word.lower() not in stopwords_es]
    return ' '.join(filtered_words)

def get_opinions_and_ratings(model, min_opinions=10):
    url = f'https://www.opinautos.com/co/{model}/opiniones'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    opinions = []
    ratings = []
    exclude_phrases = ['Lo mejor', 'Lo peor', 'Busca tu problema', 'Deja tu opinión', 'ModelXXXX']

    for opinion_span in soup.find_all('span', class_='align-middle'):
        cleaned_text = clean_text(opinion_span.get_text(strip=True))
        if cleaned_text and len(opinions) < min_opinions and not any(phrase in cleaned_text for phrase in exclude_phrases):
            opinions.append(cleaned_text)

    for rating_box in soup.find_all('div', class_='LeftRightBox__left LeftRightBox__left--noshrink'):
        stars = 0
        for star_index in range(1, 6):
            star_span = rating_box.find('span', {'data-starindex': str(star_index)})
            if star_span and star_span.find('img', {'src': 'https://static.opinautos.com/images/design2/icons/icon_star--gold.svg?v=5eb58b'}):
                stars += 1
        ratings.append(stars)

    opinions = opinions[:min_opinions]

    if len(opinions) < min_opinions:
        print(f'No se encontraron suficientes opiniones para {model}. Solo se encontraron {len(opinions)} opiniones.')

    return opinions, ratings

def analyze_sentiments(opinions):
    sentiments = []
    for opinion in opinions:
        cleaned_opinion = clean_text(opinion)
        sentiment = analyzer.polarity_scores(cleaned_opinion)
        sentiment_score = sentiment['compound']
        if sentiment_score > 0.1:
            sentiment_label = 'Positivo'
        elif sentiment_score < -0.1:
            sentiment_label = 'Negativo'
        else:
            sentiment_label = 'Neutral'
        sentiments.append((opinion, sentiment_label, sentiment_score))
    return sentiments

def summarize(opinions, num_sentences=5):
    text = " ".join(opinions)
    cleaned_text = remove_stopwords(text)
    parser = PlaintextParser.from_string(cleaned_text, Tokenizer('spanish'))
    summarizer = TextRankSummarizer()
    summary_sentences = summarizer(parser.document, num_sentences)
    summary = " ".join([str(sentence) for sentence in summary_sentences])
    return summary

def calculate_rating_change(ratings):
    if len(ratings) < 2:
        return 0  # No suficiente datos para cambio, retornar 0 en lugar de None.
    current_avg = sum(ratings[-5:]) / len(ratings[-5:])  # Últimos 5 ratings
    previous_avg = sum(ratings[:-5]) / len(ratings[:-5]) if len(ratings) > 5 else sum(ratings) / len(ratings)
    change = current_avg - previous_avg
    return round(change, 1)

@app.route('/api/opinions', methods=['GET'])
def get_car_opinions():
    model = request.args.get('model')
    if not model:
        return jsonify({'error': 'Model parameter is required'}), 400

    print(f"Fetching data for model: {model}")
    opinions, ratings = get_opinions_and_ratings(model)
    sentiments = analyze_sentiments(opinions)
    summary = summarize(opinions)
    average_rating = sum(ratings) / len(ratings) if ratings else None

    star_distribution = Counter(ratings)
    full_star_distribution = {star: star_distribution.get(star, 0) for star in range(1, 6)}
    
    rating_change = calculate_rating_change(ratings)

    # Registrar la fecha y hora de la última actualización
    last_updated = datetime.now().isoformat()

    print(f"Opinions: {opinions}")
    print(f"Ratings: {ratings}")
    print(f"Summary: {summary}")
    print(f"Average Rating: {average_rating}")
    print(f"Star Distribution: {full_star_distribution}")
    print(f"Rating Change: {rating_change}")

    return jsonify({
        'model': model,
        'opinions': opinions,
        'sentiments': [{'opinion': opinion, 'sentiment_label': sentiment_label, 'sentiment_score': sentiment_score} for opinion, sentiment_label, sentiment_score in sentiments],
        'summary': summary,
        'average_rating': round(average_rating, 1) if average_rating else 'No ratings available',
        'star_distribution': full_star_distribution,
        'rating_change': rating_change,
        'last_updated': last_updated
    })

if __name__ == '__main__':
    app.run(debug=True)

