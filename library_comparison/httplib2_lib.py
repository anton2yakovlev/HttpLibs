import httplib2
import time
import tempfile
import os
import json
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

# Создаем HTTP объект
http = httplib2.Http()

# === Функции для каждого запроса ===

@measure_time
def get_request():
    """GET запрос"""
    response, content = http.request(f'{BASE_URL}/get', 'GET')
    return response, content

@measure_time
def post_json_request():
    """POST запрос с JSON"""
    post_data = {"name": "test", "value": 123}
    data = json.dumps(post_data)
    headers = {'Content-Type': 'application/json'}
    response, content = http.request(f'{BASE_URL}/post', 'POST', body=data, headers=headers)
    return response, content

@measure_time
def put_request():
    """PUT запрос"""
    put_data = {"updated": True}
    data = json.dumps(put_data)
    headers = {'Content-Type': 'application/json'}
    response, content = http.request(f'{BASE_URL}/put', 'PUT', body=data, headers=headers)
    return response, content

@measure_time
def delete_request():
    """DELETE запрос"""
    response, content = http.request(f'{BASE_URL}/delete', 'DELETE')
    return response, content

@measure_time
def get_with_params():
    """GET с параметрами"""
    import urllib.parse
    params = {"param1": "value1", "param2": "value2"}
    query_string = urllib.parse.urlencode(params)
    url = f'{BASE_URL}/get?{query_string}'
    response, content = http.request(url, 'GET')
    return response, content

@measure_time
def get_with_headers():
    """GET с кастомными заголовками"""
    headers = {
        'Custom-Header': 'test-value',
        'Authorization': 'Bearer token123'
    }
    response, content = http.request(f'{BASE_URL}/headers', 'GET', headers=headers)
    return response, content

@measure_time
def get_user_agent():
    """GET с User-Agent"""
    headers = {'User-Agent': 'Httplib2TestClient/1.0'}
    response, content = http.request(f'{BASE_URL}/user-agent', 'GET', headers=headers)
    return response, content

@measure_time
def post_json():
    """POST с JSON данными"""
    json_data = {"key": "value", "number": 42}
    data = json.dumps(json_data)
    headers = {'Content-Type': 'application/json'}
    response, content = http.request(f'{BASE_URL}/post', 'POST', body=data, headers=headers)
    return response, content

@measure_time
def post_form_data():
    """POST с form data"""
    import urllib.parse
    form_data = {"field1": "value1", "field2": "value2"}
    data = urllib.parse.urlencode(form_data)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response, content = http.request(f'{BASE_URL}/post', 'POST', body=data, headers=headers)
    return response, content

@measure_time
def post_raw_text():
    """POST с raw text"""
    raw_text = "Это просто текстовые данные для отправки"
    headers = {'Content-Type': 'text/plain'}
    response, content = http.request(f'{BASE_URL}/post', 'POST', body=raw_text, headers=headers)
    return response, content

@measure_time
def basic_auth_request():
    """Basic аутентификация"""
    # httplib2 поддерживает добавление credentials в URL
    response, content = http.request(f'https://user:pass@httpbin.org/basic-auth/user/pass', 'GET')
    return response, content

@measure_time
def digest_auth_request():
    """Digest аутентификация"""
    # httplib2 поддерживает digest auth через add_credentials
    http.add_credentials('user', 'pass')
    response, content = http.request(f'{BASE_URL}/digest-auth/auth/user/pass', 'GET')
    return response, content

@measure_time
def set_cookies_request():
    """Установка cookies"""
    response, content = http.request(f'{BASE_URL}/cookies/set?session=abc123', 'GET')
    return response, content

@measure_time
def get_cookies_request():
    """Получение cookies (httplib2 автоматически управляет cookies)"""
    # Сначала устанавливаем cookie
    http.request(f'{BASE_URL}/cookies/set?session=abc123', 'GET')
    # Затем получаем cookies (должны сохраниться автоматически)
    response, content = http.request(f'{BASE_URL}/cookies', 'GET')
    return response, content

