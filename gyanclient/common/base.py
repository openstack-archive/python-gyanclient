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

"""
Base utilities to build API operation managers and objects on top of.
"""

import copy

import six.moves.urllib.parse as urlparse

from gyanclient.common.apiclient import base


def getid(obj):
    """Wrapper to get  object's ID.

    Abstracts the common pattern of allowing both an object or an
    object's ID (UUID) as a parameter when dealing with relationships.
    """
    try:
        return obj.id
    except AttributeError:
        return obj


class Manager(object):
    """Provides  CRUD operations with a particular API."""
    resource_class = None

    def __init__(self, api):
        self.api = api

    @property
    def api_version(self):
        return self.api.api_version

    def _create(self, url, body):
        resp, body = self.api.json_request('POST', url, body=body)
        if body:
            return self.resource_class(self, body)

    def _create_and_upload(self, url, data):
        resp, body = self.api.raw_request('POST', url, data=data)
        if body:
            return self.resource_class(self, body)

    def _format_body_data(self, body, response_key):
        if response_key:
            try:
                data = body[response_key]
            except KeyError:
                return []
        else:
            data = body

        if not isinstance(data, list):
            data = [data]

        return data

    def _list_pagination(self, url, response_key=None, obj_class=None,
                         limit=None):
        """Retrieve a list of items.

        The Gyan API is configured to return a maximum number of
        items per request, (FIXME: see Gyan's api.max_limit option). This
        iterates over the 'next' link (pagination) in the responses,
        to get the number of items specified by 'limit'. If 'limit'
        is None this function will continue pagination until there are
        no more values to be returned.

        :param url: a partial URL, e.g. '/nodes'
        :param response_key: the key to be looked up in response
            dictionary, e.g. 'nodes'
        :param obj_class: class for constructing the returned objects.
        :param limit: maximum number of items to return. If None returns
            everything.

        """
        if obj_class is None:
            obj_class = self.resource_class

        if limit is not None:
            limit = int(limit)

        object_list = []
        object_count = 0
        limit_reached = False
        while url:
            resp, body = self.api.json_request('GET', url)
            data = self._format_body_data(body, response_key)
            for obj in data:
                object_list.append(obj_class(self, obj, loaded=True))
                object_count += 1
                if limit and object_count >= limit:
                    # break the for loop
                    limit_reached = True
                    break

            # break the while loop and return
            if limit_reached:
                break

            url = body.get('next')
            if url:
                url_parts = list(urlparse.urlparse(url))
                url_parts[0] = url_parts[1] = ''
                url = urlparse.urlunparse(url_parts)

        return object_list

    def _list(self, url, response_key=None, obj_class=None, body=None,
              qparams=None):
        if qparams:
            url = "%s?%s" % (url, urlparse.urlencode(qparams))

        resp, body = self.api.json_request('GET', url)

        if obj_class is None:
            obj_class = self.resource_class

        data = self._format_body_data(body, response_key)
        return [obj_class(self, res, loaded=True) for res in data if res]

    def _update(self, url, body, method='PATCH', response_key=None):
        resp, body = self.api.json_request(method, url, body=body)
        # PATCH/PUT requests may not return a body
        if body:
            return self.resource_class(self, body)

    def _delete(self, url, qparams=None):
        if qparams:
            url = "%s?%s" % (url, urlparse.urlencode(qparams))
        self.api.raw_request('DELETE', url)

    def _search(self, url, qparams=None, response_key=None, obj_class=None,
                body=None):
        if qparams:
            url = "%s?%s" % (url, urlparse.urlencode(qparams))

        resp, body = self.api.json_request('GET', url, body=body)
        data = self._format_body_data(body, response_key)
        if obj_class is None:
            obj_class = self.resource_class
        return [obj_class(self, res, loaded=True) for res in data if res]


class Resource(base.Resource):
    """Represents a particular instance of an object (tenant, user, etc).

    This is pretty much just a bag for attributes.
    """

    def to_dict(self):
        return copy.deepcopy(self._info)
