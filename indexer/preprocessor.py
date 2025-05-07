from document.models import ExtractedText
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK resources are available
for resource in ['punkt', 'stopwords', 'wordnet']:
    path = 'tokenizers/punkt' if resource == 'punkt' else f'corpora/{resource}'
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource)

class Preprocessor:
    def __init__(self, text):
        self.text = text
        self.tokens = []                # raw tokens after cleaning
        self.normalized_tokens = []     # tokens after stopword removal & lemmatization
        self.stemmed_tokens = []        # tokens after stemming

    def tokenization(self):
        if not self.text or not self.text.strip():
            return []

        contractions = {
            "don't": "do not", "isn't": "is not", "can't": "cannot",
            "i'm": "i am", "he's": "he is", "she's": "she is", "it's": "it is",
            "we're": "we are", "they're": "they are", "you've": "you have",
            "i've": "i have", "we've": "we have", "they've": "they have",
            "wouldn't": "would not", "couldn't": "could not", "shouldn't": "should not"
        }
        url_pattern = r'https?://\S+|www\.\S+'
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

        for raw in self.text.split():
            word = contractions.get(raw.lower(), raw)
            if re.match(url_pattern, word) or re.match(email_pattern, word):
                self.tokens.append(word.lower())
                continue
            clean = word.translate(str.maketrans('', '', string.punctuation))
            clean = ''.join(ch for ch in clean if ch.isalnum() or ch == '-')
            clean = clean.strip().lower()
            if clean:
                self.tokens.append(clean)
        return self.tokens

    def normalize(self):
        if not self.tokens:
            self.tokenization()
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        self.normalized_tokens = []
        for tok in self.tokens:
            if tok in stop_words:
                continue
            lemma = lemmatizer.lemmatize(tok)
            self.normalized_tokens.append(lemma)
        return self.normalized_tokens

    def stem(self):
        if not self.normalized_tokens:
            self.normalize()
        from nltk.stem import PorterStemmer
        stemmer = PorterStemmer()
        self.stemmed_tokens = [stemmer.stem(tok) for tok in self.normalized_tokens]
        return self.stemmed_tokens

    def run_all(self):
        # Full pipeline: tokenization → normalization → stemming
        self.tokenization()
        self.normalize()
        return self.stem()
