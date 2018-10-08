## Тестовое задание
Даны 3 генератора src_a, src_b, src_c. Каждый из них при итерации возвращает словарь вида:
{'<str_key>': <some_int_value>}
где в ключе будет str, а в значении int. В каждом таком словаре всегда один ключ. 
Необходимо посчитать сумму всех значений для каждого ключа так, чтобы на выходе получился словарь вида:
```python
{
    'key_1': 123,
    'key_2': 489,
    'key_3': 900
}
```
со всеми возможными ключами и суммами их значений. Количество различных ключей и их названия заранее неизвестны.


### Настройка и запуск:
* Подготовить окружение с помощью requirements.txt и активировать его
* Запуск: `pytest test.py `
* Время выполнения каждого теста: `pytest test.py --duration=0 | grep call`