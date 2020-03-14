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

User = get_user_model()


class myReportView(LoginRequiredMixin, View):
    """我的报告模型类"""

    def get(self, request):
        return render(request, 'dailyreport/myreport.html')


class reportCreateView(LoginRequiredMixin, View):
    """添加日程模型类"""

    def get(self, request):
        ret = dict()
        category_all = [{'key': i[0], 'value': i[1]} for i in DailyReport.cat_choices]
        user_all = User.objects.exclude(username__in=['admin', request.user.username])
        ret['category_all'] = category_all
        ret['user_all'] = user_all
        return render(request, 'dailyreport/report_create.html', ret)

    def post(self, request):
        res = dict(result=False)
        daily_report_form = dailyReportForm(request.POST)
        if daily_report_form.is_valid():
            daily_report_form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
