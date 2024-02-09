import pytest
from backend.crawler import Crawler  # Assuming your crawler class is defined in crawler.py


@pytest.fixture
def crawler_instance():
    # Initialize a crawler instance with mock data
    base_url = "http://example.com"
    max_urls = 5
    n_threads = 3
    politeness_delay = 3
    max_url_per_page = None
    return Crawler(base_url, max_urls, n_threads, politeness_delay, max_url_per_page)


def test_add_url_to_crawl(crawler_instance):
    # Test the add_url_to_crawl method
    url = "http://example.com/page1"
    crawler_instance.add_url_to_crawl(url)
    assert url in crawler_instance.urls_to_crawl


def test_parse_robots(crawler_instance):
    # Test the parse_robots method
    url = "http://example.com"
    assert crawler_instance.parse_robots(url) is True  # Assuming the default behavior is to allow crawling


def test_parse_page(crawler_instance):
    # Test the parse_page method
    url = "http://example.com"
    crawler_instance.parse_page(url)
    assert url in crawler_instance.visited_urls


def test_save_visited_urls(crawler_instance, tmp_path):
    # Test the save_visited_urls method
    json_file = tmp_path / "visited_urls.json"
    crawler_instance.visited_urls = {"http://example.com": {"title": "Example", "content": "Hello"}}
    crawler_instance.save_visited_urls(json_file)
    assert json_file.is_file()  # Check if the JSON file is created


if __name__ == "__main__":
    pytest.main()