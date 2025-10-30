import connexion
import six

from swagger_server.models.book import Book  # noqa: E501
from swagger_server import util


def books_get():  # noqa: E501
    """Get all books

     # noqa: E501


    :rtype: List[Book]
    """
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """Add a new book

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
