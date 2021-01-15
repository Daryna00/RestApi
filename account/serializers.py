from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'customer_card', 'password', 'name', 'unique_id']

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.customer_card = validated_data.get('customer_card', instance.customer_card)
        instance.name = validated_data.get('name', instance.name)
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()

        return instance
