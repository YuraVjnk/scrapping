from django import forms
from scrapping_app.models import City, Language


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={
                                      'class': 'form-select'
                                  }
                                  ),
                                  label='Город'
                                  )
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={
                                          'class': 'form-select'
                                      }), label='Специальность')

    def __init__(self, *args, **kwargs):
        super(FindForm, self).__init__(*args, **kwargs)
        self.fields['city'].empty_label = 'Выберите город'
        self.fields['language'].empty_label = 'Выберите специальность'
