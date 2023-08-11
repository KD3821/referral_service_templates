from rest_framework import serializers
from .models import passcode_generator
from passlib.hash import bcrypt

from .models import TemporaryUser, User


class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.DecimalField(max_digits=100, decimal_places=0, allow_null=True, label='Телефон')

    class Meta:
        model = TemporaryUser
        fields = ['phone']

    def validate(self, data):
        phone = data.get('phone')

        if not phone:
            data['error'] = 'Введите номер телефона (только цифры)'
        else:
            if len(phone.as_tuple().digits) != 11:
                data['error'] = 'Номер должен быть 11-значным'

        return data

    def create(self, validated_data):
        phone = validated_data.get('phone')

        passcode = passcode_generator()

        hashed_passcode = bcrypt.hash(passcode)

        try:
            tmp_user = TemporaryUser.objects.filter(phone=phone)[:1].get()

            tmp_user.passcode = hashed_passcode

            tmp_user.save()

        except TemporaryUser.DoesNotExist:
            try:
                user = User.objects.filter(phone=phone)[:1].get()

                user.passcode = hashed_passcode

                user.save()

            except User.DoesNotExist:
                TemporaryUser.objects.create(phone=phone, passcode=hashed_passcode)

        return {'phone': phone, 'passcode': passcode}


class CodeSerializer(serializers.Serializer):
    passcode = serializers.CharField(label='Код')

    def validate(self, data):
        passcode = data.get('passcode')

        if len(str(passcode)) != 4:
            data['error'] = 'Код должен быть 4-значным'

        return data

    def create(self, validated_data):
        passcode = validated_data.get('passcode')

        phone = validated_data.get('phone')

        try:
            tmp_user = TemporaryUser.objects.filter(phone=phone)[:1].get()

            if bcrypt.verify(str(passcode), tmp_user.passcode):
                new_passcode = bcrypt.hash(passcode_generator())

                user = User.objects.create(
                    phone=tmp_user.phone,
                    password=str(passcode),
                    passcode=new_passcode
                )

                tmp_user.delete()

                return user

        except TemporaryUser.DoesNotExist:
            try:
                user = User.objects.filter(phone=phone)[:1].get()

                if bcrypt.verify(str(passcode), user.passcode):
                    new_passcode = bcrypt.hash(passcode_generator())

                    user.password = str(passcode)

                    user.passcode = new_passcode

                    user.save()

                    return user

            except User.DoesNotExist:
                pass

        return {'error': 'Неверный код'}
