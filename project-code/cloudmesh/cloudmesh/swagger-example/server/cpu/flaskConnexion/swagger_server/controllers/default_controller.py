import connexion
import six

from swagger_server.models.cpu import CPU  # noqa: E501
from swagger_server import util


def cpu_get():  # noqa: E501
    """cpu_get

    Returns cpu information of the hosting server # noqa: E501


    :rtype: CPU
    """
    return 'do some magic!'
