# Noodle: Crawler, Indexer, and Search Engine

Noodle is a versatile tool designed for crawling, indexing, and searching web content. With its modular architecture, Noodle offers a seamless workflow from fetching web pages to indexing their contents and providing a simple web search engine interface.

## Features

- **Crawler**: Fetch web pages from a specified base URL and save them locally. Supports multi-threading and politeness delay to respect server guidelines.
  
- **Indexer**: Index crawled web pages to facilitate quick and efficient search. Options include lemmatization, part-of-speech tagging, and stemming for enhanced search accuracy.
  
- **Ranker**: Provide ranked search results based on relevance to the user query. Utilizes indexing information to deliver accurate and meaningful results.
  
- **Web Search Engine**: Deploy a web-based search engine interface for users to interact with indexed content conveniently.

## Installation

Install the required dependencies using pip:

```
pip install -r requirements.txt
```

## Usage

### Running the Crawler

To start crawling web pages, run:

```
python main.py -c
```

This command initiates the crawler using configurations specified in `config.yml`. Crawled URLs are saved to the specified `pages-file`.

### Running the Indexer

Index the crawled URLs to enable efficient search:

```
python main.py -i
```

The indexer utilizes configurations from `config.yml` to process crawled data. Indexed information is saved in the specified output directory.

### Running the Ranker

To perform searches and retrieve ranked results:

```
python main.py -r
```

The ranker utilizes indexing information to deliver relevant search results. Users can input queries interactively.

### Running the Web Search Engine

Deploy the web-based search engine interface:

```
python main.py -w
```

This command opens the frontend interface in the default web browser, allowing users to search indexed content interactively.

## Configuration

Modify `config.yml` to adjust crawler, indexer, and ranker configurations according to your requirements. This file contains settings such as base URLs, politeness delay, indexing options, and more.

For detailed instructions on configuration options, refer to the comments within `config.yml`.
