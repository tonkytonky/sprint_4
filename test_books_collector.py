from books_collector import BooksCollector
from random import choice


class TestBooksCollector:

    book_name1 = "Гордость и предубеждение и зомби"
    book_name2 = "Что делать, если ваш кот симулирует"
    book_name3 = "Перфорация на перфокартах как искусство"
    book_name_too_long = "VERY_VERY_VERY_VERY_VERY_VERY_VERY_LONG_NAME"
    genres_valid = ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"]
    invalid_genre = "INVALID_GENRE"
    genres_age_rating = ["Ужасы", "Детективы"]
    genres_children = list(set(genres_valid) - set(genres_age_rating))

    def test_add_new_book_add_valid_name(self, collector: BooksCollector):
        """
        Добавление книги в коллекцию. Название допустимой длинны.
        Книга добавлена с пустым жанром.
        """

        collector.add_new_book(name=self.book_name1)
        
        books_genre = collector.get_books_genre()
        assert books_genre[self.book_name1] == ""
        assert len(books_genre) == 1

    def test_add_new_book_add_invalid_name(self, collector: BooksCollector):
        """
        Добавление книги в коллекцию. Название превышает допустимую длину.
        Книга не добавлена.
        """

        collector.add_new_book(name=self.book_name_too_long)

        books_genre = collector.get_books_genre()
        assert len(books_genre) == 0

    def test_set_book_genre_valid_genre(self, collector: BooksCollector):
        """
        Установка жанра из списка допустимых.
        Жанр устанавливается.
        """

        collector.add_new_book(name=self.book_name1)
        genre_valid = choice(self.genres_valid)
        collector.set_book_genre(name=self.book_name1, genre=genre_valid)

        books_genre = collector.get_books_genre()
        assert books_genre[self.book_name1] == genre_valid
    
    def test_set_book_genre_invalid_genre(self, collector: BooksCollector):
        """
        Установка жанра не из списка допустимых.
        Жанр остаётся пустым.
        """

        collector.add_new_book(name=self.book_name1)
        collector.set_book_genre(name=self.book_name1, genre=self.invalid_genre)

        books_genre = collector.get_books_genre()
        assert books_genre[self.book_name1] == ""

    def test_get_book_genre(self, collector: BooksCollector):
        """
        Получение жанра книги по её названию.
        Возвращается установленный по названию книги жанр.
        """

        collector.add_new_book(name=self.book_name1)
        genre_valid = choice(self.genres_valid)
        collector.set_book_genre(name=self.book_name1, genre=genre_valid)

        actual_genre = collector.get_book_genre(name=self.book_name1)
        assert actual_genre == genre_valid

    def test_get_books_with_specific_genre(self, collector: BooksCollector):
        """
        Получение списка книг с заданным жанром. 
        Возвращаются только книги с искомым жанром.
        """
        
        collector.add_new_book(name=self.book_name1)
        collector.add_new_book(name=self.book_name2)
        collector.add_new_book(name=self.book_name3)
        genre_valid1 = self.genres_valid[0]
        genre_valid2 = self.genres_valid[1]
        collector.set_book_genre(name=self.book_name1, genre=genre_valid1)
        collector.set_book_genre(name=self.book_name2, genre=genre_valid1)
        collector.set_book_genre(name=self.book_name3, genre=genre_valid2)

        books = collector.get_books_with_specific_genre(genre=genre_valid1)
        assert len(books) == 2

    def test_get_books_genre(self, collector: BooksCollector):
        """
        Получение коллекции книг.
        Возвращается словарь содержащий "Название книги: жанр"
        """
        
        collector.add_new_book(name=self.book_name1)
        genre_valid = choice(self.genres_valid)
        collector.set_book_genre(name=self.book_name1, genre=genre_valid)

        books_genre = collector.get_books_genre()
        book1_genre = books_genre.get(self.book_name1)
        assert book1_genre is not None
        assert book1_genre == genre_valid

    def test_get_books_for_children(self, collector: BooksCollector):
        """
        Получение книг для детей.
        Возвращаются только книги с жанром без ограничения.
        """
        
        collector.add_new_book(name=self.book_name1)
        collector.add_new_book(name=self.book_name2)
        genre_age_rating = choice(self.genres_age_rating)
        genre_children = choice(self.genres_children)
        collector.set_book_genre(name=self.book_name1, genre=genre_age_rating)
        collector.set_book_genre(name=self.book_name2, genre=genre_children)

        books = collector.get_books_for_children()
        assert len(books) == 1

    def test_add_book_in_favorites_add_book_only_once(self, collector: BooksCollector):
        """
        Добавление в Избранное.
        Книгу можно добавить только один раз.
        """
        
        collector.add_new_book(name=self.book_name1)
        collector.add_book_in_favorites(name=self.book_name1)
        collector.add_book_in_favorites(name=self.book_name1)

        books = collector.get_list_of_favorites_books()
        assert len(books) == 1

    def test_delete_book_from_favorites(self, collector: BooksCollector):
        """
        Удаление из Избранного.
        Удаляется только одно книга.
        """
        
        collector.add_new_book(name=self.book_name1)
        collector.add_new_book(name=self.book_name2)
        collector.add_book_in_favorites(name=self.book_name1)
        collector.add_book_in_favorites(name=self.book_name2)
        collector.delete_book_from_favorites(name=self.book_name1)

        books = collector.get_list_of_favorites_books()
        assert len(books) == 1
        assert self.book_name2 in books
