====
Onepercent-A-friend-of-mine
====

Onepercent-A-friend-of-mine is a small app that makes POST requests to the A Friend of Mine APIs when users do a donation on the 1%Club website.

Quick start
-----------

1. Add 'onepercent_afom' to your INSTALLED_APPS settings like this::
    
    INSTALLED_APPS = (
        ...,
        'onepercent_afom',
    )


2. Include the onepercent-afom URLConf in your project urls.py like this::

    url(r'^api/bedankjes/', include('onepercent-afom.urls.api')),

3. This small app does not have any models so no need to syncdb or migrate.

4. Once installed, you can do POST requests to your url to trigger a POST request to the A Friend of Mine APIs
