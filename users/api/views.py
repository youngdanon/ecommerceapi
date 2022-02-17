from rest_framework.views import APIView, Response
from .serializers import UserSerializer, AddressSerializer
from users.models import User, Address


class UserListView(APIView):
    def get(self, request):
        users_list = User.objects.all()
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data)


class UserView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({'error': 'User not found'}, exception=True, status=404)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({'error': 'User not found'}, exception=True, status=404)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'details': serializer.errors}, exception=True, status=400)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({'error': 'User not found'}, exception=True, status=404)
        user.delete()
        return Response(status=204)


class UserCreateView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = User.objects.create(**data)
            return Response(UserSerializer(user).data, status=200)
        else:
            return Response({'details': serializer.errors}, exception=True, status=409)


class AddressView(APIView):
    def get(self, request, user_id):
        try:
            address = Address.objects.get(user=user_id)
        except:
            return Response({'error': 'Address not found'}, exception=True, status=404)

        return Response(AddressSerializer(address).data, status=200)

    def post(self, request, user_id):
        data = request.data
        data.update({'user': user_id})
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            address = Address.objects.create(**data)
            return Response(AddressSerializer(address).data, status=200)
        else:
            return Response({'details': serializer.errors}, exception=True, status=409)

    def patch(self, request, user_id):
        try:
            address = Address.objects.get(user=user_id)
        except:
            return Response({'error': 'Address not found'}, exception=True, status=404)
        data = request.data
        serializer = AddressSerializer(address, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'details': serializer.errors}, exception=True, status=400)

    def delete(self, request, user_id):
        try:
            address = Address.objects.get(user=user_id)
        except:
            return Response({'error': 'Address not found'}, exception=True, status=404)
        address.delete()
        return Response(status=204)