@measure_time
def error_404_request():
    """Запрос с 404 ошибкой"""
    response, content = http.request(f'{BASE_URL}/status/404', 'GET')
    return response, content

@measure_time
def error_500_request():
    """Запрос с 500 ошибкой"""
    response, content = http.request(f'{BASE_URL}/status/500', 'GET')
    return response, content

@measure_time
def error_429_request():
    """Запрос с 429 ошибкой"""
    response, content = http.request(f'{BASE_URL}/status/429', 'GET')
    return response, content

@measure_time
def redirect_3_request():
    """Запрос с 3 редиректами"""
    response, content = http.request(f'{BASE_URL}/redirect/3', 'GET')
    return response, content

@measure_time
def redirect_to_request():
    """Редирект на конкретный URL"""
    response, content = http.request(f'{BASE_URL}/redirect-to?url={BASE_URL}/get', 'GET')
    return response, content

@measure_time
def no_redirect_request():
    """Запрос без автоматических редиректов"""
    # httplib2 по умолчанию следует редиректам, создаем новый объект
    http_no_redirect = httplib2.Http()
    http_no_redirect.follow_redirects = False
    response, content = http_no_redirect.request(f'{BASE_URL}/redirect/1', 'GET')
    return response, content

@measure_time
def delay_1_request():
    """Запрос с задержкой 1 секунда"""
    response, content = http.request(f'{BASE_URL}/delay/1', 'GET')
    return response, content

@measure_time
def delay_5_timeout_request():
    """Запрос с задержкой 5 секунд и таймаутом 3 секунды"""
    try:
        http_timeout = httplib2.Http(timeout=3)
        response, content = http_timeout.request(f'{BASE_URL}/delay/5', 'GET')
        return response, content
    except Exception:
        return None, None

@measure_time
def stream_lines_request():
    """Стриминг строк (httplib2 читает весь ответ)"""
    response, content = http.request(f'{BASE_URL}/stream/10', 'GET')
    lines = content.decode('utf-8').strip().split('\n')
    return response, len(lines)

@measure_time
def stream_bytes_request():
    """Стриминг бинарных данных"""
    response, content = http.request(f'{BASE_URL}/bytes/1024', 'GET')
    return response, len(content)

@measure_time
def gzip_request():
    """GZIP декомпрессия (автоматическая)"""
    response, content = http.request(f'{BASE_URL}/gzip', 'GET')
    return response, content

@measure_time
def brotli_request():
    """Brotli декомпрессия"""
    response, content = http.request(f'{BASE_URL}/brotli', 'GET')
    return response, content

@measure_time
def file_upload_request():
    """Загрузка файла (простая форма)"""
    # Создаём временный файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
        temp_file.write("Это тестовый файл для загрузки\nВторая строка файла")
        temp_file_path = temp_file.name
    
    try:
        import urllib.parse
        with open(temp_file_path, 'rb') as f:
            file_content = f.read()
        
        data = urllib.parse.urlencode({
            'description': 'Тестовый файл', 
            'file': file_content.decode('utf-8', errors='ignore')
        })
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response, content = http.request(f'{BASE_URL}/post', 'POST', body=data, headers=headers)
        return response, content
    finally:
        os.unlink(temp_file_path)

@measure_time
def json_response_request():
    """JSON ответ"""
    response, content = http.request(f'{BASE_URL}/json', 'GET')
    return response, content

@measure_time
def xml_response_request():
    """XML ответ"""
    response, content = http.request(f'{BASE_URL}/xml', 'GET')
    return response, content

@measure_time
def html_response_request():
    """HTML ответ"""
    response, content = http.request(f'{BASE_URL}/html', 'GET')
    return response, content

@measure_time
def image_response_request():
    """PNG изображение"""
    response, content = http.request(f'{BASE_URL}/image/png', 'GET')
    return response, content

# === Функции тестирования ===

