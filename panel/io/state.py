"""
Various utilities for recording and embedding state in a rendered app.
"""
from __future__ import absolute_import, division, unicode_literals

import threading

from weakref import WeakSet

import param

from bokeh.document import Document
from bokeh.io import curdoc as _curdoc
from pyviz_comms import CommManager as _CommManager


class _state(param.Parameterized):
    """
    Holds global state associated with running apps, allowing running
    apps to indicate their state to a user.
    """

    cache = param.Dict(default={}, doc="""
       Global location you can use to cache large datasets or expensive computation results
       across multiple client sessions for a given server.""") 

    webdriver = param.Parameter(default=None, doc="""
        Selenium webdriver used to export bokeh models to pngs.""")

    _curdoc = param.ClassSelector(class_=Document, doc="""
        The bokeh Document for which a server event is currently being
        processed.""")

    # Whether to hold comm events
    _hold = False

    # Used to ensure that events are not scheduled from the wrong thread
    _thread_id = None

    _comm_manager = _CommManager

    # An index of all currently active views
    _views = {}

    # For templates to keep reference to their main root
    _fake_roots = []

    # An index of all currently active servers
    _servers = {}

    # Jupyter display handles
    _handles = {}

    # Stores a set of locked Websockets, reset after every change event
    _locks = WeakSet()

    # Endpoints
    _rest_endpoints = {}

    def __repr__(self):
        server_info = []
        for server, panel, docs in self._servers.values():
            server_info.append("{}:{:d} - {!r}".format(
                server.address or "localhost", server.port, panel)
            )
        if not server_info:
            return "state(servers=[])"
        return "state(servers=[\n  {}\n])".format(",\n  ".join(server_info))

    def kill_all_servers(self):
        """Stop all servers and clear them from the current state."""
        for server_id in self._servers:
            try:
                self._servers[server_id][0].stop()
            except AssertionError:  # can't stop a server twice
                pass
        self._servers = {}

    def _unblocked(self, doc):
        thread = threading.current_thread()
        thread_id = thread.ident if thread else None
        return (doc is self.curdoc and self._thread_id == thread_id)

    def _get_callback(self, endpoint):
        _updating = {}
        def link(*events):
            event = events[0]
            obj = event.cls if event.obj is None else event.obj
            parameterizeds = self._rest_endpoints[endpoint][0]
            if obj not in parameterizeds:
                return
            updating = _updating.get(id(obj), [])
            values = {event.name: event.new for event in events
                      if event.name not in updating}
            if not values:
                return
            _updating[id(obj)] = list(values)
            for parameterized in parameterizeds:
                if parameterized in _updating:
                    continue
                try:
                    parameterized.set_param(**values)
                except Exception:
                    raise
                finally:
                    if id(obj) in _updating:
                        not_updated = [p for p in _updating[id(obj)] if p not in values]
                        _updating[id(obj)] = not_updated
        return link

    def publish(self, endpoint, parameterized, parameters=None):
        if parameters is None:
            parameters = list(parameterized.param)
        if endpoint in self._rest_endpoints:
            parameterizeds, old_parameters, cb = self._rest_endpoints[endpoint]
            if set(parameters) != set(old_parameters):
                raise ValueError("Param REST API output parameters must match across sessions.")
            parameterizeds.append(parameterized)
        else:
            cb = self._get_callback(endpoint)
            self._rest_endpoints[endpoint] = ([parameterized], parameters, cb)
        parameterized.param.watch(cb, parameters)

    @property
    def curdoc(self):
        if self._curdoc:
            return self._curdoc
        elif _curdoc().session_context:
            return _curdoc()

    @curdoc.setter
    def curdoc(self, doc):
        self._curdoc = doc

    @property
    def cookies(self):
        return self.curdoc.session_context.request.cookies if self.curdoc else {}

    @property
    def headers(self):
        return self.curdoc.session_context.request.headers if self.curdoc else {}

    @property
    def session_args(self):
        return self.curdoc.session_context.request.arguments if self.curdoc else {}


state = _state()
