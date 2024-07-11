from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def first_page(request):
    return render(request, 'ByteMe_fp.html')


def second_page(request):
    return render(request,'ByteMe_sp.html')


def third_page(request):
    return render(request,'ByteMe_tp.html')

def intro_page(request):
    return render(request,'ByteMe_Intro.html')


from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import pandas as pd
import os
from .greedy_scheduling import main
from openpyxl import  load_workbook

# 定义保存处理后文件的路径
PROCESSED_FILE_PATH =  'processed_data.xlsx'

def handle_excel_upload(request):
    global PROCESSED_FILE_PATH
    # 处理 POST 请求，确保有文件上传
    if request.method == 'POST' and request.FILES['fileInput']:
        # 获取上传的 Excel 文件对象
        excel_file = request.FILES['fileInput']
    else:
        return   HttpResponse('No file provided')

    if excel_file:#如果获取到文件对象
        # 检查上传文件格式是否为 .xlsx 或 .xls
        if excel_file.name.endswith('.xlsx') or excel_file.name.endswith('.xls'):
            # 在这里调用 main 函数进行数据处理
            main(excel_file)
            if PROCESSED_FILE_PATH and os.path.exists(PROCESSED_FILE_PATH):
                # 返回生成的 Excel 文件给用户下载
                #打开生成的 Excel 文件，并构建 HTTP 响应对象
                with open(PROCESSED_FILE_PATH, 'rb') as f:
                    #设置响应内容类型为 Excel 文件。
                    response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    #设置响应的文件下载名称
                    response['Content-Disposition'] = 'attachment; filename="processed_data.xlsx"'
                    return response
    else:
        # 添加调试信息
        print("File not found")
        return HttpResponse('No file')
    # 如果是 GET 请求或者没有文件上传，渲染指定的模板页面（假设为 your_template.html）
    return render(request, 'ByteMe_sp.html')

def handle_excel_download(request):
    # 获取模板文件的路径
    template_file_path = os.path.join(settings.BASE_DIR, 'main_app/templates/s_1.xlsx')

    # 检查模板文件是否存在
    if os.path.exists(template_file_path):
        # 添加调试信息
        print(f"Template file found at {template_file_path}")

        # 返回模板文件给用户下载
        with open(template_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="s_1.xlsx"'
            return response
    else:
        # 添加调试信息
        print("Template file not found")
        return HttpResponse('No template file')

    # 如果是 GET 请求或者没有文件上传，渲染指定的模板页面
    return render(request, 'ByteMe_sp.html')



'''
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import pandas as pd
import os
from openpyxl import  load_workbook

# 定义保存处理后文件的路径
PROCESSED_FILE_PATH = 'processed_data.xlsx'

def handle_excel_upload(request):
    # 处理 POST 请求，确保有文件上传
    if request.method == 'POST' and request.FILES['fileInput']:
        # 获取上传的 Excel 文件对象
        excel_file = request.FILES['fileInput']
    else:
        return   JsonResponse('No file provided')

    if excel_file:#如果获取到文件对象
        # 检查上传文件格式是否为 .xlsx 或 .xls
        if excel_file.name.endswith('.xlsx') or excel_file.name.endswith('.xls'):
            # 使用 pandas 读取 Excel 文件数据
            df = pd.read_excel(excel_file)

            # 在这里进行数据处理，例如计算或其他操作
            # 这里只是一个简单示例，假设处理后的数据是取前几行作为示例
            processed_data = df.head()

            # 指定生成的新 Excel 文件名
            #output_filename = 'processed_data.xlsx'

            # 将处理后的数据保存为新的 Excel 文件
            processed_data.to_excel(PROCESSED_FILE_PATH, index=False)
            #return HttpResponse('Successfully processed')
        else:
            return HttpResponse('File format error')
    else:
        return   HttpResponse('No file provided')
    # 如果是 GET 请求或者没有文件上传，渲染指定的模板页面（假设为 your_template.html）
    return render(request, 'ByteMe_sp.html')

def handle_excel_download(request):
    if os.path.exists(PROCESSED_FILE_PATH):
        # 返回生成的 Excel 文件给用户下载
        #打开生成的 Excel 文件，并构建 HTTP 响应对象
        with open(PROCESSED_FILE_PATH, 'rb') as f:
            #设置响应内容类型为 Excel 文件。
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            #设置响应的文件下载名称
            response['Content-Disposition'] = 'attachment; filename="processed_data.xlsx"'
            return response
    else:
        return HttpResponse('No file')
    # 如果是 GET 请求或者没有文件上传，渲染指定的模板页面（假设为 your_template.html）
    return render(request, 'ByteMe_sp.html')'''