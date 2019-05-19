from django import forms
from .models import Pizzeria


def get_Pizzeries():
    # you place some logic here
    Pizzerias = Pizzeria.objects.all()
    choices_list =[('0', '----')] + [(obj.id, obj.name) for obj in Pizzerias]
    return choices_list


class SelectPizzeriaForm(forms.Form):
    cfPizzeria = forms.ChoiceField(initial='0',
                                   widget=forms.Select(),
                                   required=True)

    def __init__(self, *args, **kwargs):
        super(SelectPizzeriaForm, self).__init__(*args, **kwargs)
        self.fields['cfPizzeria'] = forms.ChoiceField(
            choices=get_Pizzeries())

class OrderHeadForm(forms.Form):
    nameAndSurname = forms.CharField(max_length=60, label = 'Imię i nazwisko')
    street = forms.CharField(max_length=40, label = 'Ulica')
    streetNumber = forms.CharField(max_length=5, label = 'Numer budynku')
    houseNumber = forms.CharField(max_length=5, label = 'Numer lokalu')
    email = forms.CharField(max_length=30, label = 'Adres email')
    phoneNumber = forms.DecimalField(decimal_places=0, max_digits=9, label = 'Numer telefonu')



# Opis
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
# https://stackoverflow.com/questions/24403075/django-choicefield
# https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-choices
# https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model.get_FOO_display
# https://docs.djangoproject.com/en/2.2/topics/db/queries/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps
# https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_web_server
# https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_software_do_I_need
# https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Upload_files_to_a_web_server


