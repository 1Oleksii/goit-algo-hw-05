class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]  # Ініціалізуємо список списків для хеш-таблиці

    def hash_function(self, key):
        return hash(key) % self.size  # Обчислюємо хеш ключа

    def insert(self, key, value):
        key_hash = self.hash_function(key)  # Отримуємо індекс таблиці
        key_value = [key, value]  # Створюємо пару ключ-значення

        for pair in self.table[key_hash]:  # Перевіряємо чи ключ вже існує
            if pair[0] == key:
                pair[1] = value  # Оновлюємо значення
                return True

        self.table[key_hash].append(key_value)  # Додаємо нову пару
        return True

    def get(self, key):
        key_hash = self.hash_function(key)  # Отримуємо індекс таблиці
        for pair in self.table[key_hash]:  # Шукаємо пару за ключем
            if pair[0] == key:
                return pair[1]  # Повертаємо значення
        return None  # Якщо не знайдено

    def delete(self, key):
        key_hash = self.hash_function(key)  # Отримуємо індекс таблиці
        for i, pair in enumerate(self.table[key_hash]):  # Проходимо по кожній парі
            if pair[0] == key:
                del self.table[key_hash][i]  # Видаляємо пару за індексом
                return True  # Повертаємо True при успішному видаленні
        return False  # Якщо ключ не знайдено

# Тестуємо нашу хеш-таблицю:
H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print(H.get("apple"))   # Виведе: 10
print(H.get("orange"))  # Виведе: 20
print(H.get("banana"))  # Виведе: 30

H.delete("orange")      # Видаляємо "orange"
print(H.get("orange"))  # Виведе: None (бо елемент видалено)
