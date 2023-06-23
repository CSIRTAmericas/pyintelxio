PUBLICWWW Python Library   
========================

This python library is developed based on the original intelx library, but adding the functionality to use Intelx.io Identity API.

Original source could be find here: *https://github.com/IntelligenceX/SDK/tree/master/Python*

Installation
------------

```bash
pip3 install pyintelxio
```

Usage as command
================

```bash 

pyintelxio -apikey {API_KEY} -search {search_term} -limit 10 

pyintelxio -apikey {API_KEY} -search {search_term} -limit 10 --identityenabled

```

SEARCH EXAMPLES
---------------

* Query for 10 leaks containing pepe@example.com in intelx.io API

```bash
pyintelxio -apikey {API_KEY} search -search pepe@example.com -limit 10
```

* Query for 10 leaks of accounts and passwords for domain example.com in identity.intelx.io API

```bash
pyintelxio -apikey {API_KEY} -search example.com -limit 10 --identityenabled
```
* Download some leak file identied by SYSTEM_ID from some previous search

```bash
pyintelxio -apikey {API_KEY} -download {SYSTEM_ID} -name {FILE_NAME} -bucket {BUCKET_NAME}
```


Usage as library
================

* Print account information

```python
import pyintelxio
api = 

```

* Search for 

```python
import pyintelxio
```

## Buckets list
- darknet.tor
- darknet.i2p
- documents.public.scihub
- dumpster
- leaks.private.general
- leaks.public.general
- leaks.public.wikileaks
- pastes
- web.public.dePublic
- web.public.kp
- web.public.uaPublic
- whois 
- web.public.com
- web.gov.ru
- dumpster.web.ssn
- dumpster.web.1
- web.public.peer
- leaks.logs
- usenet
- web.public.gov
- web.public.org
- web.public.net
- web.public.info
- web.public.eu
- web.public.cn
- web.public.nord
- web.public.we
- web.public.cee
- web.public.ams
- web.public.af
- web.public.mea
- web.public.oc
- web.public.tech
- web.public.business
- web.public.social
- web.public.misc
- web.public.aq
