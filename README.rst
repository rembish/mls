MultiLingualString for Python (2k and 3k)
=========================================

.. image:: https://travis-ci.org/rembish/mls.svg?branch=master
    :target: https://travis-ci.org/rembish/mls

.. image:: https://coveralls.io/repos/rembish/mls/badge.svg
    :target: https://coveralls.io/r/rembish/mls

.. image:: https://pypip.in/download/mls/badge.svg
    :target: https://pypi.python.org/pypi/mls

This simple module implements simple unicode-like object, which can contain
multiple language mutation of one string. Actually it's subclass of unicode
type (for python 2k) / string type (for py3k) with few helping methods,
that allow you to translate your string to another languages.

Here, I'll show you some usage examples:: python

    from locale import setlocale, LC_ALL
    from mls import mls

    setlocale(LC_ALL, "en_US.UTF-8")  # Our system locale will be US english

    empty = mls()  # same as unicode, but
    print(empty.language)  # with .language attribute containing "en"

    s = mls("Hello, world!")
    t = s.translate_to("ru_RU", u"Здравствуй, мир!")  # generate new ru-mutation
    print(t.language)  # => "ru"
    print(t)  # => "Здравствуй, мир!"

    x = mls("Ahoj", language="cs")  # czech mutation of "Hi"
    x <<= "Nazdar"  # Change translation to another
    print(repr(x))  # => "cs'Nazdar'"

    a = mls({"en": "Bye", "ru": u"Пока", "cs": u"Čau"})
    print(a)  # => "Bye"
    b = a.translate_to("ru")
    print(b)  # => "Пока"
    c = a >> "cs"
    print(c)  # => "Čau"

    v = mls(en="Vodka", pl=u"Wódka", ru=u"Водка")
    print(repr(v >> "pl"))  # => "pl'W\xf3dka'"
    print(repr(v >> "fr"))  # => "fr'Vodka'" (no translation to french)

    # Also you can use any unicode/str methods
    print("world" in s)  # => True
    print(s[:5])  # => "Hello"
