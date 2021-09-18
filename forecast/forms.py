from django import forms
from .models import Race,Predict


class RaceSearchForm(forms.ModelForm):
    class Meta: 
        model = Race
        fields = ('race_date', 'race_park', 'race_number')


    race_date = forms.DateField(label='日付', widget=forms.DateInput(attrs={"type": "date"}),input_formats=['%Y-%m-%d'],required=True)
    race_park = forms.ChoiceField(
        label='競馬場', choices=Race.RACE_PARK_CHOICES, required=True)
    race_number= forms.ChoiceField(label='レース番号',choices=Race.RACE_NUMBER_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["race_date"].widget.attrs["class"] = "form-control"
        self.fields["race_date"].widget.attrs["id"] = "race_date"
        self.fields["race_park"].widget.attrs["class"] = "form-control"
        self.fields["race_park"].widget.attrs["id"] = "race_park"
        self.fields["race_number"].widget.attrs["class"] = "form-control"
        self.fields["race_number"].widget.attrs["id"] = "race_number"


class UploadForm(forms.Form):
    testfile = forms.FileField()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["testfile"].widget.attrs["class"] = "form-control"
    #     self.fields["testfile"].widget.attrs["id"] = "testfile"




# RaceSearchFormSet = forms.formset_factory(RaceSearchForm, extra=1)
