from django import forms
from .models import PolicyHolder, InsuranceModel, EventModel
from .validators import email_validation


class PolicyHolderForm(forms.ModelForm):
    """
        Form for creating or updating Policyholder instances.

        This form is used to create new Policyholder instances or update existing ones. It
        includes fields for all the model's attributes and provides validation for
        those fields.

        :param forms.ModelForm: The base class for the form.
        :type forms.ModelForm: class
    """
    class Meta:
        model = PolicyHolder
        fields = ["name", "lastname", "birth_id", "cell_phone_no", "email",
                  "street", "street_no", "city", "country", "photo", "zip_code"]
        labels = {
            "name": 'Jméno: ',
            "lastname": 'Příjmení: ',
            "birth_id": 'Rodné číslo: ',
            "cell_phone_no": 'Telefon: ',
            "email": 'Email: ',
            "street": 'Ulice: ',
            "street_no": 'Č.p./orientační číslo: ',
            "city": 'Město: ',
            "country": 'Stát: ',
            "photo": 'Fotografie: ',
            "zip_code": 'PSČ:'
        }
    email = forms.EmailField(validators=[email_validation])
        
class InsuranceModelForm(forms.ModelForm):
    """
        Form for creating or updating InsuranceModel instances.

        This form is used to create new InsuranceModel instances or update existing ones. It
        includes fields for all the model's attributes and provides validation for
        those fields.

        :param forms.ModelForm: The base class for the form.
        :type forms.ModelForm: class
    """
    class Meta:
        model = InsuranceModel
        fields = ["paid_by", "insurance_type", "target_amount",
                  "insurance_object", "valid_from", "valid_to"]
        labels = {
            "paid_by": 'Uhrazeno kým: ',
            "insurance_type": 'Typ pojištění: ',
            "target_amount": 'Cílová částka',
            "insurance_object": 'Předmět pojištění',
            "valid_from": 'Platné od: ',
            "valid_to": 'Platné do: '
        }

class EventModelForm(forms.ModelForm):
    """
        Form for creating or updating EventModel instances.

        This form is used to create new EventModel instances or update existing ones. It
        includes fields for all the model's attributes and provides validation for
        those fields.

        :param forms.ModelForm: The base class for the form.
        :type forms.ModelForm: class
    """
    class Meta:
        model = EventModel
        fields = ["title", "contract_no", "event_date",
                  "desc", "attach1", "attach2"]

        labels = {
            "title": 'Název události: ',
            "contract_no": 'Číslo smlouvy: ',
            "event_date": 'Datum vzniku: ',
            "desc": 'Popis: ',
            "attach1": 'Příloha č.1: ',
            "attach2": 'Příloha č.2: '
        }

        widgets = {
            'desc': forms.Textarea(attrs={'cols': 25, 'rows': 10})
        }