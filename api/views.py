from rest_framework import generics
from scraper.models import Email_Data
from .serializers import EmailDataSerializer


class EmailDataAPIView(generics.ListAPIView):
    queryset = Email_Data.objects.all()
    serializer_class = EmailDataSerializer
