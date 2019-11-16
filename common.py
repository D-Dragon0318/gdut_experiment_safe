import http.cookiejar
import urllib.parse
import urllib.request

# init cookie
cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

url_base = "http://222.200.98.165:8090/"
basic_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': '222.200.98.165:8090',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/78.0.3904.97 Safari/537.36'
}


def http_get(url: str, custom_header):
    _headers = basic_header.copy()
    _headers.update(custom_header)
    _request = urllib.request.Request(url=url, data=None, headers=_headers)
    _respond = opener.open(_request)
    _result = _respond.read().decode('gbk')
    return _result


def http_post(url: str, data, custom_header):
    _data = urllib.parse.urlencode(data).encode(encoding='utf-8')
    _headers = basic_header.copy()
    _headers.update(custom_header)
    _request = urllib.request.Request(url=url, data=_data, headers=_headers)

    try:
        _respond = opener.open(_request)
        _result = _respond.read().decode('gbk')
        return _result
    except urllib.request.HTTPError as _e:
        print(_e)
