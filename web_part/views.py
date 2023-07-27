import datetime

from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from api.models import YcToBp
from apiSout.models import SoutToAc
from web_part.tasks import update_info, get_info_csv, get_info_xlsx, Files
from web_part.decorators import log_clearMediaDirs


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
    context = {'message': message, 'files': files.order_by('-createdAt'),}
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
def file_export(request):
    if request.method == 'POST':
        file_processing(request, FILE_TYPE_CHOICES[request.POST['file_type_choice']], TABLE_CHOICES[request.POST['model_choice']])
    return HttpResponseRedirect('/')


def file_processing(request, func, table):
    try:
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        fileName = f'{table.__name__}_{now}.{func[1]}'
        print(fileName)
        task = func[0].delay(fileName)
        task_result = AsyncResult(task.id)
        Files.objects.create(name=fileName, type=1, task_id=task.id, status=task_result.status)
        request.session['message'] = 'Началась обработка файла'
    except BaseException:
        request.session['message'] = 'Ошибка.'
    return HttpResponseRedirect('/')


TABLE_CHOICES = {
    '1': YcToBp,
    '2': SoutToAc,
}
FILE_TYPE_CHOICES = {
    '1': (get_info_xlsx, 'xlsx'),
    '2': (get_info_csv, 'csv')
}


def update_status(files):
    for file in files:
        task_result = AsyncResult(file.task_id)
        file.status = task_result.status
        file.save()
