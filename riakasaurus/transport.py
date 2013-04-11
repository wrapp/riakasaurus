from zope.interface import implements, Interface

from twisted.protocols.basic import LineReceiver
LineReceiver.MAX_LENGTH = 1024*1024*64

from twisted.internet import defer, reactor, protocol
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from twisted.python import log
import logging

from distutils.version import StrictVersion

import urllib
import sys
import re, csv
import time
from cStringIO import StringIO

from xml.etree import ElementTree

# MD_ resources
from riakasaurus.metadata import *
from twisted.web.client import Agent


from riakasaurus.riak_index_entry import RiakIndexEntry
from riakasaurus.mapreduce import RiakLink

# protobuf
from riakasaurus.tx_riak_pb import RiakPBCClient
from riakasaurus.riak_kv_pb2 import *
from riakasaurus.riak_pb2 import *

MAX_LINK_HEADER_SIZE = 8192 - 8

LOGLEVEL_DEBUG = 1
LOGLEVEL_TRANSPORT = 2
LOGLEVEL_TRANSPORT_VERBOSE = 4

versions = {
    1: StrictVersion("1.0.0"),
    1.1: StrictVersion("1.1.0"),
    1.2: StrictVersion("1.2.0")
    }


class ITransport(Interface):
    def get_keys(self, bucket):
        """
        list keys for a given bucket
        """

    def put(self, robj, w = None, dw = None, pw = None, return_body = True, if_none_match=False):
        """
        store a riak_object
        """

    def put_new(self, robj, w=None, dw=None, pw=None, return_body=True, if_none_match=False):
        """
        store a riak_object and generate a key for it
        """

    def get(self, robj, r = None, pr = None, vtag = None):
        """
        fetch a key from the server
        """

    def delete(self, robj, rw=None, r = None, w = None, dw = None, pr = None, pw = None):
        """
        delete a key from the bucket
        """

    def server_version(self):
        """
        return cached server version
        """

    def _server_version(self):
        """
        Gets the server version from the server. To be implemented by
        the individual transport class.
        :rtype string
        """
    def get_buckets(self):
        """
        return the existing buckets
        """

    def ping(self):
        """
        Check server is alive
        """

    def set_bucket_props(self, bucket, props):
        """
        Set bucket properties
        """

    def get_bucket_props(self, bucket):
        """
        get bucket properties
        """


class FeatureDetection(object):
    _s_version = None

    def _server_version(self):
        """
        Gets the server version from the server. To be implemented by
        the individual transport class.
        :rtype string
        """
        raise NotImplementedError

    @defer.inlineCallbacks
    def phaseless_mapred(self):
        """
        Whether MapReduce requests can be submitted without phases.
        :rtype bool
        """
        d = yield self.server_version()
        defer.returnValue(d >= versions[1.1])

    @defer.inlineCallbacks
    def pb_indexes(self):
        """
        Whether secondary index queries are supported over Protocol
        Buffers

        :rtype bool
        """
        d = yield self.server_version()
        defer.returnValue(d >= versions[1.2])

    @defer.inlineCallbacks
    def pb_search(self):
        """
        Whether search queries are supported over Protocol Buffers
        :rtype bool
        """
        d = yield self.server_version()
        defer.returnValue(d >= versions[1.2])

    @defer.inlineCallbacks
    def pb_conditionals(self):
        """
        Whether conditional fetch/store semantics are supported over
        Protocol Buffers
        :rtype bool
        """
        d = yield self.server_version()
        defer.returnValue(d >= versions[1])

    @defer.inlineCallbacks
    def quorum_controls(self):
        """
        Whether additional quorums and FSM controls are available,
        e.g. primary quorums, basic_quorum, notfound_ok
        :rtype bool
        """
        d = yield self.server_version()
        defer.returnValue(d >= versions[1])

    @defer.inlineCallbacks
    def tombstone_vclocks(self):
        """
        Whether 'not found' responses might include vclocks
        :rtype bool
        """
        d = yield self.server_version()
        defer.returnValue(d >= versions[1])

    @defer.inlineCallbacks
    def pb_head(self):
        """
        Whether partial-fetches (vclock and metadata only) are
        supported over Protocol Buffers
        :rtype bool
        """
        d = yield self.server_version()
        defer.returnValue(d >= versions[1])

    @defer.inlineCallbacks
    def server_version(self):
        if not self._s_version:
            self._s_version = yield self._server_version()

        defer.returnValue(StrictVersion(self._s_version))

class BodyReceiver(protocol.Protocol):
    """ Simple buffering consumer for body objects """
    def __init__(self, finished):
        self.finished = finished
        self.buffer = StringIO()

    def dataReceived(self, buffer):
        self.buffer.write(buffer)

    def connectionLost(self, reason):
        self.buffer.seek(0)
        self.finished.callback(self.buffer)

