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


class Node(base.Resource):
    def __repr__(self):
        return "<Node %s>" % self._info


class NodeManager(base.Manager):
    resource_class = Node

    @staticmethod
    def _path(id=None):

        if id:
            return '/v1/ml-nodes/%s' % id
        else:
            return '/v1/ml-nodes'

    def list_nodes(self, **kwargs):
        """Retrieve a list of Nodes.

        :returns: A list of nodes.

        """

        return self._list_pagination(self._path(''),
                                     "nodes")

    def get(self, id):
        try:
            return self._list(self._path(id))[0]
        except IndexError:
            return None