# Проект парсинг документов PEP

Автор - 
*   [Клавдия Дунаева](https://www.t.me/klodunaeva)


**4 парсера:**

* whats-new:

Собирает ссылки на статьи о нововведениях в Python,
переходит по ним и забирает информацию об авторах и редакторах статей.
* latest-versions:

Собирает информацию о статусах версий Python.
* download:

Скачивает архив с актуальной документацией.
* pep:

Парсинг документов PEP. Сравнение статусов в таблице, со статусом в карточке, 
подсчет и вывод в csv файл общего количества PEP, а также количества по статусам.

Настроено логирование и обработка исключений.
Функции программы и режимы парсера запускаются через аргументы командной строки.

**Инструменты и стек:**

Python 3.7+, 
[requests-cache](https://requests-cache.readthedocs.io/en/latest/user_guide.html),
[tqdm](https://github.com/tqdm/tqdm),
[BeautifulSoup 4](https://beautiful-soup-4.readthedocs.io/en/latest/#), 
[PrettyTable 3.8.0](https://pypi.org/project/prettytable/),


**Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/KlavaD/bs4_parser_pep
```

```
cd src
```

Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Обновить pip:

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

В командной строке:

Нововведения, заголовки и авторы в файл: 
```
python main.py whats-new --output file
```
Статусы и количество PEP в файл:
```
python main.py pep -o file
```
Ссылка на документацию, версия, статус в "красивую" таблицу: 
```
python main.py latest-versions --output pretty
```
Скачать документацию в архив zip: 
```
python main.py download --output pretty
```
... в файл с очисткой кеша: 
```
python main.py ... --output file -c
```
Получить справку о командах: 
```
python main.py -h
```