class StringProducer(object):
    """
    Body producer for t.w.c.Agent
    """
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

class HTTPTransport(FeatureDetection):

    implements(ITransport)

    """ HTTP Transport for Riak """
    def __init__(self, client, prefix=None):
        if prefix:
            self._prefix = prefix
        else:
            self._prefix = client._prefix
        self.host = client._host
        self.port = client._port
        self.client = client
        self._client_id = None

    def http_response(self, response):
        def haveBody(body):
            headers = {"http_code": response.code}
            for key, val in response.headers.getAllRawHeaders():
                headers[key.lower()] = val[0]

            return headers, body.read()

        if response.length:
            d = defer.Deferred()
            response.deliverBody(BodyReceiver(d))
            return d.addCallback(haveBody)
        else:
            return haveBody(StringIO(""))

    def http_request(self, method, path, headers={}, body=None):
        url = "http://%s:%s%s" % (self.host, self.port, path)

        h = {}
        for k, v in headers.items():
            if not isinstance(v, list):
                h[k.lower()] = [v]
            else:
                h[k.lower()] = v

        if not 'content-type' in h.keys():
            h['content-type'] = ['application/json']

        if body:
            bodyProducer = StringProducer(body)
        else:
            bodyProducer = None

        return Agent(reactor).request(
                method, str(url), Headers(h), bodyProducer
            ).addCallback(self.http_response)

    def build_rest_path(self, bucket=None, key=None, params=None, prefix=None) :
        """
        Given a RiakClient, RiakBucket, Key, LinkSpec, and Params,
        construct and return a URL.
        """
        # Build 'http://hostname:port/prefix/bucket'
        path = ''
        path += '/' + (prefix or self._prefix)

        # Add '.../bucket'
        if bucket is not None:
            path += '/' + urllib.quote_plus(bucket._name)

        # Add '.../key'
        if key is not None:
            path += '/' + urllib.quote_plus(key)

        # Add query parameters.
        if params is not None:
            s = ''
            for key in params.keys():
                if params[key] is not None:
                    if s != '': s += '&'
                    s += urllib.quote_plus(key) + '=' + urllib.quote_plus(str(params[key]))
            path += '?' + s

        # Return.
        return path

    def decodeJson(self, s):
        return self.client.get_decoder('application/json')(s)

    def encodeJson(self, s):
        return self.client.get_encoder('application/json')(s)

    @defer.inlineCallbacks
    def get_keys(self, bucket):
        params = {'props' : 'True', 'keys' : 'true'}
        url = self.build_rest_path(bucket, params=params)


        headers, encoded_props = yield self.http_request('GET', url)

        if headers['http_code'] == 200:
            props = self.decodeJson(encoded_props)
        else:
            raise Exception('Error getting bucket properties.')

        defer.returnValue(props['keys'])

    @defer.inlineCallbacks
    def set_bucket_props(self, bucket, props):
        """
        Set bucket properties
        """
        url = self.build_rest_path(bucket)
        headers = {'Content-Type': 'application/json'}
        content = self.encodeJson({'props': props})

        #Run the request...
        headers, response = yield self.http_request('PUT', url, headers, content)

        # Handle the response...
        if (response is None):
            raise Exception('Error setting bucket properties.')

        # Check the response value...
        status = headers['http_code']

        if (status != 204):
            raise Exception('Error setting bucket properties.')

        defer.returnValue(response)

    def set_client_id(self, client_id):
        self._client_id = client_id

    def get_client_id(self):
        return self._client_id

    @defer.inlineCallbacks
    def ping(self):
        """
        Check server is alive over HTTP
        """
        response = yield self.http_request('GET', '/ping')
        res = (response is not None) and (response[1] == 'OK')
        defer.returnValue(res)

    @defer.inlineCallbacks
    def stats(self):
        """
        Gets performance statistics and server information
        """
        # TODO: use resource detection
        response = yield self.http_request('GET', '/stats', {'Accept':'application/json'})
        if response[0]['http_code'] is 200:
            defer.returnValue(self.decodeJson(response[1]))
        else:
            defer.returnValue(None)

    # FeatureDetection API - private
    @defer.inlineCallbacks
    def _server_version(self):
        stats = yield self.stats()
        if stats is not None:
            defer.returnValue(stats['riak_kv_version'])
        # If stats is disabled, we can't assume the Riak version
        # is >= 1.1. However, we can assume the new URL scheme is
        # at least version 1.0
        elif 'riak_kv_wm_buckets' in (yield self.get_resources()):
            defer.returnValue("1.0.0")
        else:
            defer.returnValue("0.14.0")

    @defer.inlineCallbacks
    def get_resources(self):
        """
        Gets a JSON mapping of server-side resource names to paths
        :rtype dict
        """
        response = yield self.http_request('GET', '/', {'Accept':'application/json'})
        if response[0]['http_code'] is 200:
            defer.returnValue(self.decodeJson(response[1]))
        else:
            defer.returnValue({})

    @defer.inlineCallbacks
    def get(self, robj, r = None, pr = None, vtag = None) :
        """
        Get a bucket/key from the server
        """
        # We could detect quorum_controls here but HTTP ignores
        # unknown flags/params.
        params = {'r' : r, 'pr': pr}
        if vtag is not None:
            params['vtag'] = vtag
        url = self.build_rest_path(robj.get_bucket(), robj.get_key(),
                                   params=params)
        response = yield self.http_request('GET', url)
        defer.returnValue(
            self.parse_body(response, [200, 300, 404])
        )

    @defer.inlineCallbacks
    def head(self, robj, r = None, pr = None, vtag = None) :
        """
        Get metadata for a bucket/key from the server, basically
        the same as get() but retrieves no data
        """
        params = {'r' : r, 'pr': pr}
        if vtag is not None:
            params['vtag'] = vtag
        url = self.build_rest_path(robj.get_bucket(), robj.get_key(),
                                   params=params)

        response = yield self.http_request('HEAD', url)
        defer.returnValue(
            self.parse_body(response, [200, 300, 404])
        )


    def put(self, robj, w = None, dw = None, pw = None, return_body = True, if_none_match=False):
        """
        Serialize put request and deserialize response
        """
        # We could detect quorum_controls here but HTTP ignores
        # unknown flags/params.
        params = {'returnbody' : str(return_body).lower(), 'w' : w, 'dw' : dw, 'pw' : pw }
        url = self.build_rest_path(bucket=robj.get_bucket(), key=robj.get_key(),
                                   params=params)
        headers = self.build_put_headers(robj)

        # TODO: use a more general 'prevent_stale_writes' semantics,
        # which is a superset of the if_none_match semantics.
        if if_none_match:
            headers["If-None-Match"] = "*"
        content = robj.get_encoded_data()
        return self.do_put(url, headers, content, return_body, key=robj.get_key())

    @defer.inlineCallbacks
    def do_put(self, url, headers, content, return_body=False, key=None):
        if key is None:
            response = yield self.http_request('POST', url, headers, content)
        else:
            response = yield self.http_request('PUT', url, headers, content)

        if return_body:
            defer.returnValue(self.parse_body(response, [200, 201, 300]))
        else:
            self.check_http_code(response, [204])
            defer.returnValue(None)

    @defer.inlineCallbacks
    def put_new(self, robj, w=None, dw=None, pw=None, return_body=True, if_none_match=False):
        """Put a new object into the Riak store, returning its (new) key."""
        # We could detect quorum_controls here but HTTP ignores
        # unknown flags/params.
        params = {'returnbody' : str(return_body).lower(), 'w' : w, 'dw' : dw, 'pw' : pw}
        url = self.build_rest_path(bucket=robj.get_bucket(), params=params)
        headers = self.build_put_headers(robj)
        # TODO: use a more general 'prevent_stale_writes' semantics,
        # which is a superset of the if_none_match semantics.
        if if_none_match:
            headers["If-None-Match"] = "*"
        content = robj.get_encoded_data()
        response = yield self.http_request('POST', url, headers, content)
        location = response[0]['location']
        idx = location.rindex('/')
        key = location[idx+1:]
        if return_body:
            vclock, [(metadata, data)] = self.parse_body(response, [201])
            defer.returnValue((key, vclock, metadata))
        else:
            self.check_http_code(response, [201])
            defer.returnValue((key, None, None))

    @defer.inlineCallbacks
    def delete(self, robj, rw=None, r = None, w = None, dw = None, pr = None, pw = None):
        """
        Delete an object.
        """
        # We could detect quorum_controls here but HTTP ignores
        # unknown flags/params.
        params = {'rw' : rw, 'r': r, 'w': w, 'dw': dw, 'pr': pr, 'pw': pw}
        headers = {}
        url = self.build_rest_path(robj.get_bucket(), robj.get_key(),
                                   params=params)
        ts = yield self.tombstone_vclocks()
        if ts and robj.vclock() is not None:
            headers['X-Riak-Vclock'] = robj.vclock()
        response = yield self.http_request('DELETE', url, headers)
        self.check_http_code(response, [204, 404])
        defer.returnValue(self)

    @defer.inlineCallbacks
    def get_buckets(self):
        """
        Fetch a list of all buckets
        """
        params = {'buckets': 'true'}
        url = self.build_rest_path(None, params=params)
        response = yield self.http_request('GET', url)

        headers, encoded_props = response[0:2]
        if headers['http_code'] == 200:
            props = self.decodeJson(encoded_props)
        else:
            raise Exception('Error getting buckets.')

        defer.returnValue(props['buckets'])

    @defer.inlineCallbacks
    def get_bucket_props(self, bucket):
        """
        Get properties for a bucket
        """
        # Run the request...
        params = {'props' : 'True', 'keys' : 'False'}
        url = self.build_rest_path(bucket, params=params)
        response = yield self.http_request('GET', url)

        headers = response[0]
        encoded_props = response[1]
        if headers['http_code'] == 200:
            props = self.decodeJson(encoded_props)
            defer.returnValue(props['props'])
        else:
            raise Exception('Error getting bucket properties.')

    @defer.inlineCallbacks
    def mapred(self, inputs, query, timeout=None):
        """
        Run a MapReduce query.
        """
        plm = yield self.phaseless_mapred()
        if not plm and (query is None or len(query) is 0):
            raise Exception('Phase-less MapReduce is not supported by this Riak node')

        # Construct the job, optionally set the timeout...
        job = {'inputs':inputs, 'query':query}
        if timeout is not None:
            job['timeout'] = timeout

        content = self.encodeJson(job)

        # Do the request...
        url = "/" + self.client._mapred_prefix
        headers = {'Content-Type': 'application/json'}
        response = yield self.http_request('POST', url, headers, content)

        # Make sure the expected status code came back...
        status = response[0]['http_code']
        if status != 200:
            raise Exception('Error running MapReduce operation. Headers: %s Body: %s' %
                            (repr(response[0]),repr(response[1])))

        result = self.decodeJson(response[1])
        defer.returnValue(result)

    @defer.inlineCallbacks
    def get_index(self, bucket, index, startkey, endkey=None):
        """
        Performs a secondary index query.
        """
        # TODO: use resource detection
        segments = ["buckets", bucket, "index", index, str(startkey)]
        if endkey:
            segments.append(str(endkey))
        uri = '/%s' % ('/'.join(segments))
        headers, data = response = yield self.get_request(uri)
        self.check_http_code(response, [200])
        jsonData = self.decodeJson(data)

        defer.returnValue(jsonData[u'keys'][:])

    @defer.inlineCallbacks
    def search(self, index, query, **params):
        """
        Performs a search query.
        """
        if index is None:
            index = 'search'

        options = {'q':query, 'wt':'json'}
        if 'op' in params:
            op = params.pop('op')
            options['q.op'] = op

        options.update(params)
        # TODO: use resource detection
        uri = "/solr/%s/select" % index
        headers, data = response = yield self.get_request(uri, options)
        self.check_http_code(response, [200])
        if 'json' in headers['content-type']:
            results = self.decodeJson(data)
            defer.returnValue(self._normalize_json_search_response(results))
        elif 'xml' in headers['content-type']:
            defer.returnValue(self._normalize_xml_search_response(data))
        else:
            raise ValueError("Could not decode search response")

    def check_http_code(self, response, expected_statuses):
        status = response[0]['http_code']
        if not status in expected_statuses:
            m = 'Expected status ' + str(expected_statuses) + ', received ' + str(status) + ' : ' + response[1]
            raise Exception(m)

    def parse_body(self, response, expected_statuses):
        """
        Given the output of RiakUtils.http_request and a list of
        statuses, populate the object. Only for use by the Riak client
        library.
        @return self
        """
        # If no response given, then return.
        if response is None:
            return self

        # Make sure expected code came back
        self.check_http_code(response, expected_statuses)

        # Update the object...
        headers = response[0]
        data = response[1]
        status = headers['http_code']

        # Check if the server is down(status==0)
        if not status:
            ### we need the host/port that was used.
            m = 'Could not contact Riak Server: http://$HOST:$PORT !'
            raise RiakError(m)

        # If 404(Not Found), then clear the object.
        if status == 404:
            return None

        # If 300(Siblings), then return the list of siblings
        elif status == 300:
            # Parse and get rid of 'Siblings:' string in element 0
            siblings = data.strip().split('\n')
            siblings.pop(0)
            return siblings

        # Parse the headers...
        vclock = None
        metadata = {MD_USERMETA: {}, MD_INDEX: []}
        links = []
        for header, value in headers.iteritems():
            if header == 'content-type':
                metadata[MD_CTYPE] = value
            elif header == 'charset':
                metadata[MD_CHARSET] = value
            elif header == 'content-encoding':
                metadata[MD_ENCODING] = value
            elif header == 'etag':
                metadata[MD_VTAG] = value
            elif header =='link':
                self.parse_links(links, headers['link'])
            elif header == 'last-modified':
                metadata[MD_LASTMOD] = value
            elif header.startswith('x-riak-meta-'):
                metadata[MD_USERMETA][header.replace('x-riak-meta-', '')] = value
            elif header.startswith('x-riak-index-'):
                field = header.replace('x-riak-index-', '')
                reader = csv.reader([value], skipinitialspace=True)
                for line in reader:
                    for token in line:
                        rie = RiakIndexEntry(field, token)
                        metadata[MD_INDEX].append(rie)
            elif header == 'x-riak-vclock':
                vclock = value
            elif header == 'x-riak-deleted':
                metadata[MD_DELETED] = True
        if links:
            metadata[MD_LINKS] = links

        return vclock, [(metadata, data)]

    def to_link_header(self, link):
        """
        Convert this RiakLink object to a link header string. Used internally.
        """
        header = ''
        header += '</'
        header += self._prefix + '/'
        header += urllib.quote_plus(link.get_bucket()) + '/'
        header += urllib.quote_plus(link.get_key()) + '>; riaktag="'
        header += urllib.quote_plus(link.get_tag()) + '"'
        return header

    def parse_links(self, links, linkHeaders):
        """
        Private.
        @return self
        """
        for linkHeader in linkHeaders.strip().split(','):
            linkHeader = linkHeader.strip()
            matches = re.match("</([^/]+)/([^/]+)/([^/]+)>; ?riaktag=\"([^\']+)\"", linkHeader) or \
                re.match("</(buckets)/([^/]+)/keys/([^/]+)>; ?riaktag=\"([^\']+)\"", linkHeader)
            if matches is not None:
                link = RiakLink(urllib.unquote_plus(matches.group(2)),
                                urllib.unquote_plus(matches.group(3)),
                                urllib.unquote_plus(matches.group(4)))
                links.append(link)
        return self

    def add_links_for_riak_object(self, robject, headers):
        links = robject.get_links()
        if links:
            current_header = ''
            for link in links:
                header = self.to_link_header(link)
                if len(current_header + header) > MAX_LINK_HEADER_SIZE:
                    current_header = ''

                if current_header != '': header = ', ' + header
                current_header += header

            headers['Link'] = current_header

        return headers

    def get_request(self, uri=None, params=None):
        url = self.build_rest_path(bucket=None, params=params, prefix=uri)

        return self.http_request('GET', url)

    def store_file(self, key, content_type="application/octet-stream", content=None):
        url = self.build_rest_path(prefix='luwak', key=key)
        headers = {'Content-Type' : content_type,
                   'X-Riak-ClientId' : self._client_id}

        return self.do_put(url, headers, content, key=key)

    @defer.inlineCallbacks
    def get_file(self, key):
        url = self.build_rest_path(prefix='luwak', key=key)
        response = yield self.http_request('GET', url)
        result = self.parse_body(response, [200, 300, 404])
        if result is not None:
            (vclock, data) = result
            (headers, body) = data.pop()
            defer.returnValue(body)

    @defer.inlineCallbacks
    def delete_file(self, key):
        url = self.build_rest_path(prefix='luwak', key=key)
        response = yield self.http_request('DELETE', url)
        self.parse_body(response, [204, 404])

    def post_request(self, uri=None, body=None, params=None, content_type="application/json"):
        uri = self.build_rest_path(prefix=uri, params=params)
        return self.http_request('POST', uri, {'Content-Type': content_type}, body)

    # Utility functions used by Riak library.

    def build_rest_path(self, bucket=None, key=None, params=None, prefix=None) :
        """
        Given a RiakClient, RiakBucket, Key, LinkSpec, and Params,
        construct and return a URL.
        """
        # Build 'http://hostname:port/prefix/bucket'
        path = ''
        path += '/' + (prefix or self._prefix)

        # Add '.../bucket'
        if bucket is not None:
            path += '/' + urllib.quote_plus(bucket._name)

        # Add '.../key'
        if key is not None:
            path += '/' + urllib.quote_plus(key)

        # Add query parameters.
        if params is not None:
            s = ''
            for key in params.keys():
                if params[key] is not None:
                    if s != '': s += '&'
                    s += urllib.quote_plus(key) + '=' + urllib.quote_plus(str(params[key]))
            path += '?' + s

        # Return.
        return path

    def build_put_headers(self, robj):
        """Build the headers for a POST/PUT request."""

        # Construct the headers...
        headers = {'Accept' : 'text/plain, */*; q=0.5',
                   'Content-Type' : robj.get_content_type(),
                   'X-Riak-ClientId' : self._client_id}

        # Add the vclock if it exists...
        if robj.vclock() is not None:
            headers['X-Riak-Vclock'] = robj.vclock()

        # Create the header from metadata
        links = self.add_links_for_riak_object(robj, headers)

        for key, value in robj.get_usermeta().iteritems():
            headers['X-Riak-Meta-%s' % key] = value

        for rie in robj.get_indexes():
            key = 'X-Riak-Index-%s' % rie.get_field()
            if key in headers:
                headers[key] += ", " + rie.get_value()
            else:
                headers[key] = rie.get_value()

        return headers

    def _normalize_json_search_response(self, json):
        """
        Normalizes a JSON search response so that PB and HTTP have the
        same return value
        """
        result = {}
        if u'response' in json:
            result['num_found'] = json[u'response'][u'numFound']
            result['max_score'] = float(json[u'response'][u'maxScore'])
            docs = []
            for doc in json[u'response'][u'docs']:
                resdoc = {u'id': doc[u'id']}
                if u'fields' in doc:
                    for k, v in doc[u'fields'].iteritems():
                        resdoc[k] = v
                docs.append(resdoc)
            result['docs'] = docs
        return result

    def _normalize_xml_search_response(self, xml):
        """
        Normalizes an XML search response so that PB and HTTP have the
        same return value
        """
        target = XMLSearchResult()
        parser = ElementTree.XMLParser(target = target)
        parser.feed(xml)
        return parser.close()

    @classmethod
    def build_headers(cls, headers):
        return ['%s: %s' % (header, value) for header, value in headers.iteritems()]

    @classmethod
    def parse_http_headers(cls, headers) :
        """
        Parse an HTTP Header string into an asssociative array of
        response headers.
        """
        retVal = {}
        fields = headers.split("\n")
        for field in fields:
            matches = re.match("([^:]+):(.+)", field)
            if matches is None: continue
            key = matches.group(1).lower()
            value = matches.group(2).strip()
            if key in retVal.keys():
                if  isinstance(retVal[key], list):
                    retVal[key].append(value)
                else:
                    retVal[key] = [retVal[key]].append(value)
            else:
                retVal[key] = value
        return retVal

