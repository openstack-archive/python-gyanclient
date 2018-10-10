#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import base64
import binascii
import json
import os
import re

from oslo_utils import netutils
import six
from six.moves.urllib import parse
from six.moves.urllib import request
from gyanclient.common.apiclient import exceptions as apiexec
from gyanclient.common import cliutils as utils
from gyanclient import exceptions as exc
from gyanclient.i18n import _



def common_filters(marker=None, limit=None, sort_key=None,
                   sort_dir=None, all_projects=False):
    """Generate common filters for any list request.

    :param all_projects: list models in all projects or not
    :param marker: entity ID from which to start returning entities.
    :param limit: maximum number of entities to return.
    :param sort_key: field to use for sorting.
    :param sort_dir: direction of sorting: 'asc' or 'desc'.
    :returns: list of string filters.
    """
    filters = []
    if all_projects is True:
        filters.append('all_projects=1')
    if isinstance(limit, int):
        filters.append('limit=%s' % limit)
    if marker is not None:
        filters.append('marker=%s' % marker)
    if sort_key is not None:
        filters.append('sort_key=%s' % sort_key)
    if sort_dir is not None:
        filters.append('sort_dir=%s' % sort_dir)
    return filters


def split_and_deserialize(string):
    """Split and try to JSON deserialize a string.

    Gets a string with the KEY=VALUE format, split it (using '=' as the
    separator) and try to JSON deserialize the VALUE.
    :returns: A tuple of (key, value).
    """
    try:
        key, value = string.split("=", 1)
    except ValueError:
        raise exc.CommandError(_('Attributes must be a list of '
                                 'PATH=VALUE not "%s"') % string)
    try:
        value = json.loads(value)
    except ValueError:
        pass

    return (key, value)


def args_array_to_patch(attributes):
    patch = []
    for attr in attributes:
        path, value = split_and_deserialize(attr)
        patch.append({path: value})
    return patch


def format_args(args, parse_comma=True):
    '''Reformat a list of key-value arguments into a dict.

    Convert arguments into format expected by the API.
    '''
    if not args:
        return {}

    if parse_comma:
        # expect multiple invocations of --label (or other arguments) but fall
        # back to either , or ; delimited if only one --label is specified
        if len(args) == 1:
            args = args[0].replace(';', ',').split(',')

    fmt_args = {}
    for arg in args:
        try:
            (k, v) = arg.split(('='), 1)
        except ValueError:
            raise exc.CommandError(_('arguments must be a list of KEY=VALUE '
                                     'not %s') % arg)
        if k not in fmt_args:
            fmt_args[k] = v
        else:
            if not isinstance(fmt_args[k], list):
                fmt_args[k] = [fmt_args[k]]
            fmt_args[k].append(v)

    return fmt_args


def print_list_field(field):
    return lambda obj: ', '.join(getattr(obj, field))


def remove_null_parms(**kwargs):
    new = {}
    for (key, value) in kwargs.items():
        if value is not None:
            new[key] = value
    return new


def list_hosts(hosts):
    columns = ('id', 'hostname', 'type', 'status')
    utils.print_list(hosts, columns,
                     {'versions': print_list_field('versions')},
                     sortby_index=None)


def list_models(models):
    columns = ('uuid', 'name', 'type', 'status', 'state', 'deployed_url',
               'deployed_on')
    utils.print_list(models, columns,
                     {'versions': print_list_field('versions')},
                     sortby_index=None)

def normalise_file_path_to_url(path):
    if parse.urlparse(path).scheme:
        return path
    path = os.path.abspath(path)
    return parse.urljoin('file:', request.pathname2url(path))


def base_url_for_url(url):
    parsed = parse.urlparse(url)
    parsed_dir = os.path.dirname(parsed.path)
    return parse.urljoin(url, parsed_dir)


def encode_file_data(data):
    if six.PY3 and isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('utf-8')


def decode_file_data(data):
    # Py3 raises binascii.Error instead of TypeError as in Py27
    try:
        return base64.b64decode(data)
    except (TypeError, binascii.Error):
        raise exc.CommandError(_('Invalid Base 64 file data.'))
