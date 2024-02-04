import spacy
import logging
from utils.singleton import Singleton

class Lemmatizer(metaclass=Singleton):
   def __init__(self, model="fr_core_news_sm"):
      """
      This function initializes the Preprocessor class.
      """
      # Check if the SpaCy model is installed
      if not spacy.util.is_package(model):
         logging.info(f"Downloading {model} model ...")
         spacy.cli.download(model)

      # Load the SpaCy model
      logging.info(f"Loading {model} model ...")
      self.nlp = spacy.load(model)

   def __call__(self, documents):
      """
      This function is called when the class is called. It removes the stopwords and lemmatizes the text.
      """
      # Create a Doc object and generate lemmas
      # Use nlp.pipe for efficient processing
      processed_docs = []
      for doc in self.nlp.pipe(documents, disable=["parser", "ner"], batch_size=32):
         # Generate lemmas, remove stopwords, and filter non-alphabetic characters
         lemmas = [token.lemma_.lower() for token in doc if token.lemma_.isalpha() and not token.is_stop]
         processed_docs.append(lemmas)

      return processed_docs