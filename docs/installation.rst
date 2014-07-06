.. _installation-chapter:

=====================
Installing django-csp
=====================

First, install django-csp via pip or from source::

    # pip
    $ pip install django-csp

::

    # source
    $ git clone https://github.com/mozilla/django-csp.git
    $ cd django-csp
    $ python setup.py install

Now edit your project's ``settings`` module. If you are not using the
built in report processor, all you need to do is::

    MIDDLEWARE_CLASSES = (
        # ...
        'csp.middleware.CSPMiddleware',
        # ...
    )

You may want to make use of django-csp's support for script nonces. If so,
you'll need to add a template context processor to ensure a CSP nonce is
available when your templates are rendered. You can do this with something
like::

    TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + ("csp.context_processors.csp",)

It's recommended that you use a template tag for script elements rather than
inserting script nonces yourself. the main advantage of doing this is that the
template tags are designed to cause template rendering to fail if the tag
body contains anything other than a text body (unless you mark the tag as
'dangerous', that is). Tags are available for both Django and Jinja
templates. In both cases you can replace::

    <script>
        // your script
    </script>

with::

    {% script %}
        // your script
    {% endscript %}

and django-csp will insert a script element with a nonce attribute set.

If you're using Django templates, ensure the context processors are set
correctly (see above) then include the csp django tag app in your installed
apps::

    INSTALLED_APPS = (
        # ...
        'csp.djangotag',
        # ...
    )

Once that's done, simply do {% load script %} in your django templates.

If you're using Jinja2 templates you must set appropriate Jinja2 extensions
instead (assuming your project is already set up for using Jinja2)::

    JINJA2_EXTENSIONS = (
        # ...
        'csp.jinja2ext.ScriptExtension',
        # ...
    )

That should do it! Go on to `configuring CSP <configuration-chapter>`_.
