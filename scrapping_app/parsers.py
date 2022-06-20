import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work', 'dou', 'djini')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
     'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
     'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'},
]


def work(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    if url:
        response = requests.get(url, headers=headers[randint(0, 2)])
        if response.status_code == 200:
            soup = BS(response.content, 'html.parser')
            main_div = soup.find('div', id='pjax-jo2b-list')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'company': company,
                                 'description': content,
                                 'city_id': city,
                                 'language_id': language, })
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page Not Response'})

    return jobs, errors


# def rabota(url):
#     jobs = []
#     errors = []
#     domain = 'https://rabota.ua/'
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         soup = BS(response.content, 'html.parser')
#         main_div = soup.find('div', id='pjax-job-list')
#         if main_div:
#             div_list = main_div.find_all('div', attrs={'class': 'job-link'})
#             for div in div_list:
#                 title = div.find('h2')
#                 href = title.a['href']
#                 content = div.p.text
#                 company = 'No name'
#                 logo = div.find('img')
#                 if logo:
#                     company = logo['alt']
#                 jobs.append({'title': title.text,
#                              'url': domain + href,
#                              'company': company,
#                              'description': content, })
#         else:
#             errors.append({'url': url, 'title': 'Table does not exists'})
#     else:
#         errors.append({'url': url, 'title': 'Page Not Response'})
#
#     return jobs, errors


def dou(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        response = requests.get(url, headers=headers[randint(0, 2)])
        if response.status_code == 200:
            soup = BS(response.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_lst:
                    if '__hot' not in li['class']:
                        title = li.find('div', attrs={'class': 'title'})
                        href = title.a['href']
                        content = li.find('div', attrs={'class': 'sh-info'})
                        company = 'No name'
                        dou_company = title.find('a', attrs={'class': 'company'})
                        if dou_company:
                            company = dou_company.text
                        jobs.append({'title': title.a.text,
                                     'url': href,
                                     'company': company,
                                     'description': content.text,
                                     'city_id': city,
                                     'language_id': language,
                                     })
            else:
                errors.append({'url': url, 'title': 'Table does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page Not Response'})

    return jobs, errors


def djini(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    if url:
        response = requests.get(url, headers=headers[randint(0, 2)])
        if response.status_code == 200:
            soup = BS(response.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
            if main_ul:
                li_lst = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
                for li in li_lst:
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    content = li.find('div', attrs={'class': 'list-jobs__description'})
                    company = 'No name'
                    djini_company = li.find('div', attrs={'class': 'list-jobs__details__info'})
                    a = 1
                    if djini_company:
                        company = djini_company.text
                        a = 1
                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'company': company,
                                 'description': content.p.text,
                                 'city_id': city,
                                 'language_id': language,
                                 })
            else:
                errors.append({'url': url, 'title': 'Table does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page Not Response'})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://djinni.co/jobs/keyword-python/kyiv/'
    jobs, errors = djini(url)
    handler = codecs.open('djini12.txt', 'w', 'utf-8')
    handler.write(str(jobs))
    handler.close()
