# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import, print_function

import contextlib

import kazoo.client
import kazoo.exceptions
import kazoo.handlers.threading

from . import log

TIMEOUT = 1

# Helper for testing
client_class = kazoo.client.KazooClient


@contextlib.contextmanager
def client(*args, **kwargs):
    zk = client_class(*args, **kwargs)
    try:
        zk.start(timeout=TIMEOUT)
    except kazoo.handlers.threading.TimeoutError:
        log.fatal(
            "Could not connect to zookeeper. " +
            "Change your config via `mesos config master`")
    try:
        yield zk
    finally:
        zk.stop()
