from time import sleep

from trellio2.base import View
from trellio2.response import json_response


async def test_view(request):
    sleep(1)
    return json_response({'test': 'success', "sleep": True})


class TestView(View):
    async def get(self, request):
        return json_response({'test': 'success', 'class_based': True})
