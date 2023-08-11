from rest_framework import serializers
from accounts.models import User


class InviteCodeSerializer(serializers.Serializer):
    invitecode = serializers.CharField(label='', style={'placeholder': 'Введите инвайт-код'})

    def validate(self, data):
        invitecode = data.get('invitecode')

        if len(str(invitecode)) != 6:
            data['error'] = 'Инвайт-код состоит из 6 символов'
        else:
            try:
                User.objects.filter(referralcode=data.get('invitecode'))[:1].get()
            except User.DoesNotExist:
                data['error'] = 'Приглашающий не найден'
        return data

    def create(self, validated_data):
        invitecode = validated_data.get('invitecode')

        inviter = User.objects.filter(referralcode=invitecode)[:1].get()

        inviter.is_verified = True
        inviter.save()

        return inviter
