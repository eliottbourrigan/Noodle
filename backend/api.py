from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from example_results import data

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
async def search():
    for page in data:
        for (key, max_chars) in [("title", 50), ("url", 30), ("content", 100)]:
            if len(page[key]) > max_chars:
                page[key] = page[key][:max_chars] + " ..."
    return data


