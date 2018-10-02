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

from six.moves.urllib import parse

from gyanclient import api_versions
from gyanclient.common import base
from gyanclient.common import utils
from gyanclient import exceptions


CREATION_ATTRIBUTES = ['name', 'image', 'command', 'cpu', 'memory',
                       'environment', 'workdir', 'labels', 'image_pull_policy',
                       'restart_policy', 'interactive', 'image_driver',
                       'security_groups', 'hints', 'nets', 'auto_remove',
                       'runtime', 'hostname', 'mounts', 'disk',
                       'availability_zone', 'auto_heal', 'privileged',
                       'exposed_ports', 'healthcheck']


class Model(base.Resource):
    def __repr__(self):
        return "<Model %s>" % self._info


class ModelManager(base.Manager):
    resource_class = Model

    @staticmethod
    def _path(id=None):

        if id:
            return '/v1/ml-models/%s' % id
        else:
            return '/v1/ml-models'

    def list_models(self, **kwargs):
        """Retrieve a list of Models.

        :returns: A list of models.

        """

        return self._list_pagination(self._path(''),
                                     "models")

    def get(self, id):
        try:
            return self._list(self._path(id))[0]
        except IndexError:
            return None

    def model_train(self, **kwargs):
        new = {}
        new['name'] = kwargs["name"]
        new['ml_file'] = kwargs["ml_file"]
        return self._create(self._path(), new)

    def delete_model(self, id):
        return self._delete(self._path(id))

    def _action(self, id, action, method='POST', **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Length', '0')
        resp, body = self.api.json_request(method,
                                           self._path(id) + action,
                                           **kwargs)
        return resp, body

    def deploy_model(self, id):
        return self._action(id, '/deploy')

    def undeploy_model(self, id):
        return self._action(id, '/unstop')

    def rebuild(self, id, **kwargs):
        return self._action(id, '/rebuild',
                            qparams=kwargs)

    def restart(self, id, timeout):
        return self._action(id, '/reboot',
                            qparams={'timeout': timeout})

    def pause(self, id):
        return self._action(id, '/pause')

    def unpause(self, id):
        return self._action(id, '/unpause')

    def logs(self, id, **kwargs):
        if kwargs['stdout'] is False and kwargs['stderr'] is False:
            kwargs['stdout'] = True
            kwargs['stderr'] = True
        return self._action(id, '/logs', method='GET',
                            qparams=kwargs)[1]

    def execute(self, id, **kwargs):
        return self._action(id, '/execute',
                            qparams=kwargs)[1]

    def execute_resize(self, id, exec_id, width, height):
        self._action(id, '/execute_resize',
                     qparams={'exec_id': exec_id, 'w': width, 'h': height})[1]
