import argparse
import yaml
import os
import webbrowser
import uvicorn

# Read the Yaml configuration file
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
    print(config)

# Argparser
parser = argparse.ArgumentParser(description="Description de votre programme")
parser.add_argument("-c", "--crawler", action="store_true", help="Run Crawler Demo")
parser.add_argument("-i", "--indexer", action="store_true", help="Run Indexer Demo")
parser.add_argument("-r", "--ranker", action="store_true", help="Run Ranker Demo")
parser.add_argument("-w", "--web", action="store_true", help="Run Web Search Engine Demo")
args = parser.parse_args()

# Run the different demos based on the arguments
if args.crawler:
    # Run the crawler demo
    from backend.crawler import crawler_demo
    crawler_config = config['crawler-config']
    crawler_demo(crawler_config)

if args.indexer:
    # Run the indexer demo
    from backend.indexer import indexer_demo
    indexer_config = config['indexer-config']
    indexer_demo(indexer_config)

if args.ranker:
    # Run the ranker demo
    from backend.ranker import ranker_demo
    ranker_config = config['ranker-config']
    ranker_demo(ranker_config)

if args.engine:
    # Open the frontend in the default web browser
    cwd = os.getcwd()
    webbrowser.open(cwd + '/frontend/index.html')
    uvicorn.run("backend.api:app")

else:
    # Display the help message if no argument is provided
    parser.print_help()