# Персональний помічник

Цей проект реалізує систему управління контактами та нотатками, що дозволяє користувачам зберігати, шукати, редагувати та видаляти інформацію в персональній адресній книзі та блокноті нотаток.

Особливістю проекту є його орієнтованість на захист даних, оскільки асистент зберігає дані в зашифрованому форматі, а без приватного ключа відкрити чи перенести їх неможливо.
Це дозволяє використовувати додаток в умовах де безпека даних є обов‘язковою.

## Структура проекту

Проект має наступну структуру каталогів та файлів:

- `src/`: Вихідний код програми.
  - `personal_assistant`: Каталог з файлами пакету
    - `commands/`: Обробники cli команд
      - `contact_commands.py`: визначення команд для роботи з контактами
      - `note_commands.py`: визначення команд для роботи з нотатками
    - `models/`: Моделі даних для представлення бізнес-об'єктів.
      - `contact.py`: Клас `Contact` для управління контактами.
      - `email_address.py`: Клас `EmailAddress` для роботи з електронними адресами.
      - `phone_number.py`: Клас `PhoneNumber` для роботи з телефонними номерами.
      - `address.py`: Клас `Address` для роботи з адресами.
      - `birthday.py`: Клас `Birthday` для роботи з датами народження.
      - `note.py`: Клас `Note` для управління нотатками.
      - `tag.py`: Клас `Tag` для тегування нотаток.
    - `enums/`: Перелічувані типи (enums) використовуються у проекті.
      - `command_types.py`: Enums `Command` та `Entity` для визначення команд в CLI.
      - `entity_type.py`: Enum `EntityType` для визначення типів сутностей.
    - `services/`: Сервіси для логіки обробки даних.
      - `storage`: Модуль для підтримки різних форматів зберігання даних 
      - - `base_storage.py`: Абстрактний клас для створення форматів збереження
      - - `json_storage.py`: Сервіс для збереження в json форматі
      - - `secure_json_storage.py`: Сервіс для збереження в json форматі зашифрованих та підписаних персональним ключем даних
      - - `pickle_storage.py`: Сервіс для збереження в pickle форматі
      - `address_book.py`: Сервіс для управління адресною книгою.
      - `cli_completer.py`: Сервіс для автодоповнення cli команд.
      - `notebook.py`: Сервіс для управління нотатками.
      - `storage_service.py`: Сервіс для зберігання та завантаження даних.  
      - `tag_manager.py`: Сервіс для керуванням тегами
    - `utils/`: Утиліти та допоміжні інструменти.
      - `cli_setup.py`: Допоміжні функції для CLI
      - `decorators.py`: Декоратори
      - `validators.py`: Валідатори для перевірки вхідних даних.
      - `helpers.py`: Допоміжні функції.
      - `key_generator.py`: Додаток для генерування унікального, персонального ключа для шифрування даних
    - `cli.py`: Основний файл CLI інтерфейсу.
    - `main.py`: Основний виконуваний файл для демонстрації використання.
- - `.data/`: Каталог для збереження даних.
- `.env.example`: Приклад файлу .env для збереження налаштувань для секретного ключа
- `requirements.txt`: Файл з залежностями проекту.

## Інсталяція

Для встановлення та запуску проекту виконайте наступні кроки:

## 1. Клонуйте репозиторій:
  ```bash
  git clone https://github.com/sergyinfo/goit-personal-assistant
  cd goit-personal-assistant
  ```

## 2. Створіть та активуйте віртуальне середовище:
   ### Для Linux/MacOS:
    
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

   ### Для Windows:

  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

## 3. Встановіть необхідні залежності:
  ```bash
  pip install -r requirements.txt
  ```

## 4. Згенеруйте секретний ключ для шифрування даних
Увага! Ніколи і нікому не передавайте цей ключ. Він має бути унікальним для кожного працюючого застосунку
що гарантує цілісність та безпеку даних

Створіть файл `.env` в каталозі `src/personal_assistant`

