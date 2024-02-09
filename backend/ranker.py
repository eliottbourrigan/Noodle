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
