from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home(request):
    city = request.GET.get('city')
    language = request.GET.get('language')
    form = FindForm()
    # qs = Vacancy.objects.all()
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'scrapping_app/home.html', {'object_list': qs, 'form': form})
