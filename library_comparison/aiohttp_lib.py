import aiohttp
import asyncio
import time
import tempfile
import os
from functools import wraps

# Константа для базового URL
BASE_URL = "https://httpbin.org"

def with_aiohttp_session(func):
    """Декоратор для автоматического создания aiohttp.ClientSession"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await func(session, *args, **kwargs)
    return wrapper

def measure_time_async(func):
    """Декоратор для измерения времени выполнения асинхронной функции"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        execution_time = time.time() - start_time
        return result, execution_time
    return wrapper

# === Асинхронные функции для каждого запроса ===

@measure_time_async
@with_aiohttp_session
async def get_request(session):
    """Асинхронный GET запрос"""
    async with session.get(f'{BASE_URL}/get') as response:
        await response.text()  # Читаем ответ
        return response

@measure_time_async
@with_aiohttp_session
async def post_json_request(session):
    """Асинхронный POST запрос с JSON"""
    post_data = {"name": "test", "value": 123}
    async with session.post(f'{BASE_URL}/post', json=post_data) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def put_request(session):
    """Асинхронный PUT запрос"""
    put_data = {"updated": True}
    async with session.put(f'{BASE_URL}/put', json=put_data) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def delete_request(session):
    """Асинхронный DELETE запрос"""
    async with session.delete(f'{BASE_URL}/delete') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def get_with_params(session):
    """Асинхронный GET с параметрами"""
    params = {"param1": "value1", "param2": "value2"}
    async with session.get(f'{BASE_URL}/get', params=params) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def get_with_headers(session):
    """Асинхронный GET с кастомными заголовками"""
    headers = {
        "Custom-Header": "test-value",
        "Authorization": "Bearer token123"
    }
    async with session.get(f'{BASE_URL}/headers', headers=headers) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def get_user_agent(session):
    """Асинхронный GET с User-Agent"""
    headers = {"User-Agent": "AiohttpTestClient/1.0"}
    async with session.get(f'{BASE_URL}/user-agent', headers=headers) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def post_json(session):
    """Асинхронный POST с JSON данными"""
    json_data = {"key": "value", "number": 42}
    async with session.post(f'{BASE_URL}/post', json=json_data) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def post_form_data(session):
    """Асинхронный POST с form data"""
    form_data = {"field1": "value1", "field2": "value2"}
    async with session.post(f'{BASE_URL}/post', data=form_data) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def post_raw_text(session):
    """Асинхронный POST с raw text"""
    raw_text = "Это просто текстовые данные для отправки"
    headers = {"Content-Type": "text/plain"}
    async with session.post(f'{BASE_URL}/post', data=raw_text, headers=headers) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def basic_auth_request(session):
    """Асинхронная Basic аутентификация"""
    auth = aiohttp.BasicAuth('user', 'pass')
    async with session.get(f'{BASE_URL}/basic-auth/user/pass', auth=auth) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def digest_auth_request(session):
    """Асинхронная Digest аутентификация (aiohttp не поддерживает Digest Auth нативно)"""
    # aiohttp не поддерживает Digest Auth из коробки, делаем обычный запрос для совместимости
    async with session.get(f'{BASE_URL}/get') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def set_cookies_request(session):
    """Асинхронная установка cookies"""
    async with session.get(f'{BASE_URL}/cookies/set?session=abc123') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def get_cookies_request(session):
    """Асинхронное получение cookies через сессию с cookies"""
    # Устанавливаем cookie
    async with session.get(f'{BASE_URL}/cookies/set?session=abc123') as _:
        pass
    # Получаем cookies
    async with session.get(f'{BASE_URL}/cookies') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def error_404_request(session):
    """Асинхронный запрос с 404 ошибкой"""
    async with session.get(f'{BASE_URL}/status/404') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def error_500_request(session):
    """Асинхронный запрос с 500 ошибкой"""
    async with session.get(f'{BASE_URL}/status/500') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def error_429_request(session):
    """Асинхронный запрос с 429 ошибкой"""
    async with session.get(f'{BASE_URL}/status/429') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def redirect_3_request(session):
    """Асинхронный запрос с 3 редиректами"""
    async with session.get(f'{BASE_URL}/redirect/3') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def redirect_to_request(session):
    """Асинхронный редирект на конкретный URL"""
    async with session.get(f'{BASE_URL}/redirect-to?url={BASE_URL}/get') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def no_redirect_request(session):
    """Асинхронный запрос без автоматических редиректов"""
    async with session.get(f'{BASE_URL}/redirect/1', allow_redirects=False) as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def delay_1_request(session):
    """Асинхронный запрос с задержкой 1 секунда"""
    async with session.get(f'{BASE_URL}/delay/1') as response:
        await response.text()
        return response

