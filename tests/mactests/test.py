import requests
with open('textfile.txt', 'w') as textfile:
    textfile.write(requests.get(url='https://search.rsl.ru/ru/search#q=author%3A(%D0%9B.%D0%92.%20%D0%93%D0%BE%D0%BB%D1%83%D0%B1%D0%B5%D0%B2%D0%B0)%20OR%20author%3A(%D0%93%D0%BE%D0%BB%D1%83%D0%B1%D0%B5%D0%B2%D0%B0%20%D0%9B.%D0%92.)').text)
    textfile.close()

