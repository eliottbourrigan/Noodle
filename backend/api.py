from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.ranker import Ranker
import yaml


max_lengths = {
    'title': 50,
    'url': 30,
    'content': 100
}

# Read the Yaml configuration file
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

ranker_config = config["ranker-config"]
ranker = Ranker(
    pages_file=ranker_config["pages-file"],
    fields=ranker_config["fields"],
    lem_model=ranker_config["lem-model"]
)

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify specific origins instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
async def search(query: str):
    pages = ranker.run(query)
    # Shorten the content of the pages to match max_lengths
    for page in pages:
        for field in max_lengths.keys():
            if len(page[field]) > max_lengths[field]:
                page[field] = page[field][:max_lengths[field]] + "..."
    return pages
