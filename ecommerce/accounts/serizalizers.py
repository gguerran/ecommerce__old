from rest_framework import serializers

from ecommerce.accounts.models import User

PASS_DIDNT_MATCH = 'As senhas não são iguais'


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        ordering = ['created']
        fields = [
            'id', 'username', 'password1', 'password2'
        ]
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        if password == password2:
            user = User(**validated_data)
            user.is_active = True
            user.is_superuser = False
            user.set_password(password)
            user.save()
            return user
        raise serializers.ValidationError(PASS_DIDNT_MATCH)


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        ordering = ['created']
        fields = [
            'id', 'username'
        ]
        extra_kwargs = {'id': {'read_only': True}}
