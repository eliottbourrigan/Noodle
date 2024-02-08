import json
import spacy
import time
from threading import Thread
from nltk.stem import SnowballStemmer
from backend.lemmatizer import Lemmatizer


class Indexer:
    def __init__(self, lem_model="fr_core_news_sm", stem_model="french", limit=None):
        """
        This function initializes the Indexer class.
        """
        self.limit = limit

        # Check if the SpaCy model is installed
        if not spacy.util.is_package(lem_model):
            print(f"Downloading {lem_model} model ...")
            spacy.cli.download(lem_model)

        # Load the SpaCy model
        print(f"Loading {lem_model} model ...")
        self.nlp = spacy.load(lem_model)

        # Load the stemmer
        if stem_model:
            self.stemmer = SnowballStemmer(stem_model)

    def run(self, input_file, output_dir, fields, use_pos=False, use_stem=False):
        """
        This function indexes the crawled webpages and saves the indexs in the output directory.
        """
        print(f"Opening {input_file}...")
        # Parse JSON file
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if self.limit:
            data = data[: self.limit]

        # Indexing the webpages
        starting_time = time.time()
        avg_tokens_per_field = {}
        for field in fields:
            # Lemmatize the content of the field
            print(f"Lemmatizing {field}...")
            lemma_docs = self.lemmatize([page[field] for page in data])

            # Stem the lemmatized content
            if self.stemmer:
                for i, doc in enumerate(lemma_docs):
                    lemma_docs[i] = [self.stemmer.stem(token) for token in doc]

            # Create the index
            print(f"Creating index for {field}...")
            index = self.create_index(lemma_docs, use_pos)

            # Saving the index
            print(f"Saving index for {field}...")
            prefix = "pos_" if use_pos else "non_pos_"
            filename = f"{output_dir}/{field}.{prefix}index.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(index, f, ensure_ascii=False)

            avg_tokens_per_field[field] = sum([len(doc) for doc in lemma_docs]) / len(
                lemma_docs
            )

        # Saving statistics
        statistics = {
            "n_docs": len(lemma_docs),
            "n_total_tokens": len(index),
            "avg_tokens_per_doc": avg_tokens_per_field,
        }
        output_file = f"{output_dir}/metadata.json"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(json.dumps(statistics, ensure_ascii=False))
        print(f"Indexing completed in {time.time() - starting_time} seconds.")

    def lemmatize(self, docs):
        """
        This function lemmatizes a list of documents.
        """
        docs = list(self.nlp.pipe(docs, disable=["parser", "ner"]))
        lemma_docs = []
        for i, doc in enumerate(docs):
            lemma_docs.append([])
            for token in doc:
                if token.is_alpha and not token.is_stop:
                    lemma_docs[i].append(token.lemma_.lower())
        return lemma_docs

    @staticmethod
    def create_index(docs, use_pos):
        """
        This function creates an index from a list of documents.
        """
        index = {}
        for i, doc in enumerate(docs):
            for j, lemma in enumerate(doc):
                # Non-positional index
                if not use_pos:
                    if not lemma in index:
                        index[lemma] = []
                    index[lemma].append(i)

                # Positionnal index
                if use_pos:
                    if not lemma in index:
                        index[lemma] = {}
                    if not i in index[lemma]:
                        index[lemma][i] = []
                    index[lemma][i].append(j)
        return index
