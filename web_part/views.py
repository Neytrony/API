import datetime
import os
import shutil

from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from web_part.models import Files
from web_part.tasks import update_info, get_info_csv, get_info_xlsx
from web_part.decorators import log_clearMediaDirs
# Create your views here.


def get_session_message(request):
    try:
        message = request.session.get('message')
        try:
            del request.session['message']
        except KeyError:
            pass
    except BaseException:
        message = 'Error'
    return message


@login_required(login_url='login')
def MainPage(request):
    # Получение списков файлов, которые нужно отобразить(есть в базе данных)
    message = get_session_message(request)
    files = Files.objects.all()
    update_status(files.exclude(status='SUCCESS'))
    context = {'message': message, 'files': files.order_by('-createdAt')}
    return render(request, 'main.html',  context)


@log_clearMediaDirs('import/')
def file_import(request):
    if request.method == 'POST':
        # Загрузка и сохранение файла
        try:
            uploaded_file = request.FILES['myfile']
            fileName = uploaded_file.name
            FileSystemStorage().save(f'import/{fileName}', uploaded_file)
            task = update_info.delay(fileName)
            task_result = AsyncResult(task.id)
            Files.objects.create(name=fileName, type=2, fileField=f'import/{fileName}', task_id=task.id, status=task_result.status)
            request.session['message'] = 'Началась обработка файла'
        except BaseException:
            request.session['message'] = 'Ошибка. Файл не выбран'
    return HttpResponseRedirect('/')


@log_clearMediaDirs('export/')
def file_export_csv(request):
    try:
        now = datetime.datetime.now()
        fileName = f'YcToBp_{now}.csv'
        task = get_info_csv.delay(fileName)
        task_result = AsyncResult(task.id)
        Files.objects.create(name=fileName, type=1, fileField=f'export/{fileName}', task_id=task.id, status=task_result.status)
        request.session['message'] = 'Началась обработка файла'
    except BaseException:
        request.session['message'] = 'Ошибка.'
    return HttpResponseRedirect('/')



@log_clearMediaDirs('export/')
def file_export_xlsx(request):
    try:
        now = datetime.datetime.now()
        fileName = f'YcToBp_{now}.xlsx'
        task = get_info_xlsx.delay(fileName)
        task_result = AsyncResult(task.id)
        Files.objects.create(name=fileName, type=1, fileField=f'export/{fileName}', task_id=task.id, status=task_result.status)
        request.session['message'] = 'Началась обработка файла'
    except BaseException:
        request.session['message'] = 'Ошибка.'
    return HttpResponseRedirect('/')


def update_status(files):
    for file in files:
        task_result = AsyncResult(file.task_id)
        file.status = task_result.status
        file.save()



