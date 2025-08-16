import requests
import time
import concurrent.futures
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import json
import tempfile
import os
from functools import wraps

# Константа для базового URL
BASE_URL = "https://httpbin.org"

def measure_time(func):
    """Декоратор для измерения времени выполнения функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        return result, execution_time
    return wrapper

# === Отдельные функции для каждого запроса ===

@measure_time
def get_request():
    """GET запрос"""
    response = requests.get(f'{BASE_URL}/get')
    return response

@measure_time  
def post_json_request():
    """POST запрос с JSON"""
    post_data = {"name": "test", "value": 123}
    response = requests.post(f'{BASE_URL}/post', json=post_data)
    return response

@measure_time
def put_request():
    """PUT запрос"""
    put_data = {"updated": True}
    response = requests.put(f'{BASE_URL}/put', json=put_data)
    return response

@measure_time
def delete_request():
    """DELETE запрос"""
    response = requests.delete(f'{BASE_URL}/delete')
    return response

@measure_time
def get_with_params():
    """GET с параметрами"""
    params = {"param1": "value1", "param2": "value2"}
    response = requests.get(f'{BASE_URL}/get', params=params)
    return response

@measure_time
def get_with_headers():
    """GET с кастомными заголовками"""
    headers = {
        "Custom-Header": "test-value",
        "Authorization": "Bearer token123"
    }
    response = requests.get(f'{BASE_URL}/headers', headers=headers)
    return response

@measure_time
def get_user_agent():
    """GET с User-Agent"""
    headers = {"User-Agent": "RequestsTestClient/1.0"}
    response = requests.get(f'{BASE_URL}/user-agent', headers=headers)
    return response

@measure_time
def post_json():
    """POST с JSON данными"""
    json_data = {"key": "value", "number": 42}
    response = requests.post(f'{BASE_URL}/post', json=json_data)
    return response

@measure_time
def post_form_data():
    """POST с form data"""
    form_data = {"field1": "value1", "field2": "value2"}
    response = requests.post(f'{BASE_URL}/post', data=form_data)
    return response

@measure_time
def post_raw_text():
    """POST с raw text"""
    raw_text = "Это просто текстовые данные для отправки"
    headers = {"Content-Type": "text/plain"}
    response = requests.post(f'{BASE_URL}/post', data=raw_text, headers=headers)
    return response

@measure_time
def basic_auth_request():
    """Basic аутентификация"""
    response = requests.get(f'{BASE_URL}/basic-auth/user/pass', 
                          auth=HTTPBasicAuth('user', 'pass'))
    return response

@measure_time
def digest_auth_request():
    """Digest аутентификация"""
    response = requests.get(f'{BASE_URL}/digest-auth/auth/user/pass',
                          auth=HTTPDigestAuth('user', 'pass'))
    return response

@measure_time
def set_cookies_request():
    """Установка cookies"""
    response = requests.get(f'{BASE_URL}/cookies/set?session=abc123')
    return response

@measure_time
def get_cookies_request(session):
    """Получение cookies через сессию"""
    response = session.get(f'{BASE_URL}/cookies')
    return response

@measure_time
def error_404_request():
    """Запрос с 404 ошибкой"""
    response = requests.get(f'{BASE_URL}/status/404')
    return response

@measure_time
def error_500_request():
    """Запрос с 500 ошибкой"""
    response = requests.get(f'{BASE_URL}/status/500')
    return response

@measure_time
def error_429_request():
    """Запрос с 429 ошибкой"""
    response = requests.get(f'{BASE_URL}/status/429')
    return response

@measure_time
def redirect_3_request():
    """Запрос с 3 редиректами"""
    response = requests.get(f'{BASE_URL}/redirect/3')
    return response

@measure_time
def redirect_to_request():
    """Редирект на конкретный URL"""
    response = requests.get(f'{BASE_URL}/redirect-to?url={BASE_URL}/get')
    return response

@measure_time
def no_redirect_request():
    """Запрос без автоматических редиректов"""
    response = requests.get(f'{BASE_URL}/redirect/1', allow_redirects=False)
    return response

@measure_time
def delay_1_request():
    """Запрос с задержкой 1 секунда"""
    response = requests.get(f'{BASE_URL}/delay/1')
    return response

@measure_time
def delay_5_timeout_request():
    """Запрос с задержкой 5 секунд и таймаутом 3 секунды"""
    try:
        response = requests.get(f'{BASE_URL}/delay/5', timeout=3)
        return response
    except requests.exceptions.Timeout:
        return None

@measure_time
def stream_lines_request():
    """Стриминг строк"""
    response = requests.get(f'{BASE_URL}/stream/10', stream=True)
    stream_lines = []
    for line in response.iter_lines():
        if line:
            stream_lines.append(line.decode('utf-8'))
    return response, len(stream_lines)

@measure_time
def stream_bytes_request():
    """Стриминг бинарных данных"""
    response = requests.get(f'{BASE_URL}/bytes/1024', stream=True)
    chunks = []
    for chunk in response.iter_content(chunk_size=256):
        chunks.append(chunk)
    total_bytes = sum(len(chunk) for chunk in chunks)
    return response, total_bytes

@measure_time
def gzip_request():
    """GZIP декомпрессия"""
    response = requests.get(f'{BASE_URL}/gzip')
    return response

@measure_time
def brotli_request():
    """Brotli декомпрессия"""
    response = requests.get(f'{BASE_URL}/brotli')
    return response

@measure_time
def sequential_delays():
    """Последовательные запросы с задержками"""
    urls = [
        f'{BASE_URL}/delay/1',
        f'{BASE_URL}/delay/2', 
        f'{BASE_URL}/delay/3'
    ]
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.status_code)
    return results

@measure_time
def parallel_delays():
    """Параллельные запросы с задержками"""
    urls = [
        f'{BASE_URL}/delay/1',
        f'{BASE_URL}/delay/2', 
        f'{BASE_URL}/delay/3'
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(requests.get, url) for url in urls]
        results = [future.result().status_code for future in concurrent.futures.as_completed(futures)]
    return results

@measure_time
def file_upload_request():
    """Загрузка файла"""
    # Создаём временный файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
        temp_file.write("Это тестовый файл для загрузки\nВторая строка файла")
        temp_file_path = temp_file.name
    
    try:
        with open(temp_file_path, 'rb') as file:
            files = {'file': ('test.txt', file, 'text/plain')}
            data = {'description': 'Тестовый файл'}
            response = requests.post(f'{BASE_URL}/post', files=files, data=data)
        return response
    finally:
        os.unlink(temp_file_path)

@measure_time
def json_response_request():
    """JSON ответ"""
    response = requests.get(f'{BASE_URL}/json')
    return response

@measure_time
def xml_response_request():
    """XML ответ"""
    response = requests.get(f'{BASE_URL}/xml')
    return response

@measure_time
def html_response_request():
    """HTML ответ"""
    response = requests.get(f'{BASE_URL}/html')
    return response

@measure_time
def image_response_request():
    """PNG изображение"""
    response = requests.get(f'{BASE_URL}/image/png')
    return response

@measure_time
def session_set_cookie(session):
    """Установка cookie через сессию"""
    response = session.get(f'{BASE_URL}/cookies/set?session=test')
    return response

@measure_time
def session_get_cookie(session):
    """Получение cookie через сессию"""
    response = session.get(f'{BASE_URL}/cookies')
    return response

@measure_time
def session_headers_request(session):
    """Запрос с постоянными заголовками сессии"""
    response = session.get(f'{BASE_URL}/headers')
    return response

# === Функции тестирования (без изменений) ===

def test_basic_requests():
    """1. Базовые запросы - GET, POST, PUT, DELETE"""
    print("\n=== 1. Базовые запросы ===")
    
    response, get_time = get_request()
    print(f"GET запрос: {response.status_code}, время: {get_time:.3f}с")
    
    response, post_time = post_json_request()
    print(f"POST запрос: {response.status_code}, время: {post_time:.3f}с")
    
    response, put_time = put_request()
    print(f"PUT запрос: {response.status_code}, время: {put_time:.3f}с")
    
    response, delete_time = delete_request()
    print(f"DELETE запрос: {response.status_code}, время: {delete_time:.3f}с")
    
    return {
        'get_time': get_time,
        'post_time': post_time, 
        'put_time': put_time,
        'delete_time': delete_time
    }

def test_params_and_headers():
    """2. Параметры и заголовки"""
    print("\n=== 2. Параметры и заголовки ===")
    
    response, params_time = get_with_params()
    print(f"GET с параметрами: {response.status_code}, время: {params_time:.3f}с")
    
    response, headers_time = get_with_headers()
    print(f"Кастомные заголовки: {response.status_code}, время: {headers_time:.3f}с")
    
    response, ua_time = get_user_agent()
    print(f"User-Agent: {response.status_code}, время: {ua_time:.3f}с")
    
    return {
        'params_time': params_time,
        'headers_time': headers_time,
        'ua_time': ua_time
    }

def test_request_body_formats():
    """3. Тело запроса в различных форматах"""
    print("\n=== 3. Форматы тела запроса ===")
    
    response, json_time = post_json()
    print(f"JSON данные: {response.status_code}, время: {json_time:.3f}с")
    
    response, form_time = post_form_data()
    print(f"Form data: {response.status_code}, время: {form_time:.3f}с")
    
    response, text_time = post_raw_text()
    print(f"Raw text: {response.status_code}, время: {text_time:.3f}с")
    
    return {
        'json_time': json_time,
        'form_time': form_time,
        'text_time': text_time
    }

def test_authentication():
    """4. Аутентификация"""
    print("\n=== 4. Аутентификация ===")
    
    response, basic_time = basic_auth_request()
    print(f"Basic Auth: {response.status_code}, время: {basic_time:.3f}с")
    
    response, digest_time = digest_auth_request()
    print(f"Digest Auth: {response.status_code}, время: {digest_time:.3f}с")
    
    return {
        'basic_time': basic_time,
        'digest_time': digest_time
    }

def test_cookies():
    """5. Работа с Cookies"""
    print("\n=== 5. Cookies ===")
    
    response, set_cookie_time = set_cookies_request()
    print(f"Установка cookie: {response.status_code}, время: {set_cookie_time:.3f}с")
    
    # Используем сессию для автоматического управления cookies
    session = requests.Session()
    session.get(f'{BASE_URL}/cookies/set?session=abc123')
    
    response, get_cookie_time = get_cookies_request(session)
    print(f"Получение cookies: {response.status_code}, время: {get_cookie_time:.3f}с")
    print(f"Cookies в ответе: {response.json().get('cookies', {})}")
    
    return {
        'set_cookie_time': set_cookie_time,
        'get_cookie_time': get_cookie_time
    }

def test_error_handling():
    """6. Обработка ошибок"""
    print("\n=== 6. Обработка ошибок ===")
    
    try:
        response, error_time = error_404_request()
        print(f"404 ошибка: {response.status_code}, время: {error_time:.3f}с")
    except requests.exceptions.RequestException as e:
        print(f"Исключение 404: {e}")
    
    try:
        response, error_time = error_500_request()
        print(f"500 ошибка: {response.status_code}, время: {error_time:.3f}с")
    except requests.exceptions.RequestException as e:
        print(f"Исключение 500: {e}")
    
    try:
        response, error_time = error_429_request()
        print(f"429 ошибка: {response.status_code}, время: {error_time:.3f}с")
    except requests.exceptions.RequestException as e:
        print(f"Исключение 429: {e}")
    
    return {
        'error_handling_time': error_time
    }

def test_redirects():
    """7. Редиректы"""
    print("\n=== 7. Редиректы ===")
    
    response, redirect_time = redirect_3_request()
    print(f"Автоматические редиректы: {response.status_code}, время: {redirect_time:.3f}с")
    print(f"Финальный URL: {response.url}")
    
    response, redirect_to_time = redirect_to_request()
    print(f"Редирект на URL: {response.status_code}, время: {redirect_to_time:.3f}с")
    
    response, no_redirect_time = no_redirect_request()
    print(f"Без редиректов: {response.status_code}, время: {no_redirect_time:.3f}с")
    
    return {
        'redirect_time': redirect_time,
        'redirect_to_time': redirect_to_time,
        'no_redirect_time': no_redirect_time
    }

def test_timeouts():
    """8. Таймауты и задержки"""
    print("\n=== 8. Таймауты ===")
    
    response, delay1_time = delay_1_request()
    print(f"Задержка 1с: {response.status_code}, время: {delay1_time:.3f}с")
    
    response, timeout_time = delay_5_timeout_request()
    if response is None:
        print(f"Таймаут сработал через {timeout_time:.3f}с")
    else:
        print(f"Задержка 5с с таймаутом 3с: {response.status_code}, время: {timeout_time:.3f}с")
    
    return {
        'delay1_time': delay1_time,
        'timeout_time': timeout_time
    }

def test_streaming():
    """9. Стриминг данных"""
    print("\n=== 9. Стриминг ===")
    
    (response, stream_lines_count), stream_time = stream_lines_request()
    print(f"Стриминг 10 строк: {response.status_code}, время: {stream_time:.3f}с")
    print(f"Получено строк: {stream_lines_count}")
    
    (response, total_bytes), bytes_time = stream_bytes_request()
    print(f"Бинарные данные: {response.status_code}, время: {bytes_time:.3f}с, байт: {total_bytes}")
    
    return {
        'stream_time': stream_time,
        'bytes_time': bytes_time
    }

def test_compression():
    """10. Сжатие"""
    print("\n=== 10. Сжатие ===")
    
    response, gzip_time = gzip_request()
    print(f"GZIP декомпрессия: {response.status_code}, время: {gzip_time:.3f}с")
    data = response.json()
    print(f"Gzipped: {data.get('gzipped', False)}")
    
    response, brotli_time = brotli_request()
    print(f"Brotli декомпрессия: {response.status_code}, время: {brotli_time:.3f}с")
    data = response.json()
    print(f"Brotli compressed: {data.get('brotli', False)}")
    
    return {
        'gzip_time': gzip_time,
        'brotli_time': brotli_time
    }

def test_async_parallel():
    """11. Параллельные запросы (имитация асинхронности)"""
    print("\n=== 11. Параллельные запросы ===")
    
    sequential_results, sequential_time = sequential_delays()
    print(f"Последовательно: {sequential_time:.3f}с, результаты: {sequential_results}")
    
    parallel_results, parallel_time = parallel_delays()
    print(f"Параллельно: {parallel_time:.3f}с, результаты: {parallel_results}")
    
    return {
        'sequential_time': sequential_time,
        'parallel_time': parallel_time
    }

def test_file_upload():
    """12. Загрузка файлов"""
    print("\n=== 12. Загрузка файлов ===")
    
    response, upload_time = file_upload_request()
    print(f"Загрузка файла: {response.status_code}, время: {upload_time:.3f}с")
    
    response_data = response.json()
    files_info = response_data.get('files', {})
    print(f"Файлы в запросе: {list(files_info.keys())}")
    
    return {
        'upload_time': upload_time
    }

def test_response_formats():
    """13. Различные форматы ответов"""
    print("\n=== 13. Форматы ответов ===")
    
    response, json_time = json_response_request()
    json_data = response.json()
    print(f"JSON: {response.status_code}, время: {json_time:.3f}с")
    print(f"JSON поля: {list(json_data.keys())}")
    
    response, xml_time = xml_response_request()
    print(f"XML: {response.status_code}, время: {xml_time:.3f}с, размер: {len(response.text)} символов")
    
    response, html_time = html_response_request()
    print(f"HTML: {response.status_code}, время: {html_time:.3f}с, размер: {len(response.text)} символов")
    
    response, image_time = image_response_request()
    print(f"PNG изображение: {response.status_code}, время: {image_time:.3f}с, размер: {len(response.content)} байт")
    
    return {
        'json_time': json_time,
        'xml_time': xml_time,
        'html_time': html_time,
        'image_time': image_time
    }

def test_sessions():
    """14. Сессии"""
    print("\n=== 14. Сессии ===")
    
    session = requests.Session()
    
    response, set_session_time = session_set_cookie(session)
    print(f"Установка сессии: {response.status_code}, время: {set_session_time:.3f}с")
    
    response, get_session_time = session_get_cookie(session)
    print(f"Получение сессии: {response.status_code}, время: {get_session_time:.3f}с")
    
    cookies = response.json().get('cookies', {})
    print(f"Cookies в сессии: {cookies}")
    
    # Добавляем постоянные заголовки к сессии
    session.headers.update({'X-Session-Header': 'persistent-value'})
    
    response, headers_session_time = session_headers_request(session)
    print(f"Постоянные заголовки: {response.status_code}, время: {headers_session_time:.3f}с")
    
    return {
        'set_session_time': set_session_time,
        'get_session_time': get_session_time,
        'headers_session_time': headers_session_time
    }

def run_all_tests():
    """Запуск всех тестов"""
    print("=== ТЕСТИРОВАНИЕ БИБЛИОТЕКИ REQUESTS ===")
    
    all_results = {}
    
    try:
        all_results['basic'] = test_basic_requests()
        all_results['params'] = test_params_and_headers()
        all_results['body_formats'] = test_request_body_formats()
        all_results['auth'] = test_authentication()
        all_results['cookies'] = test_cookies()
        all_results['errors'] = test_error_handling()
        all_results['redirects'] = test_redirects()
        all_results['timeouts'] = test_timeouts()
        all_results['streaming'] = test_streaming()
        all_results['compression'] = test_compression()
        all_results['parallel'] = test_async_parallel()
        all_results['upload'] = test_file_upload()
        all_results['formats'] = test_response_formats()
        all_results['sessions'] = test_sessions()
        
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

if __name__ == "__main__":
    results = run_all_tests()