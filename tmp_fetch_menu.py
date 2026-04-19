import urllib.request

url = 'http://127.0.0.1:8000/table/1/menu/'
try:
    data = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
    print('OK')
    terms = ['Cart parsed from backend', 'let cart = {}', 'function updateCartBar', "console.log('=== RENDER CART PAGE ===')"]
    for t in terms:
        print(f'{t}: {t in data}')
    idx = data.find('let cart')
    print(data[idx:idx+400])
except Exception as e:
    print('ERR', e)
