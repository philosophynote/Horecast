from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt 
from .models import Horse,Race,Predict
from django.http import JsonResponse, HttpResponseRedirect
from .forms import RaceSearchForm,UploadForm
import json,io,bz2,pickle
import pandas as pd
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from .func import calc_predict, select_sql_r, select_sql_h, making_predtable, insert_predtable,search_sql,insert_race_card
from .race_card import ShutubaTable as st
# from .dashboard import SthreeController
from django.conf import settings
# import fastparquet
# import s3fs,fsspec

@csrf_exempt
def scrape_rc(request):
    if request.method == "POST" and request.body :
        race_date = request.POST.get("race_date")
        race_year = request.POST.get("race_year")
        race_park = request.POST.get("race_park")
        race_count = request.POST.get("race_count")
        race_hold = request.POST.get("race_hold")
        race_id = f'{race_year}{race_park}{race_count}{race_hold}'
        race_id_list = ['{}{}'.format(race_id,str(i).zfill(2)) for i in range(1, 13, 1)]
        rc = st.scrape(race_id_list,race_date)
        
        rc.data.reset_index(inplace=True)
        rc.data.rename(columns={"index":"race_id"},inplace=True)
        insert_race_card(rc.data)
        messages.success(request, 'UPLOADに成功しました')
        return HttpResponseRedirect(reverse('forecast:manage'))
    else:
        messages.error(request, 'UPLOADに失敗しました')

def Table(request):
    sc = SthreeController(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY,settings.AWS_S3_REGION_NAME,settings.AWS_STORAGE_BUCKET_NAME)
    df = sc.read_s3file()
    # array = [io.TextIOWrapper(io.BytesIO(s3obj['Body'].read())) for s3obj in s3objs]
    # print(s3objs)
    
    head = df.tail()
    df_ex = head.to_html()
    return HttpResponse(df_ex)


class Index(TemplateView):
    template_name = 'index.html'

        #標準搭載されている関数
    def get_context_data(self,*args ,**kwargs):
        #おまじない
        context = super().get_context_data(**kwargs)
        #投稿された内容を作成日順に全てとってくる
        race_list= Race.objects.all().order_by('-race_date')
        context = {
            "post_list":race_list,
        }
        return context

class Timeline(TemplateView):
    template_name = 'timeline.html'

class Toppage(TemplateView):
    template_name = 'toppage.html'



def manage(request):
    testfile = UploadForm()
    return render(request, "manage.html", {'form': testfile})


def upload(request):
    if request.method == 'POST':
        upload = UploadForm(request.POST, request.FILES)
        if upload.is_valid():
            df = pd.read_csv(io.StringIO(
                request.FILES['testfile'].read().decode('utf-8')), delimiter=',')
            filename = bz2.BZ2File('forecast/HorecastModel.bz2', 'rb')
            lgb_clf = pickle.load(filename)
            pred, proba = calc_predict(lgb_clf,df)
            race_df = select_sql_r(df,"race")
            horse_df = select_sql_h(df,"horse")
            pred_table = race_df.merge(horse_df, left_on="race_id",
                               right_on="race_id", how="left")
            pred_table = making_predtable(pred, proba, pred_table)
            insert_predtable(pred_table)
            messages.success(request, 'UPLOADに成功しました')
            return HttpResponseRedirect(reverse('forecast:manage'))
        else:
            messages.error(request, 'UPLOADに失敗しました')
    else:
        pass
        


@csrf_exempt
def search(request):
    if request.method == "POST" and request.body :
        race_date = request.POST.get("race_date")
        race_park = request.POST.get("race_park")
        race_number = request.POST.get("race_number")
        df_pre,df_lat,df_re = search_sql(race_date, race_park, race_number)
        json_records_pre = df_pre.to_json(orient ='records')
        json_records_lat = df_lat.to_json(orient ='records')
        json_records_re = df_re.to_json(orient ='records')
        data_pre = []
        data_lat = []
        data_re = []
        data_pre = json.loads(json_records_pre)
        data_lat = json.loads(json_records_lat)
        data_re = json.loads(json_records_re)
        context = {'data_pre': data_pre,'data_lat': data_lat,'data_re': data_re}
    return JsonResponse(context, safe=False)

from django.views.decorators.csrf import requires_csrf_token
from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,)
@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)



