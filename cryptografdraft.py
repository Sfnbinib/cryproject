from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def generate_asymmetric_keys():                            # Генерация ключей для асимметричного шифрования

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def asymmetric_encrypt(data, public_key):                  # Функция для шифрования данных с использованием публичного ключа

    encrypted_data = public_key.encrypt(data.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return encrypted_data

def asymmetric_decrypt(encrypted_data, private_key):       # Функция для расшифрования данных с использованием приватного ключа
    decrypted_data = private_key.decrypt(encrypted_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return decrypted_data.decode()








def hash_data(data):                       # Функция для хеширования данных с использованием SHA256
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data.encode())
    hashed_data = digest.finalize()
    return hashed_data.hex()






def text_editor():                                  # Функции для текстового редактора

    symmetric_key = generate_symmetric_key()        # Генерация ключа для симметричного шифрования

    private_key, public_key = generate_asymmetric_keys()    # Генерация ключей для асимметричного шифрования


    while True:
        print("1. Ввести текст")
        print("2. Расшифроввать")
        print("3. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            text = input("Введите текст: ")         # Сохранение текста в переменую 'text'


            encrypted_text = symmetric_encrypt(text, symmetric_key)        # Шифрование текста


            encrypted_key = asymmetric_encrypt(symmetric_key, public_key)   # Шифрование симметричного ключа с использованием публичного ключа


            hashed_text = hash_data(text)       # Хеширование текста


            with open("encrypted_data.txt", "wb") as file:      # Сохранение зашифрованного текста, зашифрованного ключа и хеша в файл
                file.write(encrypted_text)
                file.write(encrypted_key)
                file.write(hashed_text.encode())

            print("Текст сохранен")

        elif choice == "2":
            try:

                with open("encrypted_data.txt", "rb") as file:      # Загрузка зашифрованных данных из файла
                    encrypted_text = file.read(128)
                    encrypted_key = file.read(256)
                    hashed_text = file.read().decode()

        elif choice == "3":
            print("Удачи!")


