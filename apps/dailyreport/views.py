from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from system.mixin import LoginRequiredMixin


class myReportView(LoginRequiredMixin, View):
    """我的报告模型类"""
    def get(self, request):
        return render(request, 'dailyreport/myreport.html')