Виконайте наступну команду з кореневого каталогу проекту

  ```bash
  python3 src/personal_assistant/utils/key_generator.py
  ```

Скопіюйте отриманий ключ та збережіть його в файлі `.env`, так щоб він мав наступний вигляд
  ```bash
  SECRET_KEY=your_secret_key_here
  ```

де `your_secret_key_here` - це ключ який ви скопіювали


## 5. Запустіть програму з командного рядка:
  ```bash
  cd src
  python -m personal_assistant
  ```

## 6. Використання

Нижче зазначений перелік підтримуваних команд


| Команда   | Опис                 | Параметри                                                                                            |
|-----------|----------------------|------------------------------------------------------------------------------------------------------|
| contacts  | Керування контактами | -h, --help: show this help message and exit                                                          |
|           |                      | list usage: contacts list [-h]                                                           |
|           |                      |                                                                                                      |
|           |                      | add usage: contacts add [-h] --name NAME [--birthday BIRTHDAY] [--note NOTE]     |
|           |                      |                                                                                                      |
|           |                      | edit usage: contacts edit [-h] --id ID [--name NAME] [--birthday BIRTHDAY] [--note NOTE] |
|           |                      |                                                                                                      |
|           |                      | delete usage: contacts delete [-h] --id ID                                               |
|           |                      |                                                                                                      |
|           |                      | search usage: contacts search [-h] --q Q [--by BY]                                       |
|           |                      |                                                                                                      |
|           |                      | add_phone usage: contacts add_phone [-h] --id ID --phone PHONE                           |
|           |                      |                                                                                                      |
|           |                      | delete_phone usage: contacts delete_phone [-h] --id ID --phone PHONE                     |
|           |                      |                                                                                                      |
|           |                      | add_email usage: contacts add_email [-h] --id ID --email EMAIL                           |
|           |                      |                                                                                                      |
|           |                      | delete_email usage: contacts delete_email [-h] --id ID --email EMAIL                     |
|           |                      |                                                                                                      |
|           |                      | add_address usage: contacts add_address [-h] --id ID --address ADDRESS                   |
|           |                      |                                                                                                      |
|           |                      | delete_address usage: contacts delete_address [-h] --id ID --address ADDRESS             |
|           |                      |                                                                                                      |
|           |                      | add_tag usage: contacts add_tag [-h] --id ID --tag TAG                                   |
|           |                      |                                                                                                      |
|           |                      | delete_tag usage: contacts delete_tag [-h] --id ID --tag TAG                             |
|           |                      |                                                                                                      |
|           |                      | anniversaries usage: contacts anniversaries [-h] [--days DAYS]                           |
| notes     | Керування нотатками  | -h, --help: show this help message and exit                                                          |
|           |                      | add usage: notes add [-h] --content CONTENT [CONTENT ...]                                |
|           |                      |                                                                                                      |
|           |                      | edit usage: notes edit [-h] --id ID --content CONTENT [CONTENT ...]                      |
|           |                      |                                                                                                      |
|           |                      | delete usage: notes delete [-h] --id ID                                                  |
|           |                      |                                                                                                      |
|           |                      | search usage: notes search [-h] [--content CONTENT [CONTENT ...]] [--tag TAG] [--id ID]  |
|           |                      |                                                                                                      |
|           |                      | add_tag usage: notes add_tag [-h] --id ID --tag TAG                                      |
|           |                      |                                                                                                      |
|           |                      | delete_tag usage: notes delete_tag [-h] --id ID --tag TAG                                |
|           |                      |                                                                                                      |
|           |                      | archive usage: notes archive [-h] --id ID                                                |
|           |                      |                                                                                                      |
|           |                      | restore usage: notes restore [-h] --id ID                                                |
|           |                      |                                                                                                      |
|           |                      | view_active usage: notes view_active [-h]                                                |
|           |                      |                                                                                                      |
|           |                      | view_archived usage: notes view_archived [-h]                                            |
|           |                      |                                                                                                      |
|           |                      | view_history usage: notes view_history [-h] --id ID                                      |
