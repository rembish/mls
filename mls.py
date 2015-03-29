#!/usr/bin/env python
# coding=utf-8
from locale import getlocale, getdefaultlocale, setlocale, LC_ALL, locale_alias

__all__ = ["mls", "MultiLingualString"]


def _get_system_locale():
    locale = getlocale()[0]
    if not locale:
        locale = getdefaultlocale()[0]
    return locale


def _extract_language(locale):
    return locale.split("_")[0].lower()


def _convert(value):
    if isinstance(value, str):
        value = value.decode("utf-8")
    elif not isinstance(value, unicode):
        raise ValueError(value)

    return unicode(value)


languages = sorted(set([
    _extract_language(locale)
    for locale in locale_alias.values()
    if locale != "C"
]))


class MultiLingualString(unicode):
    def __new__(cls, mapping=None, language=None, **kwargs):
        if isinstance(mapping, MultiLingualString):
            language = language or mapping.language
            instance = unicode.__new__(cls, unicode(mapping >> language))
            instance._mapping = mapping._mapping
            instance.language = language
            return instance

        language = _extract_language(language or _get_system_locale())
        if language not in languages:
            raise ValueError("Unknown language: {}".format(language))

        if mapping is None:
            mapping = u""
        if not isinstance(mapping, dict):
            mapping = {language: _convert(mapping)}

        mapping.update(kwargs)
        for key in kwargs:
            if key not in languages:
                raise ValueError("Unknown mutation mapping: {}".format(key))

        value = mapping.get(language, mapping.get(
            _extract_language(_get_system_locale()), u""))

        instance = unicode.__new__(cls, value)
        instance._mapping = mapping
        instance.language = language

        return instance

    def translate_to(self, language, value=None):
        mapping = self._mapping.copy()
        if value:
            mapping[_extract_language(language)] = _convert(value)

        return MultiLingualString(mapping, language)

    def __repr__(self):
        return "%s%s" % (
            self.language,
            super(MultiLingualString, self).__repr__()[1:]
        )

    def __ilshift__(self, other):
        mapping = self._mapping.copy()
        mapping[self.language] = _convert(other)
        return MultiLingualString(mapping, self.language)

    def __rshift__(self, language):
        return MultiLingualString(self._mapping, language)

mls = MultiLingualString


if __name__ == "__main__":
    setlocale(LC_ALL, "en_US.UTF-8")

    s = mls("Hello, world")
    t = s.translate_to("ru", u"Здравствуй, мир")
    u = t.translate_to("en")
    v = s.translate_to("cs")

    assert s == u
    assert s == v

    a = mls({"ru": u"Привет", "cs": "Ahoj", "en": "Hi"})
    b = a.translate_to("ru_RU")
    c = b.translate_to("cs", "Nazdar")

    assert repr(a) == "en'Hi'"
    assert repr(b) == "ru'\u041f\u0440\u0438\u0432\u0435\u0442'"
    assert repr(c) == "cs'Nazdar'"

    x = mls()

    assert str(x) == u""
    assert x.language == "en"

    x <<= "Hello"

    assert str(x) == u"Hello"
    assert "ll" in x

    y = u >> "ru"

    assert unicode(y) == u"Здравствуй, мир"

    z = mls(y)

    assert unicode(z) == unicode(y)
    assert z.language == "ru"
    assert z >> "en" == "Hello, world"

    w = mls(y, language="en")

    assert w == "Hello, world"
