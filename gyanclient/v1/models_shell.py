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


def _show_model(model):
    utils.print_dict(model._info)


@utils.arg('model-id',
           metavar='<model-id>',
           nargs='+',
           help='ID of the model to delete.')
def do_model_delete(cs, args):
    """Delete specified model."""
    opts = {}
    opts['id'] = args.model_id
    opts = gyan_utils.remove_null_parms(**opts)
    try:
        cs.models.delete_model(**opts)
        print("Request to delete model %s has been accepted." %
              args.model_id)
    except Exception as e:
        print("Delete for model %(model)s failed: %(e)s" %
              {'model': args.model_id, 'e': e})


@utils.arg('model-id',
           metavar='<model-id>',
           help='ID or name of the model to show.')
def do_model_show(cs, args):
    """Show details of a models."""
    opts = {}
    opts['model_id'] = args.model_id
    opts = gyan_utils.remove_null_parms(**opts)
    model = cs.models.get(**opts)
    _show_model(model)


@utils.arg('model-id',
           metavar='<model-id>',
           help='ID of the model to be deployed')
def do_undeploy_model(cs, args):
    """Undeploy the model."""
    opts = {}
    opts['model_id'] = args.model_id
    opts = gyan_utils.remove_null_parms(**opts)
    try:
        model = cs.models.undeploy_model(**opts)
        _show_model(model)
    except Exception as e:
        print("Undeployment of the model %(model)s "
              "failed: %(e)s" % {'model': args.model_id, 'e': e})


@utils.arg('model-id',
           metavar='<model-id>',
           help='ID of the model to be deployed')
def do_deploy_model(cs, args):
    """Deploy already created model."""
    opts = {}
    opts['model_id'] = args.model_id
    opts = gyan_utils.remove_null_parms(**opts)
    try:
        model = cs.models.deploy_model(**opts)
        _show_model(model)
    except Exception as e:
        print("Deployment of the model %(model)s "
              "failed: %(e)s" % {'model': args.model_id, 'e': e})


def do_model_list(cs, args):
    """List models"""
    models = cs.models.list_models()
    gyan_utils.list_models(models)


@utils.arg('name',
           metavar='<name>',
           help='ID or name of the model to train')
@utils.arg('--ml-file',
           metavar='<ml_file>',
           help='The ML model file to be trained')
def do_train_model(cs, args):
    """Remove security group for specified model."""
    opts = {}
    opts['name'] = args.name
    opts = gyan_utils.remove_null_parms(**opts)
    try:
        opts['ml_file'] = yaml.load(open(args.ml_file)) 
        models = cs.models.model_train(**opts)
        gyan_utils.list_models(models)
    except Exception as e:
        print("Creation of model %(model)s "
              "failed: %(e)s" % {'model': args.name, 'e': e})
