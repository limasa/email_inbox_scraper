from rest_framework import serializers
from scraper.models import Email_Data


class EmailDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email_Data
        fields = (
            'portal',
            'email',
            'reference',
            'message',
            'name',
            'tel',
            'price')
