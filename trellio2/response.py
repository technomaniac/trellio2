from sanic import response


def json_response(data, status=200, headers=None, content_type="application/json"):
    '''
    Returns json response
    :param data:
    :param status:
    :param headers
    :param content_type
    :return:
    '''
    return response.json(body=data, status=status, headers=headers, content_type=content_type)


class Response(response.HTTPResponse):
    pass
