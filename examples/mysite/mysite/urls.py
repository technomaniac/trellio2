from trellio2.urls import url, include

urlpatterns = [
    url('/polls', include('polls.urls'))
]
