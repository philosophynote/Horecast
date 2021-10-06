from django import forms
from .models import Race,Horse,BeforeComment,AfterComment


class RaceSearchForm(forms.ModelForm):
    class Meta: 
        model = Race
        fields = ('race_date', 'race_park', 'race_number')

    race_date = forms.ModelChoiceField(Race.objects.distinct().values_list("race_date",flat=True).order_by('race_date'),required=True)
    # race_date = forms.DateField(label='日付', widget=forms.DateInput(attrs={"type": "date"}),input_formats=['%Y-%m-%d'],required=True)
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

class BeforeCommentForm(forms.ModelForm):
    class Meta:
        model = BeforeComment
        fields = ['race','favorite_horse', 'longshot_horse_1','longshot_horse_2','longshot_horse_3','forecast_reason']

    favorite_horse = forms.ModelChoiceField(queryset=None)
    longshot_horse_1 = forms.ModelChoiceField(label='紐馬１',queryset=None, required=False)
    longshot_horse_2 = forms.ModelChoiceField(label='紐馬２',queryset=None, required=False)
    longshot_horse_3 = forms.ModelChoiceField(label='紐馬３',queryset=None, required=False)


    def __init__(self,*args ,**kwargs):
        
        race_id = kwargs.pop('race_id')
            

        super().__init__(*args,**kwargs)

        self.fields['race'].initial = race_id
        
        self.fields['favorite_horse'].queryset = Horse.objects.filter(race_id=race_id)
        self.fields['longshot_horse_1'].queryset = Horse.objects.filter(race_id=race_id)
        self.fields['longshot_horse_2'].queryset = Horse.objects.filter(race_id=race_id)
        self.fields['longshot_horse_3'].queryset = Horse.objects.filter(race_id=race_id)
        self.fields['race'].widget = forms.HiddenInput()

class AfterCommentForm(forms.ModelForm):
    class Meta:
        model = AfterComment
        fields = ['race','after_comment', 'attention_horse','attention_reason']


    attention_horse = forms.ModelChoiceField(label='紐馬１',queryset=None, required=False)



    def __init__(self,*args ,**kwargs):
        race_id = kwargs.pop('race_id')
        print(race_id)
        super().__init__(*args,**kwargs)
        self.fields['race'].initial = race_id
        self.fields['attention_horse'].queryset = Horse.objects.filter(race_id=race_id)
        self.fields['race'].widget = forms.HiddenInput()

class SearchForm(forms.Form):
    freeword = forms.CharField(min_length = 1,max_length=30, label ='',required=False)

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
