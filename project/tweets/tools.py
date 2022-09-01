import pathlib

from django.http import QueryDict


def get_file_extension(file):
    return pathlib.Path(file).suffix


def add_image_to_request(url, request_data):
    if isinstance(request_data, QueryDict):
        request_data._mutable = True
        request_data["image"] = url
        request_data._mutable = False
        return
    request_data['image'] = url