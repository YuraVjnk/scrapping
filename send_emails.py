import os, sys, django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append('proj')
os.environ['DJANGO_SETTINGS_MODULE'] = 'scrapping.settings'

django.setup()
from scrapping_app.models import Vacancy, Error, Url, City, Language
from scrapping.settings import EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Рассылка вакансий за {today}'
text_content = f'Рассылка вакансий за {today}'
from_email = EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

empty = '<h2>К сожалению, на сегодня по вашим предпочтениям вакансий нет!</h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for i in qs:
    if i['city'] and i['language']:
        users_dict.setdefault((i['city'], i['language']), [])
        users_dict[(i['city'], i['language'])].append(i['email'])
if users_dict:
    params = {'city_id__in': [],
              'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()[:10]
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h4><a href="{row["url"]}">{row["title"]}</a></h4>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        final_html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(final_html, "text/html")
            a = 1
            msg.send()





subject = ''
text_content = ''
to = ADMIN_USER
content = ''
qs = Error.objects.filter(timestamp=today)
subject_error = f'Ошибки скраппинга || Пожаления пользователей || Отсутсвующие URL | На {today}'
text_content_error = f'Ошибки скраппинга || Пожаления пользователей || Отсутсвующие URL | На {today}'
if qs.exists():
    error = qs.first()
    data = error.data
    content += f'<h2>Ошибки за {today}</h2>'
    if 'Errors' in data:
        for i in data['Errors']:
            content += f'<h4><a href="{i["url"]}">Ошибка - {i["title"]}</a></h4>'
    else:
        content += f'<p>На сегодня новых ошибок нет</p>'
    content += '<hr>'
    content += '<h2>Пожаления пользователей</h2>'
    if 'user_data' in data:
        for i in data['user_data']:
            content += f'<h4>Город: {i["city"]},  ЯП: {i["language"]}, email: {i["email"]}</h4>'
    else:
        content += f'<p>На сегодня новых пожеланий нет</p>'


qs = Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in qs}
urls_errors = ''
for key, values in users_dict.items():
    if key not in urls_dict:
        urls_errors += f'<h4>Для Города - {City.objects.get(id=key[0])} и языка - {Language.objects.get(id=key[1])} отсутсвуют вакансии</h4>'
content += '<hr>'
content += '<h2>Недостающие URL</h2>'
if urls_errors:
    content += urls_errors
else:
    content += '<p>На сегодня новых URL нет</p>'


msg = EmailMultiAlternatives(subject_error, text_content_error, from_email, [to])
msg.attach_alternative(content, "text/html")
msg.send()
