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


class Model(base.Resource):
    def __repr__(self):
        return "<Model %s>" % self._info


class ModelManager(base.Manager):
    resource_class = Model

    @staticmethod
    def _path(id=None):

        if id:
            return '/v1/ml_models/%s' % id
        else:
            return '/v1/ml_models'

    def list_models(self, **kwargs):
        """Retrieve a list of Models.

        :returns: A list of models.

        """

        return self._list_pagination(self._path(''),
                                     "ml_models")

    def get(self, id):
        try:
            return self._list(self._path(id))[0]
        except IndexError:
            return None

    def model_create(self, **kwargs):
        new = {}
        new["name"] = kwargs["name"]
        new["type"] = kwargs["type"]
        new["flavor_id"] = kwargs["flavor_id"]
        model = self._create(self._path(), new)
        upload_trained_model = kwargs['trained_model']
        return self._create_and_upload(self._path(model.id)+'/upload_trained_model', upload_trained_model)

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
        return self._action(id, '/deploy', 'GET')

    def undeploy_model(self, id):
        return self._action(id, '/undeploy', 'GET')
