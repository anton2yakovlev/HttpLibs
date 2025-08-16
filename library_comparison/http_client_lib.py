import http.client
import urllib.parse
import time
import tempfile
import os
import json
from functools import wraps

# Константа для базового URL
BASE_HOST = "httpbin.org"
BASE_PORT = 443  # HTTPS

def measure_time(func):
    """Декоратор для измерения времени выполнения функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        return result, execution_time
    return wrapper

def create_connection():
    """Создает HTTPS соединение"""
    return http.client.HTTPSConnection(BASE_HOST, BASE_PORT)

# === Функции для каждого запроса ===

@measure_time
def get_request():
    """GET запрос"""
    conn = create_connection()
    conn.request("GET", "/get")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def post_json_request():
    """POST запрос с JSON"""
    post_data = {"name": "test", "value": 123}
    data = json.dumps(post_data).encode('utf-8')
    
    conn = create_connection()
    headers = {'Content-Type': 'application/json', 'Content-Length': str(len(data))}
    conn.request("POST", "/post", body=data, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def put_request():
    """PUT запрос"""
    put_data = {"updated": True}
    data = json.dumps(put_data).encode('utf-8')
    
    conn = create_connection()
    headers = {'Content-Type': 'application/json', 'Content-Length': str(len(data))}
    conn.request("PUT", "/put", body=data, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def delete_request():
    """DELETE запрос"""
    conn = create_connection()
    conn.request("DELETE", "/delete")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def get_with_params():
    """GET с параметрами"""
    params = {"param1": "value1", "param2": "value2"}
    query_string = urllib.parse.urlencode(params)
    path = f"/get?{query_string}"
    
    conn = create_connection()
    conn.request("GET", path)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def get_with_headers():
    """GET с кастомными заголовками"""
    headers = {
        'Custom-Header': 'test-value',
        'Authorization': 'Bearer token123'
    }
    
    conn = create_connection()
    conn.request("GET", "/headers", headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def get_user_agent():
    """GET с User-Agent"""
    headers = {'User-Agent': 'HttpClientTestClient/1.0'}
    
    conn = create_connection()
    conn.request("GET", "/user-agent", headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def post_json():
    """POST с JSON данными"""
    json_data = {"key": "value", "number": 42}
    data = json.dumps(json_data).encode('utf-8')
    
    conn = create_connection()
    headers = {'Content-Type': 'application/json', 'Content-Length': str(len(data))}
    conn.request("POST", "/post", body=data, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def post_form_data():
    """POST с form data"""
    form_data = {"field1": "value1", "field2": "value2"}
    data = urllib.parse.urlencode(form_data).encode('utf-8')
    
    conn = create_connection()
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': str(len(data))}
    conn.request("POST", "/post", body=data, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def post_raw_text():
    """POST с raw text"""
    raw_text = "Это просто текстовые данные для отправки"
    data = raw_text.encode('utf-8')
    
    conn = create_connection()
    headers = {'Content-Type': 'text/plain', 'Content-Length': str(len(data))}
    conn.request("POST", "/post", body=data, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def basic_auth_request():
    """Basic аутентификация"""
    import base64
    credentials = base64.b64encode(b'user:pass').decode('ascii')
    headers = {'Authorization': f'Basic {credentials}'}
    
    conn = create_connection()
    conn.request("GET", "/basic-auth/user/pass", headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def digest_auth_request():
    """Digest аутентификация (http.client не поддерживает нативно)"""
    conn = create_connection()
    conn.request("GET", "/get")  # fallback
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def set_cookies_request():
    """Установка cookies"""
    conn = create_connection()
    conn.request("GET", "/cookies/set?session=abc123")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def get_cookies_request():
    """Получение cookies (http.client требует ручного управления)"""
    # Делаем простой запрос без управления cookies
    conn = create_connection()
    conn.request("GET", "/cookies")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def error_404_request():
    """Запрос с 404 ошибкой"""
    conn = create_connection()
    conn.request("GET", "/status/404")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def error_500_request():
    """Запрос с 500 ошибкой"""
    conn = create_connection()
    conn.request("GET", "/status/500")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def error_429_request():
    """Запрос с 429 ошибкой"""
    conn = create_connection()
    conn.request("GET", "/status/429")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def redirect_3_request():
    """Запрос с 3 редиректами (http.client не следует редиректам автоматически)"""
    conn = create_connection()
    conn.request("GET", "/redirect/3")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def redirect_to_request():
    """Редирект на конкретный URL"""
    conn = create_connection()
    conn.request("GET", f"/redirect-to?url=https://{BASE_HOST}/get")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def no_redirect_request():
    """Запрос без автоматических редиректов"""
    # httplib2 по умолчанию следует редиректам, создаем новый объект
    http_no_redirect = http.client.HTTPSConnection(BASE_HOST, BASE_PORT)
    http_no_redirect.follow_redirects = False
    http_no_redirect.request("GET", "/redirect/1")
    response = http_no_redirect.getresponse()
    data = response.read()
    http_no_redirect.close()
    return response

@measure_time
def delay_1_request():
    """Запрос с задержкой 1 секунда"""
    conn = create_connection()
    conn.request("GET", "/delay/1")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def delay_5_timeout_request():
    """Запрос с задержкой 5 секунд и таймаутом 3 секунды"""
    try:
        conn = create_connection()
        conn.timeout = 3
        conn.request("GET", "/delay/5")
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return response
    except Exception:
        return None

@measure_time
def stream_lines_request():
    """Стриминг строк"""
    conn = create_connection()
    conn.request("GET", "/stream/10")
    response = conn.getresponse()
    content = response.read().decode('utf-8')
    lines = content.strip().split('\n')
    conn.close()
    return response, len(lines)

@measure_time
def stream_bytes_request():
    """Стриминг бинарных данных"""
    conn = create_connection()
    conn.request("GET", "/bytes/1024")
    response = conn.getresponse()
    content = response.read()
    conn.close()
    return response, len(content)

@measure_time
def gzip_request():
    """GZIP декомпрессия"""
    conn = create_connection()
    conn.request("GET", "/gzip")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def brotli_request():
    """Brotli декомпрессия (не поддерживается)"""
    conn = create_connection()
    conn.request("GET", "/get")  # fallback
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def file_upload_request():
    """Загрузка файла (упрощенная)"""
    # Создаём временный файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
        temp_file.write("Это тестовый файл для загрузки\nВторая строка файла")
        temp_file_path = temp_file.name
    
    try:
        with open(temp_file_path, 'rb') as f:
            file_content = f.read()
        
        data = urllib.parse.urlencode({'description': 'Тестовый файл', 'file': file_content.decode('utf-8', errors='ignore')}).encode('utf-8')
        
        conn = create_connection()
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': str(len(data))}
        conn.request("POST", "/post", body=data, headers=headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return response
    finally:
        os.unlink(temp_file_path)

@measure_time
def json_response_request():
    """JSON ответ"""
    conn = create_connection()
    conn.request("GET", "/json")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def xml_response_request():
    """XML ответ"""
    conn = create_connection()
    conn.request("GET", "/xml")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def html_response_request():
    """HTML ответ"""
    conn = create_connection()
    conn.request("GET", "/html")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

@measure_time
def image_response_request():
    """PNG изображение"""
    conn = create_connection()
    conn.request("GET", "/image/png")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response

# === Функции тестирования ===

def test_basic_requests():
    """1. Базовые запросы - GET, POST, PUT, DELETE"""
    print("\n=== 1. Базовые запросы ===")
    
    response, get_time = get_request()
    print(f"GET запрос: {response.status}, время: {get_time:.3f}с")
    
    response, post_time = post_json_request()
    print(f"POST запрос: {response.status}, время: {post_time:.3f}с")
    
    response, put_time = put_request()
    print(f"PUT запрос: {response.status}, время: {put_time:.3f}с")
    
    response, delete_time = delete_request()
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
    
    response, params_time = get_with_params()
    print(f"GET с параметрами: {response.status}, время: {params_time:.3f}с")
    
    response, headers_time = get_with_headers()
    print(f"Кастомные заголовки: {response.status}, время: {headers_time:.3f}с")
    
    response, ua_time = get_user_agent()
    print(f"User-Agent: {response.status}, время: {ua_time:.3f}с")
    
    return {
        'params_time': params_time,
        'headers_time': headers_time,
        'ua_time': ua_time
    }

def test_request_body_formats():
    """3. Тело запроса в различных форматах"""
    print("\n=== 3. Форматы тела запроса ===")
    
    response, json_time = post_json()
    print(f"JSON данные: {response.status}, время: {json_time:.3f}с")
    
    response, form_time = post_form_data()
    print(f"Form data: {response.status}, время: {form_time:.3f}с")
    
    response, text_time = post_raw_text()
    print(f"Raw text: {response.status}, время: {text_time:.3f}с")
    
    return {
        'json_time': json_time,
        'form_time': form_time,
        'text_time': text_time
    }

def test_authentication():
    """4. Аутентификация"""
    print("\n=== 4. Аутентификация ===")
    
    response, basic_time = basic_auth_request()
    print(f"Basic Auth: {response.status}, время: {basic_time:.3f}с")
    
    response, digest_time = digest_auth_request()
    print(f"Digest Auth (fallback): {response.status}, время: {digest_time:.3f}с")
    
    return {
        'basic_time': basic_time,
        'digest_time': digest_time
    }

def test_cookies():
    """5. Работа с Cookies"""
    print("\n=== 5. Cookies ===")
    
    response, set_cookie_time = set_cookies_request()
    print(f"Установка cookie: {response.status}, время: {set_cookie_time:.3f}с")
    
    response, get_cookie_time = get_cookies_request()
    print(f"Получение cookies: {response.status}, время: {get_cookie_time:.3f}с")
    
    return {
        'set_cookie_time': set_cookie_time,
        'get_cookie_time': get_cookie_time
    }

def test_error_handling():
    """6. Обработка ошибок"""
    print("\n=== 6. Обработка ошибок ===")
    
    response, error_time = error_404_request()
    print(f"404 ошибка: {response.status}, время: {error_time:.3f}с")
    
    response, error_time = error_500_request()
    print(f"500 ошибка: {response.status}, время: {error_time:.3f}с")
    
    response, error_time = error_429_request()
    print(f"429 ошибка: {response.status}, время: {error_time:.3f}с")
    
    return {
        'error_handling_time': error_time
    }

def test_redirects():
    """7. Редиректы (ограниченные в http.client)"""
    print("\n=== 7. Редиректы ===")
    
    response, redirect_time = redirect_3_request()
    print(f"Запрос с редиректами: {response.status}, время: {redirect_time:.3f}с")
    
    response, redirect_to_time = redirect_to_request()
    print(f"Редирект на URL: {response.status}, время: {redirect_to_time:.3f}с")
    
    return {
        'redirect_time': redirect_time,
        'redirect_to_time': redirect_to_time
    }

def test_timeouts():
    """8. Таймауты и задержки"""
    print("\n=== 8. Таймауты ===")
    
    response, delay1_time = delay_1_request()
    print(f"Задержка 1с: {response.status}, время: {delay1_time:.3f}с")
    
    response, timeout_time = delay_5_timeout_request()
    if response is None:
        print(f"Таймаут сработал через {timeout_time:.3f}с")
    else:
        print(f"Задержка 5с с таймаутом 3с: {response.status}, время: {timeout_time:.3f}с")
    
    return {
        'delay1_time': delay1_time,
        'timeout_time': timeout_time
    }

def test_streaming():
    """9. Стриминг данных"""
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
    
    response, gzip_time = gzip_request()
    print(f"GZIP: {response.status}, время: {gzip_time:.3f}с")
    
    response, brotli_time = brotli_request()
    print(f"Brotli (fallback): {response.status}, время: {brotli_time:.3f}с")
    
    return {
        'gzip_time': gzip_time,
        'brotli_time': brotli_time
    }

def test_file_upload():
    """11. Загрузка файлов"""
    print("\n=== 11. Загрузка файлов ===")
    
    response, upload_time = file_upload_request()
    print(f"Загрузка файла: {response.status}, время: {upload_time:.3f}с")
    
    return {
        'upload_time': upload_time
    }

def test_response_formats():
    """12. Различные форматы ответов"""
    print("\n=== 12. Форматы ответов ===")
    
    response, json_time = json_response_request()
    print(f"JSON: {response.status}, время: {json_time:.3f}с")
    
    response, xml_time = xml_response_request()
    print(f"XML: {response.status}, время: {xml_time:.3f}с")
    
    response, html_time = html_response_request()
    print(f"HTML: {response.status}, время: {html_time:.3f}с")
    
    response, image_time = image_response_request()
    print(f"PNG изображение: {response.status}, время: {image_time:.3f}с")
    
    return {
        'json_time': json_time,
        'xml_time': xml_time,
        'html_time': html_time,
        'image_time': image_time
    }

def run_all_tests():
    """Запуск всех тестов"""
    print("=== ТЕСТИРОВАНИЕ БИБЛИОТЕКИ HTTP.CLIENT ===")
    
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
