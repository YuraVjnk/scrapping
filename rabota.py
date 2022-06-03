import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'}

domain = 'https://rabota.ua'
url = 'https://rabota.ua/ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'
response = requests.get(url, headers=headers)

# jobs = []
# errors = []
# if response.status_code == 200:
#     soup = BS(response.content, 'html.parser')
#     main_div = soup.find('div', id='pjax-job-list')
#     if main_div:
#         div_list = main_div.find_all('div', attrs={'class': 'job-link'})
#         for div in div_list:
#             title = div.find('h2')
#             href = title.a['href']
#             content = div.p.text
#             company = 'No name'
#             logo = div.find('img')
#             if logo:
#                 company = logo['alt']
#             jobs.append({'title': title.text,
#                          'url': domain + href,
#                          'company': company,
#                          'description': content, })
#     else:
#         errors.append({'url': url, 'title': 'Div does not exists'})
# else:
#     errors.append({'url': url, 'title': 'Page Not Response'})

handler = codecs.open('rabota.html', 'w', 'utf-8')
handler.write(str(response.text))
handler.close()
