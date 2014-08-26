Zabbix graph proxy
==================

Tiny python zabbix client for proxying graphs from zabbix. Python 3 compatible.

It does not need any third party dependencies. All dependencies are native python libraries

## How to start

```shell
git clone git@github.com:nogizhopaboroda/zabbix_graph_proxy.git && cd zabbix_graph_proxy
```

or

```shell
wget https://raw.githubusercontent.com/nogizhopaboroda/zabbix_graph_proxy/master/zbx_proxy.py
```

then 

```shell
python zbx_proxy.py
```

## How to use

open in your browser http://localhost:8080/%your_zabbix_graph_id%

or

```
curl http://localhost:8080/%your_zabbix_graph_id% > graph.png
```


