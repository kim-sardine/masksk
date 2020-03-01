from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from mask.core.utils import generate_random_string_digits
from mask.mailings.models import Mailing

def create_mailing(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not Mailing.objects.filter(email=email).exists():
                token = generate_random_string_digits(40)
                Mailing.objects.create(
                    email=email,
                    token=token,
                )
                messages.success(request, f'신청 완료. 이메일 : "{email}"')
            else:
                messages.error(request, f'이미 존재하는 이메일입니다. : "{email}"')

    return redirect(reverse('home'))


def revoke_mailing(request, token):
    mailing = get_object_or_404(Mailing, token=token)

    if request.method == 'GET':
        return render(request, 'mailing/revoke.html')
    elif request.method == 'POST':
        mailing.delete()
        messages.success(request, f'수신 거부가 완료되었습니다.')

    return redirect(reverse('home'))
