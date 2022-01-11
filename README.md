# welltory_challenge
Тестовый проект на позицию Python Developer in Data science

## Требования

* `docker-compose version 1.29.2, build 5becea4c`
* `docker version 20.10.12`

## Запуск тестов и сервера

```bash
docker-compose up --build
```

Команда выполнит два теста:
* `request_test.py` проверяет работоспособность методов API (коды возврата методов)
* `pearson_test.py` проверяет свойства коэффициента корреляции

API запускается на порте `5336`.

[Web-интерфейс к API](http://127.0.0.1:5336/docs)
