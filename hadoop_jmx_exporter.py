#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from lib import utils
from lib.utils import get_module_logger
from lib.hdfs_namenode import NameNodeMetricCollector
from lib.hdfs_datanode import DataNodeMetricCollector
from lib.hdfs_journalnode import JournalNodeMetricCollector
from lib.yarn_resourcemanager import ResourceManagerMetricCollector
from lib.yarn_nodemanager import NodeManagerMetricCollector

logger = get_module_logger(__name__)


def register_prometheus(cluster, args):
    if args.nns is not None and len(args.nns) > 0:
        nnc = NameNodeMetricCollector(cluster, args.nns)
        nnc.collect()
        REGISTRY.register(nnc)
        REGISTRY.register(DataNodeMetricCollector(cluster, nnc))
    if args.rms is not None and len(args.rms) > 0:
        rmc = ResourceManagerMetricCollector(cluster, args.rms, args.queue)
        rmc.collect()
        REGISTRY.register(rmc)
        REGISTRY.register(NodeManagerMetricCollector(cluster, rmc))
    if args.jns is not None and len(args.jns) > 0:
        REGISTRY.register(JournalNodeMetricCollector(cluster, args.jns))
def main():
    args = utils.parse_args()
    host = args.host
    port = int(args.port)
    start_http_server(port, host)
    print("Listen at %s:%s" % (host, port))
    print(args)
    register_prometheus(args.cluster, args)
    while True:
        time.sleep(300)


if __name__ == "__main__":
    main()
