#View
from django.views.generic import TemplateView,DetailView,CreateView,UpdateView,DeleteView,ListView
from django.shortcuts import render,HttpResponse,resolve_url,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.core.paginator import Paginator

#login
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

#model
from .models import Horse,Race,Predict,Result,BeforeComment,AfterComment

#form
from .forms import RaceSearchForm,UploadForm,BeforeCommentForm,AfterCommentForm,SearchForm,LoginForm,SignUpForm
from django.db.models import Q

#settings
from django.conf import settings
#モジュール
from .func import calc_predict, select_sql_r, select_sql_h, making_predtable, insert_predtable,search_sql,insert_race_card
from .race_card import ShutubaTable as st

#その他ライブラリ
import json,io,bz2,pickle,datetime
import pandas as pd
from collections import OrderedDict

#index
class Index(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self,*args ,**kwargs):
        context = super().get_context_data(**kwargs)
        race_list = Race.objects.all().latest('race_date')
        race_date_last = race_list.response_race_date()
        race_list_last= Race.objects.filter(race_date = race_date_last).all().order_by('race_id')
        context = {
            "race_list":race_list_last,
        }
        return context

#concept
class Concept(TemplateView):
    template_name = 'app/concept.html'


#race
class Racelist(TemplateView):
    template_name = 'app/race.html'
    model = Race

    def get_context_data(self,*args ,**kwargs):
        context = super().get_context_data(**kwargs)
        race_list = Race.objects.all().latest('race_date')
        race_date_last = race_list.response_race_date()
        race_list_last= Race.objects.filter(race_date = race_date_last).all().order_by('race_id')
        context = {
            "race_list":race_list_last,
        }

        return context

#race_detail
class RaceDetail(LoginRequiredMixin,DetailView):
    template_name = 'app/race_detail.html' 

    model = Race
    slug_field = 'race_id'
    slug_url_kwarg = 'race_id'

    def get_context_data(self, *args ,**kwargs):
        detail_data = Race.objects.get(race_id = self.kwargs['race_id'])
        race_date = detail_data.race_date
        race_park = detail_data.race_park
        race_number = detail_data.race_number 
        race_id,df_pre,df_lat,df_re = search_sql(race_date, race_park, race_number)
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
        return context

@csrf_exempt
def search(request):
    if request.method == "POST" and request.body :
        race_date = request.POST.get("race_date")
        race_park = request.POST.get("race_park")
        race_number = request.POST.get("race_number")
        race_id,df_pre,df_lat,df_re = search_sql(race_date, race_park, race_number)
        
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

#dashboard
def Dashboard(request):
    return render(request, 'app/dashboard.html')

#timeline
class Timeline(ListView):
    template_name = 'app/timeline.html'
    context_object_name = 'forecast_list'

    paginate_by = 5
    
    def get_queryset(self):
        return BeforeComment.objects.all().order_by('-created_at')

class ChoiceRace(LoginRequiredMixin,TemplateView):
    template_name = 'app/choice_race.html'
    model = Race

    def get_context_data(self,*args ,**kwargs):
        context = super().get_context_data(**kwargs)
        race_list = Race.objects.all().latest('race_date')
        race_date_last = race_list.response_race_date()
        race_list_last= Race.objects.filter(race_date = race_date_last).all()
        # race_list=[race.race_id for race in race_list_last]
        race_park_held=[race.race_park for race in race_list_last]
        race_park_held=list(OrderedDict.fromkeys(race_park_held).keys())

        context = {
            "race_park_held":race_park_held,
            "race_list":race_list_last,
        }
        return context

class OnlyMyPostMinin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        beforecomment = BeforeComment.objects.get(id = self.kwargs['pk'])
        return beforecomment.author==self.request.user


class CreateBeforeComment(LoginRequiredMixin,CreateView):
    form_class = BeforeCommentForm
    template_name = 'app/create_beforecomment.html'
    model = BeforeComment

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(CreateBeforeComment,self).form_valid(form)


    def get_success_url(self):
        messages.success(self.request,"予想を投稿しました")
        return resolve_url('forecast:timeline')

    def get_form_kwargs(self):
        kwargs = super(CreateBeforeComment,self).get_form_kwargs()
        kwargs['race_id'] = self.request.path.split('/')[-1] #service_idはパラメータ
        return kwargs


class DetailBeforeComment(LoginRequiredMixin,DetailView):
    template_name = 'app/detail_beforecomment.html' 
    model = BeforeComment

    def get_context_data(self, *args ,**kwargs):
        detail_data = BeforeComment.objects.get(id=self.kwargs['pk'])
        race_data = Race.objects.values('race_id','race_date','race_park','race_number','race_name').get(race_id = detail_data.race)
        race_data["race_date"] = datetime.datetime.strptime(race_data["race_date"], "%Y/%m/%d")
        comment_data = AfterComment.objects.filter(comment=self.kwargs['pk']).all()
        params = {
            'object':detail_data,
            'race':race_data,
            'comment_list':comment_data
        }
        return params

