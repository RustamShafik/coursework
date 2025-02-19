# Анализ финансовых операций

### Автор: Рустам Шафиков

Этот проект предназначен для анализа финансовых операций, загруженных из Excel-файла. Он предоставляет возможность поиска транзакций, фильтрации данных по дате, расчета данных по картам, получения курсов валют и цен на акции, а также формирования дашборда с ключевой информацией.

## Структура проекта

Проект состоит из следующих файлов:

- **main.py**: Основной скрипт для поиска транзакций по ключевому слову.
- **views.py**: Модуль для загрузки данных, фильтрации, расчета данных по картам, получения курсов валют и цен на акций, а также формирования дашборда.
- **services.py**: Модуль для поиска транзакций по ключевому слову.
- **operations.xlsx**: Excel-файл с данными о транзакциях (должен быть размещен в папке `../` относительно проекта).
- **user_settings.json**: JSON-файл с настройками пользователя (например, список валют и акций для отслеживания).
- **.env**: Файл для хранения API-ключей (например, для получения курсов валют и цен на акции).

## Функциональность

### 1. Загрузка данных
Данные о транзакциях загружаются из Excel-файла (`operations.xlsx`). В процессе загрузки данные преобразуются в нужные форматы (даты, числовые значения).

### 2. Поиск транзакций
Реализована возможность поиска транзакций по ключевому слову в описании или категории. Результат возвращается в формате JSON.

### 3. Фильтрация данных по дате
Данные можно отфильтровать по диапазону дат (с 1-го числа месяца до указанной даты).

### 4. Расчет данных по картам
Для каждой карты рассчитывается:
- Общая сумма расходов.
- Кэшбэк (1% от суммы расходов).

### 5. Получение курсов валют
Используя внешний API, проект получает текущие курсы валют относительно рубля. Список валют задается в `user_settings.json`.

### 6. Получение цен на акции
Используя внешний API, проект получает текущие цены на акции. Список акций задается в `user_settings.json`.

### 7. Формирование дашборда
Функция `get_dashboard_data` формирует JSON-структуру с данными для дашборда, включая:
- Приветствие (в зависимости от времени суток).
- Данные по картам.
- Топ-5 транзакций по сумме.
- Курсы валют.
- Цены на акции.

## Как использовать

### Установка зависимостей
Убедитесь, что у вас установлены необходимые библиотеки. Для установки выполните:

```bash
pip install pandas requests python-dotenv