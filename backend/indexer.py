import json
import time
from utils.preprocessor import Lemmatizer
from threading import Thread

class Indexer:
   def __init__(self, model="fr_core_news_sm", output_dir="output", limit=None):
      """
      This function initializes the Indexer class.
      """
      self.tokens = {} # {token: [count_webpage_1, count_webpage_2, ...]}
      self.field_counter = {} # {field: token_count}
      self.webpage_counter = [] # [token_count_1, token_count_2, ...]
      self.preprocessor = Preprocessor(model = model)
      self.output_dir = output_dir
      self.limit = limit

   def index(self, input_file):
      """
      This function indexes the crawled webpages.
      """
      print(f"Opening {input_file}...")
      # Parse JSON file
      with open(input_file, "r", encoding="utf-8") as f:
         data = json.load(f)

      # Limiting the number of webpages
      if self.limit:
         data = data[:self.limit]

      # Counting the number of webpages
      self.nb_webpages = len(data)
      print(f"{self.nb_webpages} webpages found.")

      # Indexing the webpages
      starting_time = time.time()
      for field in ["title"]:
         self.field_counter[field] = 0
         # Lemmatize the content of the field
         webpages = self.preprocessor([webpage[field] for webpage in data]) 
         for i, webpage in enumerate(webpages):
            for token in set(webpage):
               if not token in self.tokens:
                  self.tokens[token] = []
               self.tokens[token].append(i)
            self.field_counter[field] += len(webpage)
      print(f"Indexing completed in {time.time() - starting_time} seconds.")
      
   def save_results(self):
      """
      This function saves the results in the output directory.
      """
      # Saving tokens
      print(f"Saving tokens in {self.output_dir}/tokens.json ...")
      with open(self.output_dir + "/tokens.json", "w") as f:
         json.dump(self.tokens, f, indent=2)

      # Saving statistics
      print(f"Saving statistics in {self.output_dir}/metadata.json ...")
      statstics = {
         "nb_webpages": self.nb_webpages,
         "nb_tokens": len(self.tokens),
         "avg_tokens_per_field": {field: self.field_counter[field] / self.nb_webpages for field in self.field_counter}
      }
      with open(self.output_dir + "/metadata.json", "w") as f:
         json.dump(statstics, f, indent=2)