class UpdateBeforeComment(OnlyMyPostMinin,UpdateView):
    model = BeforeComment
    form_class = BeforeCommentForm
    template_name = 'app/create_beforecomment.html'

    def get_success_url(self):
        messages.success(self.request,"予想を更新しました")
        return resolve_url('forecast:timeline')

    def get_form_kwargs(self):
        kwargs = super(UpdateBeforeComment,self).get_form_kwargs()
        comment = self.object
        target_comment = BeforeComment.objects.get(pk=comment.pk)
        kwargs["race_id"] = target_comment.race.race_id
        return kwargs

class DeleteBeforeComment(OnlyMyPostMinin,DeleteView):
    template_name = 'app/beforecomment_confirm_delete.html' 
    model = BeforeComment

    def get_success_url(self):
        messages.info(self.request,"予想を削除しました。")
        return resolve_url('forecast:timeline')

class CreateAfterComment(OnlyMyPostMinin,CreateView):
    form_class = AfterCommentForm
    template_name = 'app/create_aftercomment.html'
    model = AfterComment

    def form_valid(self, form):
        before_pk = self.kwargs['pk']
        before = get_object_or_404(BeforeComment, pk=before_pk)
        after = form.save(commit=False)
        after.comment = before
        after.save()
        messages.success(self.request,"レース回顧を投稿しました。")
        return redirect('forecast:detail_beforecomment', pk=before_pk)
 

    def get_form_kwargs(self):
        kwargs = super(CreateAfterComment,self).get_form_kwargs()
        comment_id = self.request.path.split('/')[-1] #service_idはパラメータ
        target_comment = BeforeComment.objects.get(pk=comment_id)
        
        kwargs['race_id'] = target_comment.race_id
        return kwargs
    

class DeleteAfterComment(OnlyMyPostMinin,DeleteView):
    template_name = 'app/aftercomment_confirm_delete.html' 
    model = AfterComment


    def get_success_url(self):
        messages.info(self.request,"コメントを削除しました。")
        return resolve_url('forecast:timeline')

def search_forecast(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST) 

        if searchform.is_valid():
           freeword = searchform.cleaned_data['freeword'] 
           search_list = BeforeComment.objects.filter(Q(race__race_name__icontains = freeword) | Q(favorite_horse__icontains = freeword) |Q(longshot_horse_1__icontains = freeword) |Q(longshot_horse_2__icontains = freeword) |Q(longshot_horse_3__icontains = freeword)).all().order_by('-updated_at')
           params = {
                'search_list':search_list,
           }
        return render(request, 'app/forecast_search.html',params)

#login
class Login(LoginView):
    form_class= LoginForm
    template_name = 'app/login.html'

#logout
class Logout(LogoutView):
    template_name = 'app/logout.html'

#signup
class SignUp(CreateView):
    form_class= SignUpForm
    template_name = 'app/signup.html'
    success_url = reverse_lazy('forecast:index')

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        self.object = user
        messages.info(self.request,'ユーザ登録をしました。')
        return HttpResponseRedirect(self.get_success_url())

#manage
def manage(request):
    testfile = UploadForm()
    return render(request, "app/manage.html", {'form': testfile})

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
        messages.success(request, 'スクレイピングに成功しました')
        return HttpResponseRedirect(reverse('forecast:manage'))
    else:
        messages.error(request, 'スクレイピングに失敗しました')



#現在使用していない
def Table(request):
    sc = SthreeController(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY,settings.AWS_S3_REGION_NAME,settings.AWS_STORAGE_BUCKET_NAME)
    df = sc.read_s3file()
    # array = [io.TextIOWrapper(io.BytesIO(s3obj['Body'].read())) for s3obj in s3objs]
    # print(s3objs)
    
    head = df.tail()
    df_ex = head.to_html()
    return HttpResponse(df_ex)




    # return JsonResponse(context, safe=False)

def judgecomment(request):
    if request.method == "POST":
        race_id = request.POST.get("race_id")
        
        detail_data = Result.objects.filter(race_id = race_id).values()
        data_list = [data for data in detail_data]
        rank_list =[data["rank"] for data in data_list]
        context ={"rank_list":rank_list}
        # print(detail_data)
        # print(rank_list)
        return JsonResponse(context, safe=False)
        # race_date = detail_data.race_date
        # race_park = detail_data.race_park
        # race_number = detail_data.race_number 



#バグ確認
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



