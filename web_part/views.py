from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from web_part.tasks import update_info, get_info_csv, get_info_xlsx
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
    context = {'message': message}
    return render(request, 'main.html',  context)


def file_upload(request):
    if request.method == 'POST':
        # Загрузка и сохранение файла
        try:
            uploaded_file = request.FILES['myfile']
            FileSystemStorage().save(uploaded_file.name, uploaded_file)
            # Распаковка аdрхива и обработка файлов из него
            update_info.delay(uploaded_file.name)
            request.session['message'] = 'Началась обработка файла'
        except BaseException:
            request.session['message'] = 'Ошибка. Файл не выбран'
    return HttpResponseRedirect('/')


def file_export_csv(request):
    try:
        get_info_csv.delay()
        request.session['message'] = 'Началась обработка файла'
    except BaseException:
        request.session['message'] = 'Ошибка.'
    return HttpResponseRedirect('/')



def file_export_xlsx(request):
    try:
        get_info_xlsx.delay()
        request.session['message'] = 'Началась обработка файла'
    except BaseException:
        request.session['message'] = 'Ошибка.'
    return HttpResponseRedirect('/')


