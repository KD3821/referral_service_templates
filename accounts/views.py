from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .models import User
from .serializers import LoginSerializer, CodeSerializer
from service.serializers import InviteCodeSerializer


class LoginView(APIView):
    swagger_schema = None
    render_classes = [TemplateHTMLRenderer]

    def get(self, request):
        logout(request)

        serializer = LoginSerializer()

        return Response({'serializer': serializer},  template_name='user_login.html')


class VerifyView(APIView):
    swagger_schema = None
    render_classes = [TemplateHTMLRenderer]

    def get(self, request):
        serializer = CodeSerializer()

        return Response(
            {
                'serializer': serializer.data,
                'error': request.data.get('error')
            },
            template_name='user_login.html'
        )

    def post(self, request):
        phone = request.data.get('phone')

        code_serializer = CodeSerializer()

        phone_serializer = LoginSerializer(data={'phone': phone})

        phone_serializer.is_valid(raise_exception=True)

        validated_data = phone_serializer.validated_data

        if not validated_data.get('error'):
            tmp_user_data = phone_serializer.save()

            return Response(
                {
                    'serializer': code_serializer,
                    'passcode': tmp_user_data.get('passcode'),
                    'phone': tmp_user_data.get('phone')
                },
                template_name='user_code.html'
            )
        return Response(
            {
                'serializer': phone_serializer,
                'error': validated_data.get('error')
            },
            template_name='user_login.html'
        )


class HomeView(APIView):
    swagger_schema = None
    render_classes = [TemplateHTMLRenderer]
    template_name = 'start.html'

    def get(self, request, *args, **kwargs):
        phone = kwargs.get('phone')

        try:
            user = User.objects.filter(phone=phone)[:1].get()

            login(request, user)

            invited_users = User.objects.filter(is_invited=True, invitecode=user.referralcode)

        except User.DoesNotExist:
            return Response(
                {
                    'serializer': LoginSerializer(),
                    'error': 'Требуется авторизация'
                },
                template_name='user_login.html')

        return Response(
            {
                'serializer': InviteCodeSerializer(),
                'user': user,
                'invited_users': invited_users
            }
        )

    def post(self, request):
        data = request.data

        if not data.get('passcode'):
            return Response(
                {
                    'serializer': LoginSerializer(),
                    'error': 'Введен некорректный код'
                },
                template_name='user_login.html'
            )

        code_serializer = CodeSerializer(data={'passcode': data.get('passcode')})

        code_serializer.is_valid(raise_exception=True)

        validated_data = code_serializer.validated_data

        if not validated_data.get('error'):
            validated_data['phone'] = data.get('phone')

            user_data = code_serializer.save()

            if not isinstance(user_data, User):
                return Response(
                    {
                        'serializer': LoginSerializer(),
                        'error': user_data.get('error')
                    },
                    template_name='user_login.html'
                )

            user = authenticate(phone=user_data.phone, password=data.get('passcode'))

            login(request, user)

            invited_users = User.objects.filter(is_invited=True, invitecode=user.referralcode)

            invitecode_serializer = InviteCodeSerializer()

            return Response(
                {
                    'serializer': invitecode_serializer,
                    'user': user,
                    'invited_users': invited_users
                },
                template_name='start.html'
            )

        return Response(
            {
                'serializer': LoginSerializer(),
                'error': validated_data.get('error')
            },
            template_name='user_login.html'
        )
