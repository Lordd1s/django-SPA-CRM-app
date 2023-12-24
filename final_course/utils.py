from newsapi import NewsApiClient
from django.core.cache import caches
from django.db.models import Model


res_401 = "Данные не были предоставлены (JWT)"


def news():
    # Init
    newsapi = NewsApiClient(api_key="961c9acd6b784b64b7391496c61cd5f8")

    top_headlines = newsapi.get_top_headlines(
        language="en",
        country="us",
    )
    return top_headlines


if __name__ == "__main__":
    news()


cache = caches["default"]


class CustomCache:
    """Кеширование данных."""

    @staticmethod
    def caching(key: str, query_params: dict, model: Model, timeout: int = 1) -> any:
        """
        Попытка взять или записать кэш (Для оптимизации запросов БД).

        :param key: str: Ключ для получения или записывания кэша
        :param query_params: dict: Параметры для модели ({"name": "John", "age": 28})
        :param model: Model: Ваша модель (models.Model_Name / ModelName)
        :param timeout: int: Время жизней кэша
        :return Кэшированный объект
        """

        data = cache.get(key)
        if data is None:
            # Замените следующую строку на выполнение запроса к базе данных с использованием query_params
            # Например, используйте Django ORM или Raw SQL, в зависимости от вашего кода
            data = model.objects.filter(**query_params).values()
            cache.set(key, data, timeout=timeout)
        return data

    @staticmethod
    def clear_cache(key: str) -> any:
        """Очистка кэша."""
        cache.set(key, None, timeout=1)

    @staticmethod
    def set_cache(key: str, data: any, timeout: int = 1):
        cache.set(key, data, timeout=timeout)
        return cache.get(key)

    @staticmethod
    def get_cache(key: str):
        return cache.get(key)
