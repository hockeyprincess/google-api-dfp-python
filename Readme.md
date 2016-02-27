# Google's DoubleClick for Publishers API Python Client Library #

Google's DoubleClick for Publishers API service lets developers design computer
programs that interact directly with the DFP platform. With these applications,
advertisers and third parties can more efficiently -- and creatively -- manage
their large or complex DFP accounts.

Google's DFP API Python Client Library makes it easy to write
Python clients to programmatically access DFP accounts. One of
the main features of this client library is that it hides the SOAP layer from
end users, which makes it much easier to interact with API. The outgoing and
incoming SOAP messages are monitored and logged on demand. The response headers
like responseTime, requestId, etc. can also be logged on demand. Another nice
feature of this client library is that it handles data types for all API call
parameters. You no longer need to remember that Date.hour is of type int and
Company.id is of type long. Both of these variables can now be sent as simple
strings, when passing them as parameters. In fact, all variables are passed as
either dict, list, or str. The conversion to the right type is handled
internally by the client library.

The client library provides support for ZSI, which is a well known web services
toolkit from `http://pywebsvcs.sourceforge.net/`.

Two modules are supported for parsing SOAP XML messages. By default, the client
library uses the PyXML module in order to parse SOAP XML messages. In addition,
the library also supports ElementTree module, which may be activated simply by
setting the appropriate config value (i.e. config`[`'xml\_parser']). Note that if
you already have an lxml module installed and wish to use ElementTree, you do
not need to install ElementTree. The lxml module is mostly compatible with
ElementTree.

Although there are projects out there that still support PyXML, it is no longer
maintained. The last update for the ElementTree library is dated 2007-09-12.
Out of these three libraries, the lxml is the one that was updated most
recently.

The code examples, located in `examples/`, demonstrate how to use client
library. For additional examples, take a look at the unit tests in `tests/`.

Useful scripts are located in the `scripts/` directory.

The documentation was generated using Epydoc, a nice tool for generating API
documentation for Python modules.

The data files consist of a set of files in CSV format located in
`dfp_api/data/`.

The client library includes a set of unit tests located in `tests/`. All unit
tests are (and should be) executed against the Sandbox environment. Whenever
changes are made to the client library, the appropriate unit test should be
executed to make sure that everything is working as intended and no new bugs
were introduced.


## How do I start? ##

If you haven't yet done so, you'll need to request sandbox access to the API as
directed on this page: `http://code.google.com/apis/dfp/docs/signup.html`. Once
that's taken care of, proceed to the step-by-step guide below. Write some code
and enjoy!


## Step-by-step guide for accessing the sandbox ##

  1. Make sure you have Python v2.4 or above installed. The latest stable version can be fetched from `http://www.python.org/`.
  1. A ZSI web services toolkit from http://pywebsvcs.sourceforge.net/ is required.
  1. Fetch the latest version of the PyXML module from `http://sourceforge.net/projects/pyxml/`. This is required by the client library.
  1. Sign up for a Google Account. In later steps, we'll assume that the new login is joe.shmoe@gmail.com.
  1. Navigate to the directory that contains your downloaded unzipped client library and run the `setup.py` script to install the `dfp_api` module.
> > `$ python setup.py build install`
  1. From the same directory, run the `dfp_api_config.py` script to set authentication headers. More information about the format of each header is at `http://code.google.com/apis/dfp/docs/developers_guide.html#headers`. Example,
```
   Login email: joe.shmoe@gmail.com
   Login password: secret
   Network code [optional]:
   Application name: GoogleTest

   Enable debugging mode [y/n]: n
   Enable SOAP XML logging mode [y/n]: y
   Enable API request logging mode [y/n]: y
```
  1. Read over the documentation in `docs/index.html` to familiarize yourself with the API of the client library.


## How to make a release ##

  1. Create a new directory named `dfpapi_python_lib_v.v.v`, where v.v.v is a version number (i.e. 1.0.0), and copy the new release into it.
  1. Run the unit tests in `tests/` and the demo programs in `examples/` to make sure that no new bugs were introduced. The `tests/all_tests.py` script will run all available unit tests.
  1. Update LIB\_VERSION in `dfp_api/__init__.py`.
  1. Update the `ChangeLog` file with the new changes.
  1. If you are adding/removing support for an API version, update API\_VERSIONS and MIN\_API\_VERSION in `dfp_api/__init__.py`.
    * If you will also be using ZSI toolkit, run the `scripts/gen_wsdl_services.py` script to generate the client interface code.
    * If you are upgrading to a newer version of SOAPpy or ZSI, make sure to update MIN\_SOAPPY\_VERSION in `dfp_api/soappy_toolkit/__init__.py` and/or MIN\_ZSI\_VERSION in `dfp_api/zsi_toolkit/__init__.py`.
    * Delete the old documentation from `docs/`, regenerate new documentation, and modify the footer to remove the timestamp by executing the following commands from the release's home directory:
```
   $ find docs \( -not -name 'docs' -and -not -name 'README' \) | xargs rm
   $ epydoc --name "DFP API Python Client Library" --url "http://code.google.com/p/google-api-dfp-python/" --html dfp_api --exclude=_services -o docs
   $ perl -pi -e 's/Generated by Epydoc (\d+\.\d+\.\d+) .*/Generated by Epydoc $1/' docs/*
```
  1. Delete the user specific data files: `*.pkl` and `logs/*.log`. Delete all instances of `*.pyc` files from the client library.
```
   $ find . \( -name '*.pkl' -or -name '*.log' -or -name '*.pyc' \) | xargs rm
```
  1. Pack the new release into a tarball and then gzip it,
```
   $ tar -cvf dfpapi_python_lib_v.v.v.tar dfpapi_python_lib_v.v.v/
   $ gzip dfpapi_python_lib_v.v.v.tar
```


## Where do I submit bug reports and/or feature requests? ##

Use the issue tracker at http://code.google.com/p/google-api-dfp-python/issues/list.


## External Dependencies ##

  * [Python v2.4+](http://www.python.org/)
  * [PyXML v0.8.3+](http://sourceforge.net/projects/pyxml/) or [ElementTree v1.2.6+](http://effbot.org/zone/element-index.htm) or [lxml v2.2+](http://codespeak.net/lxml/index.html)
  * [ZSI v2.0](http://pywebsvcs.sourceforge.net/)
  * [Epydoc](http://epydoc.sourceforge.net/) (only if you will be generating docs)
  * [Google Account](https://www.google.com/accounts/NewAccount)


Author:

> api.sgrinberg@gmail.com (Stan Grinberg)

Maintainer:
> api.sgrinberg@gmail.com (Stan Grinberg)