def test_basic_requests():
    """1. Базовые запросы - GET, POST, PUT, DELETE"""
    print("\n=== 1. Базовые запросы ===")
    
    (response, content), get_time = get_request()
    print(f"GET запрос: {response.status}, время: {get_time:.3f}с")
    
    (response, content), post_time = post_json_request()
    print(f"POST запрос: {response.status}, время: {post_time:.3f}с")
    
    (response, content), put_time = put_request()
    print(f"PUT запрос: {response.status}, время: {put_time:.3f}с")
    
    (response, content), delete_time = delete_request()
    print(f"DELETE запрос: {response.status}, время: {delete_time:.3f}с")
    
    return {
        'get_time': get_time,
        'post_time': post_time, 
        'put_time': put_time,
        'delete_time': delete_time
    }

def test_params_and_headers():
    """2. Параметры и заголовки"""
    print("\n=== 2. Параметры и заголовки ===")
    
    (response, content), params_time = get_with_params()
    print(f"GET с параметрами: {response.status}, время: {params_time:.3f}с")
    
    (response, content), headers_time = get_with_headers()
    print(f"Кастомные заголовки: {response.status}, время: {headers_time:.3f}с")
    
    (response, content), ua_time = get_user_agent()
    print(f"User-Agent: {response.status}, время: {ua_time:.3f}с")
    
    return {
        'params_time': params_time,
        'headers_time': headers_time,
        'ua_time': ua_time
    }

def test_request_body_formats():
    """3. Тело запроса в различных форматах"""
    print("\n=== 3. Форматы тела запроса ===")
    
    (response, content), json_time = post_json()
    print(f"JSON данные: {response.status}, время: {json_time:.3f}с")
    
    (response, content), form_time = post_form_data()
    print(f"Form data: {response.status}, время: {form_time:.3f}с")
    
    (response, content), text_time = post_raw_text()
    print(f"Raw text: {response.status}, время: {text_time:.3f}с")
    
    return {
        'json_time': json_time,
        'form_time': form_time,
        'text_time': text_time
    }

def test_authentication():
    """4. Аутентификация"""
    print("\n=== 4. Аутентификация ===")
    
    (response, content), basic_time = basic_auth_request()
    print(f"Basic Auth: {response.status}, время: {basic_time:.3f}с")
    
    (response, content), digest_time = digest_auth_request()
    print(f"Digest Auth: {response.status}, время: {digest_time:.3f}с")
    
    return {
        'basic_time': basic_time,
        'digest_time': digest_time
    }

def test_cookies():
    """5. Работа с Cookies"""
    print("\n=== 5. Cookies ===")
    
    (response, content), set_cookie_time = set_cookies_request()
    print(f"Установка cookie: {response.status}, время: {set_cookie_time:.3f}с")
    
    (response, content), get_cookie_time = get_cookies_request()
    print(f"Получение cookies: {response.status}, время: {get_cookie_time:.3f}с")
    
    data = json.loads(content.decode('utf-8'))
    print(f"Cookies в ответе: {data.get('cookies', {})}")
    
    return {
        'set_cookie_time': set_cookie_time,
        'get_cookie_time': get_cookie_time
    }

def test_error_handling():
    """6. Обработка ошибок"""
    print("\n=== 6. Обработка ошибок ===")
    
    (response, content), error_time = error_404_request()
    print(f"404 ошибка: {response.status}, время: {error_time:.3f}с")
    
    (response, content), error_time = error_500_request()
    print(f"500 ошибка: {response.status}, время: {error_time:.3f}с")
    
    (response, content), error_time = error_429_request()
    print(f"429 ошибка: {response.status}, время: {error_time:.3f}с")
    
    return {
        'error_handling_time': error_time
    }