@measure_time_async
async def delay_5_timeout_request():
    """Асинхронный запрос с задержкой 5 секунд и таймаутом 3 секунды"""
    timeout = aiohttp.ClientTimeout(total=3.0)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f'{BASE_URL}/delay/5') as response:
                await response.text()
                return response
    except asyncio.TimeoutError:
        return None

@measure_time_async
@with_aiohttp_session
async def stream_lines_request(session):
    """Асинхронный стриминг строк"""
    stream_lines = []
    async with session.get(f'{BASE_URL}/stream/10') as response:
        async for line in response.content:
            if line:
                stream_lines.append(line.decode('utf-8'))
    return response, len(stream_lines)

@measure_time_async
@with_aiohttp_session
async def stream_bytes_request(session):
    """Асинхронный стриминг бинарных данных"""
    chunks = []
    async with session.get(f'{BASE_URL}/bytes/1024') as response:
        async for chunk in response.content.iter_chunked(256):
            chunks.append(chunk)
    total_bytes = sum(len(chunk) for chunk in chunks)
    return response, total_bytes

@measure_time_async
@with_aiohttp_session
async def gzip_request(session):
    """Асинхронная GZIP декомпрессия"""
    async with session.get(f'{BASE_URL}/gzip') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def brotli_request(session):
    """Асинхронная Brotli декомпрессия"""
    async with session.get(f'{BASE_URL}/brotli') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def sequential_delays(session):
    """Асинхронные последовательные запросы с задержками"""
    urls = [
        f'{BASE_URL}/delay/1',
        f'{BASE_URL}/delay/2', 
        f'{BASE_URL}/delay/3'
    ]
    results = []
    for url in urls:
        async with session.get(url) as response:
            await response.text()
            results.append(response.status)
    return results

@measure_time_async
@with_aiohttp_session
async def parallel_delays(session):
    """Асинхронные параллельные запросы с задержками"""
    urls = [
        f'{BASE_URL}/delay/1',
        f'{BASE_URL}/delay/2', 
        f'{BASE_URL}/delay/3'
    ]
    
    async def fetch_url(url):
        async with session.get(url) as response:
            await response.text()
            return response.status
    
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

@measure_time_async
@with_aiohttp_session
async def file_upload_request(session):
    """Асинхронная загрузка файла"""
    # Создаём временный файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
        temp_file.write("Это тестовый файл для загрузки\nВторая строка файла")
        temp_file_path = temp_file.name
    
    try:
        data = aiohttp.FormData()
        data.add_field('description', 'Тестовый файл')
        data.add_field('file', 
                      open(temp_file_path, 'rb'),
                      filename='test.txt',
                      content_type='text/plain')
        
        async with session.post(f'{BASE_URL}/post', data=data) as response:
            await response.text()
            return response
    finally:
        os.unlink(temp_file_path)

@measure_time_async
@with_aiohttp_session
async def json_response_request(session):
    """Асинхронный JSON ответ"""
    async with session.get(f'{BASE_URL}/json') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def xml_response_request(session):
    """Асинхронный XML ответ"""
    async with session.get(f'{BASE_URL}/xml') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def html_response_request(session):
    """Асинхронный HTML ответ"""
    async with session.get(f'{BASE_URL}/html') as response:
        await response.text()
        return response

@measure_time_async
@with_aiohttp_session
async def image_response_request(session):
    """Асинхронное PNG изображение"""
    async with session.get(f'{BASE_URL}/image/png') as response:
        await response.read()  # Читаем бинарные данные
        return response

