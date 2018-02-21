from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from social_django.models import UserSocialAuth
from django.utils import timezone
from django.http import HttpResponseRedirect

from polarization.accounts.models import Node
from polarization.search.models import Search, Tweet


class SearchView(View, LoginRequiredMixin):
    login_url = '/login/'

    def get(self, request):
        social_auth = UserSocialAuth.objects.filter(user=self.request.user).first()
        nodes = Node.objects.filter(created_by=social_auth)
        searches = Search.objects.filter(created_by=social_auth)
        search_ids = list(searches.values_list("id", flat=True))
        print(search_ids)
        tweets = Tweet.objects.filter(search_id__in=search_ids)
        return render(request, 'search/search.html', {
            "nodes": nodes,
            "searches": searches,
            "tweets": tweets
        })


class CreateSearchView(View, LoginRequiredMixin):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'search/add_search.html')

    def post(self, request):
        social_auth = UserSocialAuth.objects.filter(user=self.request.user).first()
        Search.objects.create(
            keyword=request.POST["keyword"],
            language=request.POST["language"],
            start_date=timezone.now(),
            finish_date=timezone.now() + timezone.timedelta(days=7),
            created_by=social_auth,
        )
        return HttpResponseRedirect(request.path_info)
