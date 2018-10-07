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


def _show_node(node):
    utils.print_dict(node._info)


@utils.arg('node-id',
           metavar='<node-id>',
           help='ID or name of the node to show.')
def do_node_show(cs, args):
    """Show details of a Node."""
    opts = {}
    opts['node_id'] = args.node_id
    opts = gyan_utils.remove_null_parms(**opts)
    node = cs.nodes.get(**opts)
    _show_node(node)


def do_node_list(cs, args):
    """List Nodes"""
    nodes = cs.nodes.list_nodes()
    gyan_utils.list_nodes(nodes)
