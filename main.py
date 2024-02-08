import argparse
import yaml
import os
import webbrowser
import uvicorn

# Read the Yaml configuration file
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Argparser
parser = argparse.ArgumentParser(
    description="Noodle: Crawler, Indexer, and Search Engine."
)
parser.add_argument("-c", "--crawler", action="store_true", help="Run Crawler")
parser.add_argument("-i", "--indexer", action="store_true", help="Run Indexer")
parser.add_argument("-r", "--ranker", action="store_true", help="Run Ranker")
parser.add_argument("-w", "--web", action="store_true", help="Run Web Search Engine")
args = parser.parse_args()


if args.crawler:
    from backend.crawler import Crawler

    crawler_config = config["crawler-config"]
    crawler = Crawler(
        base_url=crawler_config["base-url"],
        max_urls=crawler_config["max-urls"],
        n_threads=crawler_config["n-threads"],
        politeness_delay=crawler_config["politeness-delay"],
        max_url_per_page=crawler_config["max-url-per-page"],
    )
    crawler.crawl()
    crawler.save_visited_urls(config["pages-file"])


elif args.indexer:
    from backend.indexer import Indexer

    indexer_config = config["indexer-config"]
    indexer = Indexer(
        lem_model=indexer_config["lem-model"],
        limit=indexer_config["limit"],
    )
    indexer.run(
        input_file=indexer_config["input-file"],
        output_dir=indexer_config["output-dir"],
        fields=indexer_config["fields"],
        use_pos=indexer_config["use-pos"],
        use_stem=indexer_config["use-stem"],
    )


elif args.ranker:
    # Run the ranker demo
    pass

elif args.web:
    # Open the frontend in the default web browser
    cwd = os.getcwd()
    webbrowser.open(cwd + "/frontend/index.html")
    uvicorn.run("backend.api:app")

else:
    # Display the help message if no argument is provided
    parser.print_help()
