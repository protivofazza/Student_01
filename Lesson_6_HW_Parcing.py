import requests
from bs4 import BeautifulSoup
import json


"""Програма при запуску на виконання за допомогою 'api.ipstack.com' визначає населений пункт користувача і виводить 
прогноз погоди для цого місця на наступну добу. Далі за бажанням користувач може запросити прогноз для іншого міста 
та дати, шляхом введення цієї інформації з клавіатури. Також програма перевіряє, чи не вібулося змін в певних місцях 
коду сайту, щоб попередити користувача про можливе некоректне відображення інформації"""


class WeatherParser:

    def __init__(self, base_url):
        self.base_url = base_url
        self.last_time = ''

    def get_page(self):
        try:
            res = requests.get(self.base_url)
        except requests.ConnectionError:
            return
        if res.status_code < 400:
            return res.text

    @staticmethod
    def get_local_city():
        send_url = "http://api.ipstack.com/check?access_key=03085a3acd43146eb875db9b663d7383&language=ru"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        # latitude = geo_json['latitude']
        # longitude = geo_json['longitude']
        return geo_json['city']

    @staticmethod
    def get_weather(day_=2):  # За замовчуванням метод повертатиме погоду на завтра для міста
        id_day = "bd" + str(day_)
        return f'\t\tмін {soup.find("div", id=id_day).findNext("div", class_="min").findNext("span").text}' \
               f'   макс {soup.find("div", id=id_day).findNext("div", class_="max").findNext("span").text}' \
               f'       {soup.find("div", id=id_day).findNext("div").get(key="title")}'


url_for_parsing = f'https://ua.sinoptik.ua/погода-{WeatherParser.get_local_city()}/10-днів'
parser = WeatherParser(url_for_parsing)
page = parser.get_page()
soup = BeautifulSoup(page, 'html.parser')
if not soup.head.find("title").text == 'SINOPTIK: Погода у Києві на 10 днів, прогноз погоди на 10 днів у Києві та ' \
                                       'Україна. Довгостроковий метеопрогноз Київ у Київській області':
    print("Адміністратором сайту-джерела були зроблені не верифіковані зміни в коді сайту. Програма може відображати"
          " інформацію некоректно. Будьте уважні")

print(f'\n{soup.head.find("title").text[10:soup.head.find("title").text.find("на") - 1]} на завтра, '
      f'{soup.find("div", id="bd2").findNext("p", class_="date").text} '
      f'{soup.find("div", id="bd2").findNext("p", class_="month").text}, очікується наступна:')
print(parser.get_weather())

city = input("\nЩоб отримати погоду для іншого міста, введіть його назву (Enter, щоб залишити визначене місто): ")
try:
    if city:
        url_for_parsing = f'https://ua.sinoptik.ua/погода-{city}/10-днів'
        parser = WeatherParser(url_for_parsing)
        page = parser.get_page()
        soup = BeautifulSoup(page, 'html.parser')
except TypeError:
    print("Міста з назвою, що була введена, не знайдено в переліку доступних для прогнозу.\nПеревірте правильність "
          "написання назви міста та спробуйте ще раз.")
    exit(21)

print(f"\nЩоб отримати прогноз не на завтра, а на інший день, зазначте відповідну цифру:"
      f'\n              1 - погода у {soup.head.find("title").text[19:soup.head.find("title").text.find("на") - 1]} на '
      f'{soup.find("div", id="bd1").findNext("p", class_="date").text} '
      f'{soup.find("div", id="bd1").findNext("p", class_="month").text} (сьогодні)'
      f'\n              2 - {soup.find("div", id="bd2").findNext("a", class_="day-link").get(key="title")} (завтра)'
      f'\n              3 - {soup.find("div", id="bd3").findNext("a", class_="day-link").get(key="title")}(післязавтра)'
      f'\n              4 - {soup.find("div", id="bd4").findNext("a", class_="day-link").get(key="title")}'
      f'\n              5 - {soup.find("div", id="bd5").findNext("a", class_="day-link").get(key="title")}'
      f'\n              6 - {soup.find("div", id="bd6").findNext("a", class_="day-link").get(key="title")}'
      f'\n              7 - {soup.find("div", id="bd7").findNext("a", class_="day-link").get(key="title")}'
      f'\n              8 - {soup.find("div", id="bd8").findNext("a", class_="day-link").get(key="title")}'
      f'\n              9 - {soup.find("div", id="bd9").findNext("a", class_="day-link").get(key="title")}'
      f'\n             10 - {soup.find("div", id="bd10").findNext("a", class_="day-link").get(key="title")}')

day_set = input('\nВведіть цифру для вашого варіанту вибору: ')
if not day_set.isdigit() or not 1 <= int(day_set) <= 10:
    print('\nВведено неіснуючий варіант вибору, тому за замовчуванням виводиться',
          soup.find("div", id="bd2").findNext("a", class_="day-link").get(key="title"), '(завтра):', '\n',
          WeatherParser.get_weather(), '\n')
elif day_set and day_set.isdigit():
    print('\nДля демонстрації вибрана',
          soup.find("div", id="bd" + day_set).findNext("a", class_="day-link").get(key="title") + ':', '\n',
          WeatherParser.get_weather(int(day_set)), '\n')
elif not day_set:
    print('\nОскільки дата не вибрана, за замовчуванням виводиться',
          soup.find("div", id="bd2").findNext("a", class_="day-link").get(key="title"), '(завтра):', '\n',
          WeatherParser.get_weather(), '\n')


