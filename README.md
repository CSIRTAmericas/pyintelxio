INTELX Python Library   
========================

This python library is developed based on the original intelx library, but adding the functionality to use Intelx.io Identity API.

Original source could be find here: *https://github.com/IntelligenceX/SDK/tree/master/Python*

Installation
------------

You need to install this package and de the original package from IntelX.io

```bash
pip install pyintelx
pip install "intelx @ git+https://github.com/IntelligenceX/SDK#subdirectory=Python"
```

Enviromental Variables
------------
You can set up this two variables if you want

```bash
INTELX_KEY= {api_key} # API KEY of your IntelligenceX account
IDENTITY_ENABLED= {anything} # If present identity api search is enabled. Identity service needs the api key set up.
```

Usage as command
================

```bash 

pyintelx -apikey {API_KEY} -search {search_term} -limit 10 

pyintelx -apikey {API_KEY} -search {search_term} -limit 10 --identityenabled

pyintelx -apikey {API_KEY} -search {search_term} -limit 10 --identityenabled --accounts

```

SEARCH EXAMPLES
---------------

* Query for 10 leaks containing pepe@example.com in intelx.io API

```bash
pyintelx -apikey {API_KEY} search -search pepe@example.com -limit 10
```

* Query for 10 leaks of accounts and passwords for domain example.com in identity.intelx.io API

```bash
pyintelx -apikey {API_KEY} -search example.com -limit 10 --identityenabled --accounts
```

* Query for 10 data leaks for domain example.com in identity.intelx.io API

```bash
pyintelx -apikey {API_KEY} -search example.com -limit 10 --identityenabled
```

* Download some leak file identied by SYSTEM_ID from some previous search

```bash
pyintelx -apikey {API_KEY} -download {SYSTEM_ID} -name {FILE_NAME} -bucket {BUCKET_NAME}
```


Usage as library
================

* Print account information

```python
from pyintelx import intelx
API_KEY = "your api key"

intelx_service = intelx(API_KEY)

intelx_service.GET_CAPABILITIES()

```

* Search for using intelx service

```python
from pyintelx import intelx
API_KEY = "your api key"

intelx_service = intelx(API_KEY)
intelx_service.search("example@example.com", maxresults=max_results, datefrom=date_from, dateto=date_to, buckets=[])
```

* Search for using identity Search Data Leaks service

```python
from pyintelx import IdentityService
API_KEY = "your api key"

identity_service = IdentityService(API_KEY)

identity_service.search("example@example.com", maxresults=max_results, datefrom=date_from, dateto=date_to, buckets=[])
```

* Search for using identity export accounts service

```python
from pyintelx import IdentityService
API_KEY = "your api key"

identity_service = IdentityService(API_KEY)

identity_service.export_accounts("example.com", maxresults=max_results, datefrom=date_from, dateto=date_to, buckets=[])
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