class XMLSearchResult(object):
    # Match tags that are document fields
    fieldtags = ['str', 'int', 'date']

    def __init__(self):
        # Results
        self.num_found = 0
        self.max_score = 0.0
        self.docs = []

        # Parser state
        self.currdoc = None
        self.currfield = None
        self.currvalue = None

    def start(self, tag, attrib):
        if tag == 'result':
            self.num_found = int(attrib['numFound'])
            self.max_score = float(attrib['maxScore'])
        elif tag == 'doc':
            self.currdoc = {}
        elif tag in self.fieldtags and self.currdoc is not None:
            self.currfield = attrib['name']

    def end(self, tag):
        if tag == 'doc' and self.currdoc is not None:
            self.docs.append(self.currdoc)
            self.currdoc = None
        elif tag in self.fieldtags and self.currdoc is not None:
            if tag == 'int':
                self.currvalue = int(self.currvalue)
            self.currdoc[self.currfield] = self.currvalue
            self.currfield = None
            self.currvalue = None

    def data(self, data):
        if self.currfield:
            # riak_solr_output adds NL + 6 spaces
            data = data.rstrip()
            if self.currvalue:
                self.currvalue += data
            else:
                self.currvalue = data

    def close(self):
        return {'num_found':self.num_found,
                'max_score':self.max_score,
                'docs': self.docs }

