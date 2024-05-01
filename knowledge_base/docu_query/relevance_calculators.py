from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BaseRelevanceCalculator:

    def calculate_relevance(self, documents:list[dict], query:str) -> float:
        raise NotImplementedError("Subclasses must implement calculate_relevance method.")
    
    def get_corpus(self, documents) -> list[str]:
        """
        Extracts the corpus from each document in the queryset
        """
        #Could change the view so that a user defined model field can be used as the content field
        corpus = documents.values_list('content', flat=True)

        if len(corpus) == 0:
            raise ValueError('No documents in the database')
        return corpus

class TFIDFCosineSimilarityCalculator(BaseRelevanceCalculator):
    
    def calculate_relevance(self, documents:list[dict], query: str) -> list[float]:
        """
        Calculates the cosine similarity between the TFIDF of the document content
        and the query for each document in the database. Sets the relevance score
        on the document.
        """
        vectorizer = TfidfVectorizer()
        corpus = self.get_corpus(documents)
        vectorizer.fit(corpus)

        for document in documents:
            doc_tdidf = vectorizer.transform([document.content])
            query_tfidf = vectorizer.transform([query])
            score = cosine_similarity(query_tfidf, doc_tdidf)[0,0]
            document.set_relevance_score(score)
        
        return documents

class TFIDFNgramCosineSimilarityCalculator(BaseRelevanceCalculator):

    def calculate_relevance(self, documents: list[dict], query: str) -> list[float]:
        """
        Calculates the cosine similarity between the TFIDF for 1-3 word ngrams  
        of the document content and the query for each document in the database. 
        Sets the relevance score on the document
        """
        vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        corpus = self.get_corpus(documents)
        vectorizer.fit(corpus)

        for document in documents:
            doc_tdidf = vectorizer.transform([document.content])
            query_tfidf = vectorizer.transform([query])
            score = cosine_similarity(query_tfidf, doc_tdidf)[0,0]
            document.set_relevance_score(score)

        return documents

