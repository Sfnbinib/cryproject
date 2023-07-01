from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet






def generate_symmetric_key():                               # Генерация ключа для симметричного шифрования
    key = Fernet.generate_key()
    return key

def generate_asymmetric_keys():                             # Генерация ключей для асимметричного шифрования
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def symmetric_encrypt(data, key):                            # Функция для шифрования данных с помощью ключа
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def symmetric_decrypt(encrypted_data, key):                   # Функция для расшифрования данных с помощью ключа
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()

def asymmetric_encrypt(data, public_key):                     #  Функция для шифрования данных с использованием публичного ключа
    encrypted_data = public_key.encrypt(data.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return encrypted_data

def asymmetric_decrypt(encrypted_data, private_key):          #  Функция для расшифрования данных с использованием приватного ключа
    decrypted_data = private_key.decrypt(encrypted_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return decrypted_data.decode()







def hash_data(data):                                          # Функция для хеширования данных с использованием SHA256
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data.encode())
    hashed_data = digest.finalize()
    return hashed_data.hex()







def text_editor():                                             # Функции для текстового редактора
    symmetric_key = generate_symmetric_key()                   # Генерация ключа для симметричного шифрования
    private_key, public_key = generate_asymmetric_keys()       # Генерация ключей для асимметричного шифрования(public, private)

    while True:
        print("1. Ввести текст")
        print("2. Расшифровать")
        print("3. Выйти")

        choice = input("Выберите действие: ")




        if choice == "1":                                      # Функция с выбором действия
            text = input("Введите текст: ")                    # Сохранение текста в переменую 'text'
            encrypted_text = symmetric_encrypt(text, symmetric_key)         # Шифрование текста
            encrypted_key = asymmetric_encrypt(symmetric_key, public_key)   # Шифрование симметричного ключа с использованием публичного ключа
            hashed_text = hash_data(text)                                   # Хеширование текста

            with open("encrypted_data.txt", "wb") as file:                  # Сохранение зашифрованного текста, зашифрованного ключа и хеша в файл
                file.write(encrypted_text)
                file.write(encrypted_key)
                file.write(hashed_text.encode())

            print("Текст сохранен")

        elif choice == "2":
            try:
                with open("encrypted_data.txt", "rb") as file:              # Загрузка зашифрованных данных из файла
                    encrypted_text = file.read(128)
                    encrypted_key = file.read(256)
                    hashed_text = file.read().decode()

                decrypted_key = asymmetric_decrypt(encrypted_key, private_key)
                decrypted_text = symmetric_decrypt(encrypted_text, decrypted_key)

                if hash_data(decrypted_text) == hashed_text:
                    print("Текст:", decrypted_text)
                else:
                    print("Неверность целостности данных")

            except FileNotFoundError:                                       # Функция ошибки файла
                print("Файл с зашифрованными данными не найден")

        elif choice == "3":
            print("Удачи!")
            break


# 1) Запустите программу
# 2) Выберете следующую команду:
#     1. Ввести текст
#     2. Расшифровать
#     3. Выйти
# 3)Примечание: Если у вас не установлена библиотека cryptography, вы можете установить ее с помощью инструмента управления пакетами Python.
#     (pip install cryptography)
#
#
#
# О прoграмме:
# Программа - текстовой редактор с возможностью шифрования, расшифровки и хеширования данных.
#
# 1) Ввести текст: Позволяет пользователю ввести текст для сохранения.
#     Текст шифруется с использованием симметричного шифрования.
#     Симметричный ключ, используемый для шифрования, генерируется.
#     Симметричный ключ шифруется с использованием асимметричного шифрования с публичным ключом.
#     Введенный текст также хешируется для обеспечения целостности данных.
#     Зашифрованный текст, зашифрованный ключ и хеш сохраняются в файл.
#
# 2) Расшифровать: Позволяет пользователю расшифровать ранее сохраненные данные.
#     Программа пытается загрузить зашифрованные данные из файла.
#     Зашифрованный текст, зашифрованный ключ и хеш считываются из файла.
#     Зашифрованный ключ расшифровывается с использованием приватного ключа.
#     Расшифрованный ключ используется для расшифровки зашифрованного текста.
#     Расшифрованный текст сравнивается с хешем, чтобы проверить целостность данных.
#     Если хеши совпадают, расшифрованный текст выводится на экран.
#
# 3) Выйти: Завершает программу.