class StatefulTransport(object):

    def __init__(self,transport):
        self.__transport = transport
        self.__state = 'idle'
        self.__created = time.time()
        self.__used = time.time()

    def __repr__(self):
        return '<StatefulTransport idle=%.2fs state=\'%s\' transport=%s>' % (time.time() - self.__used, self.__state, self.__transport)

    def isActive(self):
        return self.__state == 'active'

    def setActive(self):
        self.__state = 'active'
        self.__used = time.time()

    def isIdle(self):
        return self.__state == 'idle'

    def setIdle(self):
        self.__state = 'idle'
        self.__used = time.time()

    def getTransport(self):
        return self.__transport

    def age(self):
        return time.time() - self.__used


class PBCTransport(FeatureDetection):
    """ Protocoll buffer transport for Riak """

    implements(ITransport)

    debug = 0
    logToLevel = logging.INFO
    MAX_TRANSPORTS = 50
    MAX_IDLETIME   = 5*60     # in seconds
    GC_TIME        = 120        # how often (in seconds) the garbage collection should run
    timeout        = None

    def __init__(self, client):
        self._prefix = client._prefix
        self.host = client._host
        self.port = client._port
        self.client = client
        self._client_id = None
        self._transports = []    # list of transports, empty on start
        self._gc = reactor.callLater(self.GC_TIME, self._garbageCollect)

    def setTimeout(self,t):
        self.timeout = t

    @defer.inlineCallbacks
    def _getFreeTransport(self):
        foundOne = False
        for stp in self._transports:
            if stp.isIdle():
                stp.setActive()
                foundOne = True
                if self.debug & LOGLEVEL_TRANSPORT_VERBOSE:
                    log.msg("[%s] aquired idle transport[%d]: %s" % (self.__class__.__name__, len(self._transports),stp), logLevel = self.logToLevel)
                defer.returnValue(stp)
        if not foundOne:
            if len(self._transports) > self.MAX_TRANSPORTS:
                raise Exception("to many transports, aborting")

            # nothin free, create a new protocol instance, append
            # it to self._transports and return it
            transport = yield RiakPBCClient().connect(self.host, self.port)
            if self.timeout:
                transport.setTimeout(self.timeout)
            stp = StatefulTransport(transport)
            idx = len(self._transports)
            self._transports.append(stp)
            stp.setActive()
            if self.debug & LOGLEVEL_TRANSPORT:
                log.msg("[%s] allocate new transport[%d]: %s" % (self.__class__.__name__, len(self._transports),stp), logLevel = self.logToLevel)
            defer.returnValue(stp)

    @defer.inlineCallbacks
    def _garbageCollect(self):
        self._gc = reactor.callLater(self.GC_TIME, self._garbageCollect)
        for idx, stp in enumerate(self._transports):
            if (stp.isIdle() and stp.age() > self.MAX_IDLETIME):
                yield stp.getTransport().quit()
                if self.debug & LOGLEVEL_TRANSPORT:
                    log.msg("[%s] expire idle transport[%d] %s" % (self.__class__.__name__, idx,stp), logLevel = self.logToLevel)
                    log.msg("[%s] %s" % (self.__class__.__name__, self._transports), logLevel = self.logToLevel)
                self._transports.remove(stp)
            elif self.timeout and stp.isActive() and stp.age() > self.timeout:
                yield stp.getTransport().quit()
                if self.debug & LOGLEVEL_TRANSPORT:
                    log.msg("[%s] expire timeouted transport[%d] %s" % (self.__class__.__name__, idx,stp), logLevel = self.logToLevel)
                    log.msg("[%s] %s" % (self.__class__.__name__, self._transports), logLevel = self.logToLevel)
                self._transports.remove(stp)


    @defer.inlineCallbacks
    def quit(self):
        self._gc.cancel()      # cancel the garbage collector

        for stp in self._transports:
            if self.debug & LOGLEVEL_DEBUG:
                log.msg("[%s] transport[%d].quit() %s" % (self.__class__.__name__, len(self._transports),stp), logLevel = self.logToLevel)
            yield stp.getTransport().quit()

    def __del__(self):
        """on shutdown, close all transports"""
        self.quit()

    def put(self, robj, w = None, dw = None, pw = None, return_body = True, if_none_match=False):
        ret = self.__put(robj, w, dw, pw, return_body = return_body, if_none_match = if_none_match)
        if return_body:
            return ret
        else:
            return None

    def put_new(self, robj, w=None, dw=None, pw=None, return_body=True, if_none_match=False):
        ret = self.__put(robj, w, dw, pw, return_body = return_body, if_none_match = if_none_match)
        if return_body:
            return ret
        else:
            return (ret[0],None,None)


    @defer.inlineCallbacks
    def __put(self, robj, w = None, dw = None, pw = None, return_body=True, if_none_match=False):
        # std kwargs
        kwargs = {'w'             : w,
                  'dw'            : dw,
                  'pw'            : pw,
                  'return_body'   : return_body,
                  'if_none_match' : if_none_match
                  }
        # vclock
        vclock = robj.vclock() or None

        payload = {
            'value' : robj.get_encoded_data(),
            'content_type' : robj.get_content_type(),
            }

        # links
        links = robj.get_links()
        if links:
            payload['links'] = []
            for l in links:
                payload['links'].append((l.get_bucket(), l.get_key(), l.get_tag()))

        # usermeta
        if robj.get_usermeta():
            payload['usermeta'] = []
            for key, value in robj.get_usermeta().iteritems():
                payload['usermeta'].append((key, value))

        # indexes
        if robj.get_indexes():
            payload['indexes'] = []
            for index in robj.get_indexes():
                payload['indexes'].append((index.get_field(), index.get_value()))


        # aquire transport, fire, release
        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.put(robj.get_bucket().get_name(),
                                  robj.get_key(),
                                  payload,
                                  vclock,
                                  **kwargs
                                  )
        stp.setIdle()
        defer.returnValue(self.parseRpbGetResp(ret))


    @defer.inlineCallbacks
    def get(self, robj, r = None, pr = None, vtag = None):

        # ***FIXME*** whats vtag for? ignored for now

        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.get(robj.get_bucket().get_name(),
                                  robj.get_key(),
                                  r = r,
                                  pr = pr)

        stp.setIdle()
        defer.returnValue(self.parseRpbGetResp(ret))

    @defer.inlineCallbacks
    def head(self, robj, r = None, pr = None, vtag = None):
        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.get(robj.get_bucket().get_name(),
                                  robj.get_key(),
                                  r = r,
                                  pr = pr,
                                  head = True)

        stp.setIdle()
        defer.returnValue(self.parseRpbGetResp(ret))


    @defer.inlineCallbacks
    def delete(self, robj, rw=None, r = None, w = None, dw = None, pr = None, pw = None):
        """
        Delete an object.
        """
        # We could detect quorum_controls here but HTTP ignores
        # unknown flags/params.
        kwargs = {'rw' : rw, 'r': r, 'w': w, 'dw': dw, 'pr': pr, 'pw': pw}
        headers = {}

        ts = yield self.tombstone_vclocks()
        if ts and robj.vclock() is not None:
            kwargs['vclock'] = robj.vclock()

        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.delete(robj.get_bucket().get_name(),
                                     robj.get_key(),
                                     **kwargs
                                     )

        stp.setIdle()
        defer.returnValue(ret)


    @defer.inlineCallbacks
    def get_buckets(self):
        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.getBuckets()
        stp.setIdle()
        defer.returnValue([x for x in ret.buckets])


    @defer.inlineCallbacks
    def server_version(self):
        if not self._s_version:
            self._s_version = yield self._server_version()

        defer.returnValue(StrictVersion(self._s_version))

    @defer.inlineCallbacks
    def _server_version(self):
        stp = yield self._getFreeTransport()
        transport = stp.getTransport()

        stats = yield transport.getServerInfo()
        stp.setIdle()


        if stats is not None:
            if self.debug % LOGLEVEL_DEBUG:
                log.msg("[%s] fetched server version: %s" % (
                    self.__class__.__name__, stats.server_version
                ), logLevel = self.logToLevel)
            defer.returnValue(stats.server_version)
        else:
            defer.returnValue("0.14.0")

    @defer.inlineCallbacks
    def ping(self):
        """
        Check server is alive
        """
        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.ping()
        stp.setIdle()
        defer.returnValue(ret == True)


    @defer.inlineCallbacks
    def set_bucket_props(self, bucket, props):
        """
        Set bucket properties
        """
        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.setBucketProperties(bucket.get_name(), **props)
        stp.setIdle()
        defer.returnValue(ret == True)


    @defer.inlineCallbacks
    def get_bucket_props(self, bucket):
        """
        get bucket properties
        """
        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.getBucketProperties(bucket.get_name())
        stp.setIdle()
        defer.returnValue({'n_val'      : ret.props.n_val,
                           'allow_mult' : ret.props.allow_mult})

    @defer.inlineCallbacks
    def get_keys(self, bucket):
        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.getKeys(bucket.get_name())
        stp.setIdle()
        defer.returnValue(ret)

    def parseRpbGetResp(self,res):
        """
        adaptor for a RpbGetResp message
        message RpbGetResp {
           repeated RpbContent content = 1;
           optional bytes vclock = 2;
           optional bool unchanged = 3;
        }
        """
        if res == True:         # empty response
            return None
        vclock = res.vclock
        resList = []
        for content in res.content: # iterate over RpbContent field
            metadata = {MD_USERMETA: {}, MD_INDEX: []}
            data = content.value
            if content.HasField('content_type'): 
                metadata[MD_CTYPE] = content.content_type

            if content.HasField('charset'): 
                metadata[MD_CHARSET] = content.charset

            if content.HasField('content_encoding'): 
                metadata[MD_ENCODING] = content.content_encoding

            if content.HasField('vtag'): 
                metadata[MD_VTAG] = content.vtag

            if content.HasField('last_mod'): 
                metadata[MD_LASTMOD] = content.last_mod

            if content.HasField('deleted'): 
                metadata[MD_DELETED] = content.deleted

            if len(content.links):
                metadata[MD_LINKS] = []
                for l in content.links:
                    metadata[MD_LINKS].append(RiakLink(l.bucket,l.key,l.tag))

            if len(content.usermeta):
                metadata[MD_USERMETA] = {}
                for md in content.usermeta:
                    metadata[MD_USERMETA][md.key] = md.value

            if len(content.indexes):
                metadata[MD_INDEX] = []
                for ie in content.indexes:
                    metadata[MD_INDEX].append(RiakIndexEntry(ie.key, ie.value))
            resList.append((metadata, data))
        return vclock, resList


    def decodeJson(self, s):
        return self.client.get_decoder('application/json')(s)

    def encodeJson(self, s):
        return self.client.get_encoder('application/json')(s)

    @defer.inlineCallbacks
    def search(self, index, query, **params):
        stp = yield self._getFreeTransport()
        transport = stp.getTransport()
        ret = yield transport.search(index, query, **params)
        stp.setIdle()
        defer.returnValue(ret)


    # def deferred_sleep(self,secs):
    #     """
    #     fake deferred sleep

    #     @param secs: time to sleep
    #     @type secs: float
    #     """
    #     d = defer.Deferred()
    #     reactor.callLater(secs, d.callback, None)
    #     return d
