from trellio2.urls import Blueprint, url
from .views import test_view, TestView

bp = Blueprint('polls', url_prefix='/v1/polls')
bp.url('/', test_view, 'get')

urlpatterns = [
    url('/test/', TestView.as_view())
]