@measure_time_async
@with_aiohttp_session
async def session_operations(session):
    """Асинхронные операции с сессией через один клиент"""
    # Устанавливаем cookie
    async with session.get(f'{BASE_URL}/cookies/set?session=test') as _:
        pass
    
    # Получаем cookies
    async with session.get(f'{BASE_URL}/cookies') as response1:
        await response1.text()
    
    # Добавляем постоянные заголовки
    session.headers.update({'X-Session-Header': 'persistent-value'})
    
    # Запрос с постоянными заголовками
    async with session.get(f'{BASE_URL}/headers') as response2:
        await response2.text()
    
    return response1, response2

# === Асинхронные функции тестирования ===

async def test_basic_requests():
    """1. Базовые запросы - GET, POST, PUT, DELETE"""
    print("\n=== 1. Базовые запросы ===")
    
    response, get_time = await get_request()
    print(f"GET запрос: {response.status}, время: {get_time:.3f}с")
    
    response, post_time = await post_json_request()
    print(f"POST запрос: {response.status}, время: {post_time:.3f}с")
    
    response, put_time = await put_request()
    print(f"PUT запрос: {response.status}, время: {put_time:.3f}с")
    
    response, delete_time = await delete_request()
    print(f"DELETE запрос: {response.status}, время: {delete_time:.3f}с")
    
    return {
        'get_time': get_time,
        'post_time': post_time, 
        'put_time': put_time,
        'delete_time': delete_time
    }

async def test_params_and_headers():
    """2. Параметры и заголовки"""
    print("\n=== 2. Параметры и заголовки ===")
    
    response, params_time = await get_with_params()
    print(f"GET с параметрами: {response.status}, время: {params_time:.3f}с")
    
    response, headers_time = await get_with_headers()
    print(f"Кастомные заголовки: {response.status}, время: {headers_time:.3f}с")
    
    response, ua_time = await get_user_agent()
    print(f"User-Agent: {response.status}, время: {ua_time:.3f}с")
    
    return {
        'params_time': params_time,
        'headers_time': headers_time,
        'ua_time': ua_time
    }

async def test_request_body_formats():
    """3. Тело запроса в различных форматах"""
    print("\n=== 3. Форматы тела запроса ===")
    
    response, json_time = await post_json()
    print(f"JSON данные: {response.status}, время: {json_time:.3f}с")
    
    response, form_time = await post_form_data()
    print(f"Form data: {response.status}, время: {form_time:.3f}с")
    
    response, text_time = await post_raw_text()
    print(f"Raw text: {response.status}, время: {text_time:.3f}с")
    
    return {
        'json_time': json_time,
        'form_time': form_time,
        'text_time': text_time
    }

async def test_authentication():
    """4. Аутентификация"""
    print("\n=== 4. Аутентификация ===")
    
    response, basic_time = await basic_auth_request()
    print(f"Basic Auth: {response.status}, время: {basic_time:.3f}с")
    
    response, digest_time = await digest_auth_request()
    print(f"Digest Auth (fallback): {response.status}, время: {digest_time:.3f}с")
    
    return {
        'basic_time': basic_time,
        'digest_time': digest_time
    }

async def test_cookies():
    """5. Работа с Cookies"""
    print("\n=== 5. Cookies ===")
    
    response, set_cookie_time = await set_cookies_request()
    print(f"Установка cookie: {response.status}, время: {set_cookie_time:.3f}с")
    
    response, get_cookie_time = await get_cookies_request()
    print(f"Получение cookies: {response.status}, время: {get_cookie_time:.3f}с")
    
    # Получаем JSON из ответа
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/cookies/set?session=abc123') as _:
            pass
        async with session.get(f'{BASE_URL}/cookies') as resp:
            data = await resp.json()
            print(f"Cookies в ответе: {data.get('cookies', {})}")
    
    return {
        'set_cookie_time': set_cookie_time,
        'get_cookie_time': get_cookie_time
    }

