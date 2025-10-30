import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server import util


def books_get():  # noqa: E501
    """Get all books

     # noqa: E501


    :rtype: Union[List[Book], Tuple[List[Book], int], Tuple[List[Book], int, Dict[str, str]]
    """
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """Add a new book

     # noqa: E501

    :param book: 
    :type book: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    book = body
    if connexion.request.is_json:
        book = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
