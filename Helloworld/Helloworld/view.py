from time import sleep
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
from datetime import datetime
from django.http import FileResponse
from django.utils import timezone
# import openai
from django.views.decorators.http import require_http_methods
from django.conf import settings
# from .models import history_event
from django.db import transaction
from django.shortcuts import render

@csrf_exempt
def test1(request):
    return render(request, 'ByteMe_fp.html')

@csrf_exempt
def second_page(request):
    return render(request,'ByteMe_sp.html')