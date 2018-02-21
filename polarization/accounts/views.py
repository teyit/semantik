from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from rest_framework.generics import CreateAPIView
from social_django.models import UserSocialAuth

from .serializers import NodeSerializer
from .models import Node


class CreateNodeView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = NodeSerializer


class HomeView(View, LoginRequiredMixin):
    login_url = '/login/'

    def get(self, request):
        social_auth = UserSocialAuth.objects.filter(user=self.request.user).first()
        nodes = Node.objects.filter(created_by=social_auth)
        return render(request, 'accounts/home.html', {'nodes': nodes})


class NodeView(View, LoginRequiredMixin):
    login_url = '/login/'

    def get(self, request):
        created_by = UserSocialAuth.objects.filter(user=self.request.user)
        nodes = Node.objects.filter(created_by=created_by)
        return render(request, 'accounts/node.html', {'nodes': nodes})

    def post(self, request):
        handle = request.POST["username"]
        created_by = UserSocialAuth.objects.filter(user=self.request.user).first()
        Node.objects.create(handle=handle, created_by=created_by)
        nodes = Node.objects.filter(created_by=created_by)
        return HttpResponseRedirect(request.path_info)
