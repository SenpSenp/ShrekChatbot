import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    sentences = sent_tokenize(text, language='portuguese')
    stop_words = set(stopwords.words('portuguese'))
    return sentences, stop_words

def create_tfidf_vectorizer(stop_words):
    return TfidfVectorizer(stop_words=list(stop_words))
