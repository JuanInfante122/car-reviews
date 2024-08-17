import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# Descargar recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Inicializar el analizador de sentimientos de VADER
analyzer = SentimentIntensityAnalyzer()

def clean_text(text):
    """Limpia el texto eliminando caracteres especiales y puntuación."""
    text = re.sub(r'\s+', ' ', text)  # Reemplazar múltiples espacios por uno solo
    text = re.sub(r'[^\w\s]', '', text)  # Eliminar puntuación
    return text.strip()

def get_opinions(model, min_opinions=10):
    url = f'https://www.opinautos.com/co/{model}/opiniones'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    opinions = set()
    exclude_phrases = ['Lo mejor', 'Lo peor', 'Busca tu problema', 'Deja tu opinión', 'ModelXXXX']

    for opinion_span in soup.find_all('span', class_='align-middle'):
        cleaned_text = clean_text(opinion_span.get_text(strip=True))
        if cleaned_text and len(opinions) < min_opinions and not any(phrase in cleaned_text for phrase in exclude_phrases):
            opinions.add(cleaned_text)

    opinions = list(opinions)[:min_opinions]

    if len(opinions) < min_opinions:
        print(f'No se encontraron suficientes opiniones para {model}. Solo se encontraron {len(opinions)} opiniones.')

    return opinions

def analyze_sentiments(opinions):
    """Analiza el sentimiento de cada opinión utilizando VADER."""
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
    """Genera un resumen basado en las opiniones utilizando TextRank."""
    text = " ".join(opinions)
    parser = PlaintextParser.from_string(text, Tokenizer('spanish'))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

models = ['chevrolet/sail', 'volkswagen/gol', 'toyota/hilux']

for model in models:
    opinions = get_opinions(model)
    sentiments = analyze_sentiments(opinions)
    summary = summarize(opinions)
    
    print(f'\nModelo: {model.replace("/", " ").title()}')
    print(f'Opiniones ({len(opinions)}):')
    for opinion in opinions:
        print(f'- {opinion}')
    
    print('\nAnálisis de Sentimientos:')
    for opinion, sentiment_label, sentiment_score in sentiments:
        print(f'- Opinión: {opinion} | Sentimiento: {sentiment_label} ({sentiment_score})')
    
    print(f'\nResumen:')
    print(summary)