async def test_error_handling():
    """6. Обработка ошибок"""
    print("\n=== 6. Обработка ошибок ===")
    
    error_time = 0
    try:
        response, error_time = await error_404_request()
        print(f"404 ошибка: {response.status}, время: {error_time:.3f}с")
    except aiohttp.ClientError as e:
        print(f"Исключение 404: {e}")
    
    try:
        response, error_time = await error_500_request()
        print(f"500 ошибка: {response.status}, время: {error_time:.3f}с")
    except aiohttp.ClientError as e:
        print(f"Исключение 500: {e}")
    
    try:
        response, error_time = await error_429_request()
        print(f"429 ошибка: {response.status}, время: {error_time:.3f}с")
    except aiohttp.ClientError as e:
        print(f"Исключение 429: {e}")
    
    return {
        'error_handling_time': error_time
    }

async def test_redirects():
    """7. Редиректы"""
    print("\n=== 7. Редиректы ===")
    
    response, redirect_time = await redirect_3_request()
    print(f"Автоматические редиректы: {response.status}, время: {redirect_time:.3f}с")
    print(f"Финальный URL: {response.url}")
    
    response, redirect_to_time = await redirect_to_request()
    print(f"Редирект на URL: {response.status}, время: {redirect_to_time:.3f}с")
    
    response, no_redirect_time = await no_redirect_request()
    print(f"Без редиректов: {response.status}, время: {no_redirect_time:.3f}с")
    
    return {
        'redirect_time': redirect_time,
        'redirect_to_time': redirect_to_time,
        'no_redirect_time': no_redirect_time
    }

async def test_timeouts():
    """8. Таймауты и задержки"""
    print("\n=== 8. Таймауты ===")
    
    response, delay1_time = await delay_1_request()
    print(f"Задержка 1с: {response.status}, время: {delay1_time:.3f}с")
    
    response, timeout_time = await delay_5_timeout_request()
    if response is None:
        print(f"Таймаут сработал через {timeout_time:.3f}с")
    else:
        print(f"Задержка 5с с таймаутом 3с: {response.status}, время: {timeout_time:.3f}с")
    
    return {
        'delay1_time': delay1_time,
        'timeout_time': timeout_time
    }

async def test_streaming():
    """9. Стриминг данных"""
    print("\n=== 9. Стриминг ===")
    
    (response, stream_lines_count), stream_time = await stream_lines_request()
    print(f"Стриминг 10 строк: {response.status}, время: {stream_time:.3f}с")
    print(f"Получено строк: {stream_lines_count}")
    
    (response, total_bytes), bytes_time = await stream_bytes_request()
    print(f"Бинарные данные: {response.status}, время: {bytes_time:.3f}с, байт: {total_bytes}")
    
    return {
        'stream_time': stream_time,
        'bytes_time': bytes_time
    }

async def test_compression():
    """10. Сжатие"""
    print("\n=== 10. Сжатие ===")
    
    response, gzip_time = await gzip_request()
    print(f"GZIP декомпрессия: {response.status}, время: {gzip_time:.3f}с")
    
    # Получаем JSON для проверки
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/gzip') as resp:
            data = await resp.json()
            print(f"Gzipped: {data.get('gzipped', False)}")
    
    response, brotli_time = await brotli_request()
    print(f"Brotli декомпрессия: {response.status}, время: {brotli_time:.3f}с")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/brotli') as resp:
            data = await resp.json()
            print(f"Brotli compressed: {data.get('brotli', False)}")
    
    return {
        'gzip_time': gzip_time,
        'brotli_time': brotli_time
    }

async def test_parallel_requests():
    """11. Параллельные запросы"""
    print("\n=== 11. Параллельные запросы ===")
    
    sequential_results, sequential_time = await sequential_delays()
    print(f"Последовательно: {sequential_time:.3f}с, результаты: {sequential_results}")
    
    parallel_results, parallel_time = await parallel_delays()
    print(f"Параллельно: {parallel_time:.3f}с, результаты: {parallel_results}")
    
    return {
        'sequential_time': sequential_time,
        'parallel_time': parallel_time
    }

