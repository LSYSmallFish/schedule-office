from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import get_user_model
# Create your views here.
from system.mixin import LoginRequiredMixin
from .models import DailyReport
from .forms import dailyReportForm
from django.http import HttpResponse
import json
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
import re
from datetime import datetime, timedelta
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

User = get_user_model()


class myReportView(LoginRequiredMixin, View):
    """我的报告模型类"""

    def get(self, request):
        ret = dict()
        my_report_all = DailyReport.objects.filter(user=int(request.user.id))

        attention_all = DailyReport.objects.filter(attention__id=int(request.user.id))
        ret['my_report_all'] = my_report_all | attention_all
        print(attention_all)
        return render(request, 'dailyreport/myreport.html', ret)


@method_decorator(xframe_options_exempt, name='dispatch')
class reportCreateView(LoginRequiredMixin, View):
    """添加日程模型类"""

    def get(self, request):
        ret = dict()
        category_all = [{'key': i[0], 'value': i[1]} for i in DailyReport.cat_choices]
        user_all = User.objects.exclude(username__in=['admin', request.user.username])
        ret['category_all'] = category_all
        ret['user_all'] = user_all
        print(user_all)
        # 新增内容，接收前端传递过来的calDate内容，并对时间进行处理
        if 'calDate' in request.GET and request.GET['calDate']:
            calDate = re.split('[-: ]', request.GET['calDate'])
            Y, M, D, h, m = map(int, calDate)
            start_time = datetime(Y, M, D, h, m)
            end_time = start_time + timedelta(hours=1)
            ret['start_time'] = start_time
            ret['end_time'] = end_time
        return render(request, 'dailyreport/report_create.html', ret)

    def post(self, request):
        res = dict(result=False)
        daily_report_form = dailyReportForm(request.POST)
        if daily_report_form.is_valid():
            daily_report_form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')

@method_decorator(xframe_options_exempt, name='dispatch')
class reportDetailView(LoginRequiredMixin, View):
    """
    日报详情模型类
    """

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            category_all = [{'key': i[0], 'value': i[1]} for i in DailyReport.cat_choices]
            report = get_object_or_404(DailyReport, pk=int(request.GET['id']))
            user_all = User.objects.exclude(id=report.id)
            ret['category_all'] = category_all
            ret['user_all'] = user_all
            ret['report'] = report
        return render(request, 'dailyreport/report_detail.html', ret)
    def post(self, request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            daily_report = get_object_or_404(DailyReport, pk=int(request.POST['id']))
            daily_report_form = dailyReportForm(request.POST, instance=daily_report)
            if daily_report_form.is_valid():
                daily_report_form.save()
                res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
