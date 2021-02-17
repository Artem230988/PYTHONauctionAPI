from django.core.mail import send_mail
from rest_framework import serializers
from .models import *
from .tasks import send_spam_email, summa


class LotSerializer(serializers.ModelSerializer):

    owner = serializers.CharField(source='owner.username')
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    current_buyer = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Lot
        fields = ('id', 'title', 'description', 'category', 'closed_date', 'starting_rate', 'current_rate', 'owner', 'current_buyer' )


class LotCreateSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.owner = self.context['request'].user
        instance.save()
        return instance

    class Meta:
        model = Lot
        fields = ('title', 'description', 'category', 'closed_date', 'starting_rate')


class LotUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lot
        fields = ('title', 'description', 'category', 'closed_date', )


class UpdateRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lot
        fields = ('current_rate', )

    def validate(self, data):
        if data['current_rate'] < self.instance.current_rate or data['current_rate'] < self.instance.starting_rate:
            raise serializers.ValidationError("ставка должна быть выше текущей и начальной ставок")
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.current_buyer = self.context['request'].user
        instance.save()
        send_spam_email.delay(instance.owner.email)
        return instance