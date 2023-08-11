from django.contrib.auth import login
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from accounts.models import User
from .serializers import InviteCodeSerializer



class InviteCodeView(APIView):
    swagger_schema = None
    render_classes = [TemplateHTMLRenderer]
    template_name = 'start.html'

    def get(self, request):
        return Response(
            {
                'serializer': InviteCodeSerializer(),
                'user': request.user,
                'invited_users': None,
                'error': 'error_msg'
            }
        )

    def post(self, request):
        invitecode = request.data.get('invitecode')

        user = User.objects.get(phone=request.data.get('phone'))

        login(request, user)

        invited_users = User.objects.filter(is_invited=True, invitecode=user.referralcode)

        if not invitecode or user.referralcode == invitecode:
            if not invitecode:
                error_msg = 'Введите инвайт-код'
            else:
                error_msg = 'Некорректый инвайт-код'
            messages.error(request, error_msg)
            return Response(
                {
                    'serializer': InviteCodeSerializer(),
                    'user': request.user,
                    'invited_users': invited_users,
                    'error': error_msg
                },
            )

        referral_user = invited_users.filter(referralcode=invitecode)

        if referral_user:
            messages.error(request, 'Для Вас инвайт-код не доступен')
            return Response(
                {
                    'serializer': InviteCodeSerializer(),
                    'user': request.user,
                    'invited_users': invited_users,
                    'error': 'Для Вас инвайт-код не доступен'
                },
            )

        referral_serializer = InviteCodeSerializer(data={'invitecode': invitecode})

        referral_serializer.is_valid(raise_exception=True)

        validated_data = referral_serializer.validated_data

        if validated_data.get('error'):
            messages.error(request, validated_data.get('error'))
            return Response(
                {
                    'serializer': InviteCodeSerializer(),
                    'user': user,
                    'invited_users': invited_users,
                    'error': validated_data.get('error')
                },
            )

        inviter = referral_serializer.save()

        user.invitecode = inviter.referralcode

        user.is_invited = True

        user.save()

        return Response(
            {
                'serializer': InviteCodeSerializer(),
                'user': user,
                'invited_users': invited_users
            }
        )
