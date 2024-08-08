import pytest

from books_collector import BooksCollector


@pytest.fixture(scope="function")
def collector():
    collector = BooksCollector()
    return collector
