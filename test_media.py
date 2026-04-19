import urllib.request

try:
    r = urllib.request.urlopen('http://127.0.0.1:8000/media/menu_images/41g7lMwDtAL.jpg')
    content = r.read()
    print(f"Status: {r.status}")
    print(f"Content length: {len(content)}")
    print("Image is accessible!")
except Exception as e:
    print(f"Error: {e}")