import json
import spacy
import time
from threading import Thread
from nltk.stem import SnowballStemmer


class Ranker:
    def __init__(
        self, pages_file, fields, lem_model="fr_core_news_sm", stem_model="french"
    ):
        """
        This function initializes the Ranker class.

        :param str pages_file: the path to the file containing the webpages. It must be a JSON file
            containing a list of dictionaries that must contain the "title", "url" and "content" key.
        :param dict fields: a dictionary containing the fields to be used for ranking the webpages.
            The keys are the fields and the values are dictionaries containing the "weight" and "index-file".
        :param str lem_model: the SpaCy model to use for lemmatization.
        :param str stem_model: the Snowball stemmer to use for stemming.

        """
        self.pages_file = pages_file
        self.fields = fields  # {"field": {"weight": weight, "index-file": index-file}}

        # Check if the SpaCy model is installeds
        if not spacy.util.is_package(lem_model):
            print(f"Downloading {lem_model} model ...")
            spacy.cli.download(lem_model)

        # Load the SpaCy model
        print(f"Loading {lem_model} model ...")
        self.nlp = spacy.load(lem_model)

        # Load the stemmer
        if stem_model:
            self.stemmer = SnowballStemmer(stem_model)

    def run(self, query, n_results=10):
        """
        This function ranks the webpages based on the query.

        :param str query: the query to rank the webpages.
        :param int n_results: the number of results to return.
        :return: the ranked webpages.

        """
        # Preprocess the query
        lemma_query = self.preprocess_query([query])

        # Rank the webpages
        ranked_pages = self.rank_pages(lemma_query)
        return ranked_pages[:n_results]

    def preprocess_query(self, query):
        """
        This function lemmatizes and stems the query

        :param str query: the query to preprocess.
        :return: the lemmatized and stemmed query.

        """
        docs = list(self.nlp.pipe(query, disable=["parser", "ner"]))
        lemma_docs = []
        for i, doc in enumerate(docs):
            lemma_docs.append([])
            for token in doc:
                if token.is_alpha and not token.is_stop:
                    lemma_docs[i].append(token.lemma_.lower())

        # Stem the lemmatized content
        if self.stemmer:
            for i, doc in enumerate(lemma_docs):
                lemma_docs[i] = [self.stemmer.stem(token) for token in doc]
        return lemma_docs[0]

    def rank_pages(self, lemma_query):
        """
        This function ranks the webpages based on the query.

        :param list lemma_query: the lemmatized and stemmed query.
        :return: the ranked webpages.

        """
        scores = {}  # {"doc_id": score, ...}

        # Load the index
        for field in self.fields:
            weight = self.fields[field]["weight"]
            index_file = self.fields[field]["index-file"]

            # Load the index file
            with open(index_file, "r", encoding="utf-8") as f:
                index = json.load(
                    f
                )  # {"token": {"doc_id": [pos_1, pos_2, ...], ...}, ...}

            for lemma in lemma_query:
                if lemma in index:
                    for doc_id in index[lemma]:
                        if doc_id not in scores:
                            scores[doc_id] = 0
                        scores[doc_id] += weight * len(index[lemma][doc_id])

        # Sort the webpages based on the scores
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Load the webpages
        with open(self.pages_file, "r", encoding="utf-8") as f:
            pages = json.load(f)

        # Return the ranked webpages
        return [pages[int(doc_id)] for doc_id, _ in sorted_scores]


    @staticmethod
    def retrieve_top_pages(n_pages, query, index):
        """
        This function retrieves the top pages based on the BM25 score.

        :param int n_pages: the number of pages to retrieve.
        :param list query: the query to rank the webpages.
        :param dict index: the inverted index.
        :return: the top pages.

        """

        def bm25_score(query, token_index, page_id, avg_doc_length, k1=1.5, b=0.75):
            """
            This function computes the BM25 score.

            :param list query: the query to rank the webpages.
            :param dict token_index: the inverted index.
            :param str page_id: the page id.
            :param float avg_doc_length: the average document length.
            :param float k1: the k1 parameter.
            :param float b: the b parameter.
            :return: the BM25 score.

            """
            score = 0
            for token in query:
                if token in token_index and page_id in token_index[token]:
                    f = len(token_index[token][page_id])
                    idf = math.log((len(token_index) - f + 0.5) / (f + 0.5) + 1)
                    tf = f * (k1 + 1) / (f + k1 * (1 - b + b * len(token_index[token][page_id]) / avg_doc_length))
                    score += idf * tf
            return score

        avg_doc_length = sum(len(doc) for doc in index.values()) / len(index)
        scores = {}
        for page_id in index.values():
            scores[page_id] = bm25_score(query, index, page_id, avg_doc_length)
        top_pages = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:n_pages]
        return top_pages