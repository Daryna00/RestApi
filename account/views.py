from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-id')

    def get_permissions(self):
        permission = AllowAny() if self.action in ('create',) else IsAdminUser()
        print(self.action)
        return [permission]


class UserView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({"user": serializer.data})


    def post(self, request):
        user = request.data.get("user")
        # Create an article from the above data
        serializer = UserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({"success": "User '{}' created successfully".format(user_saved.title)})


    def put(self, request, id):

        saved_user = get_object_or_404(User.objects.all(), id=id)
        data = request.data.get('user')
        serializer = UserSerializer(instance=saved_user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({
            "success": "User '{}' updated successfully".format(user_saved.title)
        })

    def delete(self, request, id):
        # Get object with this pk
        user = get_object_or_404(User.objects.all(), id=id)
        user.delete()
        return Response({
            "message": "User with id `{}` has been deleted.".format(id)
        }, status=204)
