import redis
import numpy as np

class RedisNumpyStorage:
    def __init__(self, host='localhost', port=6379, db=0):
        # Подключение к Redis
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def save_numpy_array(self, key, array):
        """
        Сохранение NumPy массива в Redis
        
        :param key: Ключ для хранения массива
        :param array: NumPy массив для сохранения
        """
        # Сериализация массива в байты
        serialized_array = array.tobytes()
        
        # Сохранение метаданных массива
        self.redis_client.hset(key, mapping={
            'dtype': str(array.dtype),
            'shape': str(array.shape),
            'data': serialized_array
        })

    def load_numpy_array(self, key):
        """
        Загрузка NumPy массива из Redis
        
        :param key: Ключ для загрузки массива
        :return: NumPy массив или None, если ключ не найден
        """
        # Получение метаданных массива
        data = self.redis_client.hgetall(key)
        
        if not data:
            return None
        
        # Десериализация массива
        dtype = np.dtype(data[b'dtype'].decode())
        shape = eval(data[b'shape'].decode())
        
        # Восстановление массива
        array = np.frombuffer(data[b'data'], dtype=dtype).reshape(shape)
        
        return array

    def delete_numpy_array(self, key):
        """
        Удаление массива из Redis
        
        :param key: Ключ для удаления
        """
        self.redis_client.delete(key)

# Пример использования
def main():
    # Создание экземпляра хранилища
    storage = RedisNumpyStorage()

    # Загрузка embeddings
    embeddings = np.load('../query.npy')

    # Сохранение в Redis
    storage.save_numpy_array('query_embeddings', embeddings)

    # Загрузка из Redis
    loaded_embeddings = storage.load_numpy_array('query_embeddings')

    # Проверка, что массивы идентичны
    print("Массивы идентичны:", np.array_equal(embeddings, loaded_embeddings))

    # Опционально: удаление
    # storage.delete_numpy_array('query_embeddings')

if __name__ == '__main__':
    main()