async def test_file_upload():
    """12. Загрузка файлов"""
    print("\n=== 12. Загрузка файлов ===")
    
    response, upload_time = await file_upload_request()
    print(f"Загрузка файла: {response.status}, время: {upload_time:.3f}с")
    
    # Получаем данные ответа
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('description', 'test')
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("test")
            temp_file_path = temp_file.name
        
        try:
            data.add_field('file', open(temp_file_path, 'rb'), filename='test.txt')
            async with session.post(f'{BASE_URL}/post', data=data) as resp:
                response_data = await resp.json()
                files_info = response_data.get('files', {})
                print(f"Файлы в запросе: {list(files_info.keys())}")
        finally:
            os.unlink(temp_file_path)
    
    return {
        'upload_time': upload_time
    }

async def test_response_formats():
    """13. Различные форматы ответов"""
    print("\n=== 13. Форматы ответов ===")
    
    response, json_time = await json_response_request()
    print(f"JSON: {response.status}, время: {json_time:.3f}с")
    
    # Получаем JSON данные для анализа
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/json') as resp:
            json_data = await resp.json()
            print(f"JSON поля: {list(json_data.keys())}")
    
    response, xml_time = await xml_response_request()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/xml') as resp:
            text = await resp.text()
            print(f"XML: {response.status}, время: {xml_time:.3f}с, размер: {len(text)} символов")
    
    response, html_time = await html_response_request()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/html') as resp:
            text = await resp.text()
            print(f"HTML: {response.status}, время: {html_time:.3f}с, размер: {len(text)} символов")
    
    response, image_time = await image_response_request()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/image/png') as resp:
            content = await resp.read()
            print(f"PNG изображение: {response.status}, время: {image_time:.3f}с, размер: {len(content)} байт")
    
    return {
        'json_time': json_time,
        'xml_time': xml_time,
        'html_time': html_time,
        'image_time': image_time
    }

async def test_sessions():
    """14. Сессии"""
    print("\n=== 14. Сессии ===")
    
    (response1, response2), session_time = await session_operations()
    
    print(f"Операции с сессией: время: {session_time:.3f}с")
    
    # Получаем cookies из ответа
    async with aiohttp.ClientSession() as session:
        await session.get(f'{BASE_URL}/cookies/set?session=test')
        async with session.get(f'{BASE_URL}/cookies') as resp:
            data = await resp.json()
            cookies = data.get('cookies', {})
            print(f"Cookies в сессии: {cookies}")
    
    return {
        'session_time': session_time
    }

async def run_all_tests():
    """Асинхронный запуск всех тестов"""
    print("=== ТЕСТИРОВАНИЕ БИБЛИОТЕКИ AIOHTTP (АСИНХРОННО) ===")
    
    all_results = {}
    
    try:
        all_results['basic'] = await test_basic_requests()
        all_results['params'] = await test_params_and_headers()
        all_results['body_formats'] = await test_request_body_formats()
        all_results['auth'] = await test_authentication()
        all_results['cookies'] = await test_cookies()
        all_results['errors'] = await test_error_handling()
        all_results['redirects'] = await test_redirects()
        all_results['timeouts'] = await test_timeouts()
        all_results['streaming'] = await test_streaming()
        all_results['compression'] = await test_compression()
        all_results['parallel'] = await test_parallel_requests()
        all_results['upload'] = await test_file_upload()
        all_results['formats'] = await test_response_formats()
        all_results['sessions'] = await test_sessions()
        
    except Exception as e:
        print(f"Ошибка при выполнении тестов: {e}")
    
    print("\n=== СВОДКА РЕЗУЛЬТАТОВ ===")
    for test_name, results in all_results.items():
        if isinstance(results, dict):
            times = [v for k, v in results.items() if k.endswith('_time')]
            if times:
                avg_time = sum(times) / len(times)
                print(f"{test_name}: среднее время {avg_time:.3f}с")
    
    return all_results

def main():
    """Главная функция для запуска асинхронных тестов"""
    return asyncio.run(run_all_tests())

if __name__ == "__main__":
    results = main()
