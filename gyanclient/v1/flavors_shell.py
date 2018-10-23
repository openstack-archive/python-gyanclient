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


def _show_flavor(flavor):
    utils.print_dict(flavor._info)


@utils.arg('flavor_id',
           metavar='<flavor-id>',
           help='ID of the Flavor to delete.')
def do_flavor_delete(cs, args):
    """Delete specified flavor."""
    try:
        cs.flavors.delete_flavor(args.flavor_id)
        print("Request to delete flavor %s has been accepted." %
              args.flavor_id)
    except Exception as e:
        print("Delete for flavor %(flavor)s failed: %(e)s" %
              {'flavor': args.flavor_id, 'e': e})


@utils.arg('flavor_id',
           metavar='<flavor-id>',
           help='ID or name of the flavor to show.')
def do_flavor_show(cs, args):
    """Show details of a flavors."""
    flavor = cs.flavors.get(args.flavor_id)
    _show_flavor(flavor)


def do_flavor_list(cs, args):
    """List flavors"""
    flavors = cs.flavors.list_flavors()
    gyan_utils.list_flavors(flavors)


@utils.arg('name',
           metavar='<name>',
           help='ID or name of the flavor to train')
@utils.arg('--hints-path',
           metavar='<hints_path>',
           help='Absolute path for trained flavors')
def do_flavor_create(cs, args):
    """Upload and create a trained flavor"""
    opts = {}
    opts['name'] = args.name
    opts['hints_data'] = yaml.load(open(args.hints_path))
    opts = gyan_utils.remove_null_parms(**opts)
    try:
        flavors = cs.flavors.flavor_create(**opts)
        gyan_utils.list_flavors([flavors])
    except Exception as e:
        print("Creation of flavor %(flavor)s "
              "failed: %(e)s" % {'flavor': args.name, 'e': e})
