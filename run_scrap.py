import asyncio, os, sys, django
from django.contrib.auth import get_user_model
import datetime as dt

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append('proj')
os.environ['DJANGO_SETTINGS_MODULE'] = 'scrapping.settings'

django.setup()
from django.db import DatabaseError
from scrapping_app.parsers import *
from scrapping_app.models import Vacancy, Error, Url

User = get_user_model()

parsers = (
    (work, 'work'),
    (dou, 'dou'),
    (djini, 'djini'),
)

jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dict[pair]
            urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_lst = get_urls(settings)
loop = asyncio.get_event_loop()
if url_lst:
    tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
                 for data in url_lst
                 for func, key in parsers]
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        data = err.data.get('Errors', [])
        err.data['Errors'].extend(data)
        err.save()
    else:
        Error(data={'Errors': errors}).save()

ten_days_ago = dt.date.today() - dt.timedelta(10)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
