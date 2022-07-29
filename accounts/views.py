from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import Http404
from .models import Address
from .serializers import AddressSerializer


# Create your views here.
class AddressController(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, user):
        try:
            return Address.objects.filter(user__email=user)
        except Exception:
            raise Http404

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("--------Error adding address :", e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        addresses = self.get_object(request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
