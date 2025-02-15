from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id', None)
        if account_id:
            return Destination.objects.filter(account__account_id=account_id)
        return Destination.objects.all()


@api_view(['POST'])
def incoming_data(request):
    if request.method == 'POST':
        if not request.headers.get('CL-X-TOKEN'):
            return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

        app_secret_token = request.headers['CL-X-TOKEN']
        account = get_object_or_404(Account, app_secret_token=app_secret_token)

        data = request.data
        if not isinstance(data, dict):
            return Response({"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

        destinations = Destination.objects.filter(account=account)
        for destination in destinations:
            headers = destination.headers
            if destination.http_method == 'GET':
                response = requests.get(destination.url, params=data, headers=headers)
            else:
                response = requests.request(destination.http_method, destination.url, json=data, headers=headers)
            # Handle response if needed

        return Response({"status": "Data sent to destinations"}, status=status.HTTP_200_OK)