# План сравнения HTTP библиотек

## Порядок тестирования эндпоинтов

### 1. Базовые запросы
```
GET https://httpbin.org/get
POST https://httpbin.org/post (с JSON данными)
PUT https://httpbin.org/put (обновление)
DELETE https://httpbin.org/delete
```
**Цель**: Синтаксис базовых операций, простота использования

### 2. Параметры и заголовки
```
GET https://httpbin.org/get?param1=value1&param2=value2
GET https://httpbin.org/headers (кастомные заголовки)
GET https://httpbin.org/user-agent
```
**Цель**: Работа с параметрами запроса и заголовками

### 3. Тело запроса (различные форматы)
```
POST https://httpbin.org/post (JSON)
POST https://httpbin.org/post (form-data)
POST https://httpbin.org/post (raw text)
```
**Цель**: Отправка данных в разных форматах

### 4. Аутентификация
```
GET https://httpbin.org/basic-auth/user/pass
GET https://httpbin.org/digest-auth/auth/user/pass
```
**Цель**: Простота реализации аутентификации

### 5. Cookies
```
GET https://httpbin.org/cookies/set?session=abc123
GET https://httpbin.org/cookies
```
**Цель**: Автоматическое управление cookies

### 6. Обработка ошибок
```
GET https://httpbin.org/status/404
GET https://httpbin.org/status/500
GET https://httpbin.org/status/429
```
**Цель**: Механизмы обработки HTTP ошибок

### 7. Редиректы
```
GET https://httpbin.org/redirect/3
GET https://httpbin.org/redirect-to?url=https://httpbin.org/get
```
**Цель**: Автоматическое следование редиректам

### 8. Таймауты и задержки
```
GET https://httpbin.org/delay/1
GET https://httpbin.org/delay/5 (с таймаутом 3 сек)
```
**Цель**: Настройка таймаутов, обработка медленных запросов

### 9. Стриминг данных
```
GET https://httpbin.org/stream/10
GET https://httpbin.org/bytes/1024
```
**Цель**: Работа с большими объемами данных

### 10. Сжатие
```
GET https://httpbin.org/gzip
GET https://httpbin.org/brotli
```
**Цель**: Автоматическая декомпрессия

### 11. Асинхронность (для поддерживающих)
```
Параллельные запросы к:
GET https://httpbin.org/delay/1
GET https://httpbin.org/delay/2  
GET https://httpbin.org/delay/3
```
**Цель**: Производительность при множественных запросах

### 12. Загрузка файлов
```
POST https://httpbin.org/post (multipart/form-data)
```
**Цель**: Отправка файлов

### 13. Различные форматы ответов
```
GET https://httpbin.org/json
GET https://httpbin.org/xml
GET https://httpbin.org/html
GET https://httpbin.org/image/png
```
**Цель**: Парсинг различных типов контента

### 14. Сессии (где применимо)
```
GET https://httpbin.org/cookies/set?session=test
GET https://httpbin.org/cookies (переиспользование сессии)
```
**Цель**: Управление состоянием между запросами

## Критерии сравнения

### Простота использования
- Количество строк кода для базового запроса
- Читаемость синтаксиса
- Необходимость импортов/зависимостей

### Функциональность
- Автоматическое управление cookies/сессиями
- Встроенная поддержка JSON
- Обработка редиректов
- Декомпрессия

### Производительность  
- Время выполнения синхронных запросов
- Асинхронная производительность
- Память при стриминге

### Обработка ошибок
- Автоматические retry
- Детализация ошибок
- Кастомизация обработки

### Дополнительные возможности
- Мидлвары/интерцепторы
- Валидация SSL
- Прокси поддержка
- Метрики/логирование

## Структура результата
Для каждого теста записывать:
1. Код реализации
2. Время выполнения  
3. Размер кода
4. Особенности поведения
5. Возникшие проблемы
