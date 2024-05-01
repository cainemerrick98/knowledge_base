import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def preprocess_text(content: str):
    """
    Called to preprocess the document content and the query string before saving to the database.
    Sets to lower case, removes the punctuation and stopwords.
    """
    tokens =  word_tokenize(content.lower())

    punctuation = string.punctuation + "\u2019"
    tokens = [token for token in tokens if token not in punctuation]
    
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    return ' '.join(tokens)