def test_redirects():
    """7. Редиректы"""
    print("\n=== 7. Редиректы ===")
    
    (response, content), redirect_time = redirect_3_request()
    print(f"Автоматические редиректы: {response.status}, время: {redirect_time:.3f}с")
    
    (response, content), redirect_to_time = redirect_to_request()
    print(f"Редирект на URL: {response.status}, время: {redirect_to_time:.3f}с")
    
    (response, content), no_redirect_time = no_redirect_request()
    print(f"Без редиректов: {response.status}, время: {no_redirect_time:.3f}с")
    
    return {
        'redirect_time': redirect_time,
        'redirect_to_time': redirect_to_time,
        'no_redirect_time': no_redirect_time
    }

def test_timeouts():
    """8. Таймауты и задержки"""
    print("\n=== 8. Таймауты ===")
    
    (response, content), delay1_time = delay_1_request()
    print(f"Задержка 1с: {response.status}, время: {delay1_time:.3f}с")
    
    result, timeout_time = delay_5_timeout_request()
    if result is None:
        print(f"Таймаут сработал через {timeout_time:.3f}с")
    else:
        response, content = result
        print(f"Задержка 5с с таймаутом 3с: {response.status}, время: {timeout_time:.3f}с")
    
    return {
        'delay1_time': delay1_time,
        'timeout_time': timeout_time
    }

def test_streaming():
    """9. Стриминг данных (ограничено в httplib2)"""
    print("\n=== 9. Стриминг ===")
    
    (response, stream_lines_count), stream_time = stream_lines_request()
    print(f"Стриминг 10 строк: {response.status}, время: {stream_time:.3f}с")
    print(f"Получено строк: {stream_lines_count}")
    
    (response, total_bytes), bytes_time = stream_bytes_request()
    print(f"Бинарные данные: {response.status}, время: {bytes_time:.3f}с, байт: {total_bytes}")
    
    return {
        'stream_time': stream_time,
        'bytes_time': bytes_time
    }

def test_compression():
    """10. Сжатие"""
    print("\n=== 10. Сжатие ===")
    
    (response, content), gzip_time = gzip_request()
    print(f"GZIP декомпрессия: {response.status}, время: {gzip_time:.3f}с")
    data = json.loads(content.decode('utf-8'))
    print(f"Gzipped: {data.get('gzipped', False)}")
    
    (response, content), brotli_time = brotli_request()
    print(f"Brotli декомпрессия: {response.status}, время: {brotli_time:.3f}с")
    data = json.loads(content.decode('utf-8'))
    print(f"Brotli compressed: {data.get('brotli', False)}")
    
    return {
        'gzip_time': gzip_time,
        'brotli_time': brotli_time
    }

def test_file_upload():
    """11. Загрузка файлов"""
    print("\n=== 11. Загрузка файлов ===")
    
    (response, content), upload_time = file_upload_request()
    print(f"Загрузка файла: {response.status}, время: {upload_time:.3f}с")
    
    return {
        'upload_time': upload_time
    }

def test_response_formats():
    """12. Различные форматы ответов"""
    print("\n=== 12. Форматы ответов ===")
    
    (response, content), json_time = json_response_request()
    data = json.loads(content.decode('utf-8'))
    print(f"JSON: {response.status}, время: {json_time:.3f}с")
    print(f"JSON поля: {list(data.keys())}")
    
    (response, content), xml_time = xml_response_request()
    print(f"XML: {response.status}, время: {xml_time:.3f}с, размер: {len(content)} байт")
    
    (response, content), html_time = html_response_request()
    print(f"HTML: {response.status}, время: {html_time:.3f}с, размер: {len(content)} байт")
    
    (response, content), image_time = image_response_request()
    print(f"PNG изображение: {response.status}, время: {image_time:.3f}с, размер: {len(content)} байт")
    
    return {
        'json_time': json_time,
        'xml_time': xml_time,
        'html_time': html_time,
        'image_time': image_time
    }

def run_all_tests():
    """Запуск всех тестов"""
    print("=== ТЕСТИРОВАНИЕ БИБЛИОТЕКИ HTTPLIB2 ===")
    
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
        all_results['upload'] = test_file_upload()
        all_results['formats'] = test_response_formats()
        
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