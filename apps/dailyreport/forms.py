from django import forms
from .models import DailyReport


class dailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = '__all__'
