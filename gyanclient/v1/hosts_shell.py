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

import argparse
from contextlib import closing
import io
import json
import os
import tarfile
import time
import yaml

from gyanclient.common import cliutils as utils
from gyanclient.common import utils as gyan_utils
from gyanclient import exceptions as exc


def _show_host(host):
    utils.print_dict(host._info)


@utils.arg('host-id',
           metavar='<host-id>',
           help='ID or name of the host to show.')
def do_host_show(cs, args):
    """Show details of a Host."""
    opts = {}
    opts['host_id'] = args.host_id
    opts = gyan_utils.remove_null_parms(**opts)
    host = cs.hosts.get(**opts)
    _show_host(host)


def do_host_list(cs, args):
    """List Hosts"""
    hosts = cs.hosts.list_hosts()
    gyan_utils.list_hosts(hosts)
