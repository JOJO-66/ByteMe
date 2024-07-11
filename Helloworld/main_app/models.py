from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django import forms
class UploadFileForm(forms.Form):
    file=forms.FileField()


class s_0(models.Model):
    work_id = models.IntegerField()  # 工单号
    logistics_id = models.IntegerField()  # 物流编号
    num = models.IntegerField()  # 数量
    plan_start_date = models.DateField(null=True, blank=True)  # 计划开始日期
    plan_completion_date = models.DateField(null=True, blank=True)  # 计划完工日期
    #related_name='successor_work_orders' 允许你通过该名称访问与之关联的工单。
    predecessor_work_order = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='successor_work_orders')  # 前置工单
    priority = models.IntegerField()  # 优先级

    #__str__() 方法定义了模型实例的字符串表示，便于在管理界面和其他地方显示。
    def __str__(self):
        return f"Work Order: {self.work_id}"

    #Meta 类用于提供模型的元数据，如 verbose_name 和 verbose_name_plural 用于设置模型在管理界面中的显示名称。
    class Meta:
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'


