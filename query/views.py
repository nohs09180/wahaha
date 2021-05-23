from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from .models import Query
from .forms import QueryForm

User = get_user_model()

def top(request):
    form = QueryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            query = form.save()
            admin = User.objects.filter(first_name='admin', is_superuser=True)[0]
            context = {
                # 'name': query.name,
                'subject': query.subject,
                'contents': query.contents,
            }
            subject = render_to_string('query/mail_templates/subject.txt', context)
            message = render_to_string('query/mail_templates/message.txt', context)
            # send_mail(subject, message, None, [admin.email])
            return redirect('query:success')
    context = {
        'form': form,
    }
    return render(request, 'query/top.html', context)

def success(request):
    return render(request, 'query/success.html')