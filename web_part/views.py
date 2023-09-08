import datetime

from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from api.models import YcToBp, BpToYc
from apiSout.models import SoutToAc, Employee
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
        with open('mediafiles/logs/error.log', 'w') as f:
            f.write(str(request.POST))
            f.write('\n')
            f.write(str(dict(request.POST)['file_type_choice'][0]))
            f.write('\n')
        file_processing(request, FILE_TYPE_CHOICES[dict(request.POST)['file_type_choice'][0]], TABLE_CHOICES[dict(request.POST)['model_choice'][0]])
    return HttpResponseRedirect('/')


def file_processing(request, func, model):
    try:
        with open('mediafiles/logs/error.log', 'w') as f:
            f.write('123')
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fileName = f'{model.__name__}_{now}.{func[1]}'
            f.write(f'{fileName}')
            task = func[0].delay(kwargs={'fileName': fileName, 'model': model})
            f.write(f'{func[0]}')
            f.write(f'{model.__name__}')
        task_result = AsyncResult(task.id)
        Files.objects.create(name=fileName, type=1, task_id=task.id, status=task_result.status)
        request.session['message'] = 'Началась обработка файла'
    except BaseException:
        request.session['message'] = 'Ошибка.'
    return HttpResponseRedirect('/')


TABLE_CHOICES = {
    '1': YcToBp,
    '2': BpToYc,
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
