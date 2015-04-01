# coding=utf-8
"""
Unicode-like storage for multiple language mutations.
"""
from doctest import testmod
from locale import getlocale, getdefaultlocale, locale_alias
from six import text_type, u, PY2

__all__ = ["mls", "MultiLingualString"]


def _get_system_locale():
    """
    Returns current (or default) system locale.
    """
    return getlocale()[0] or getdefaultlocale()[0]


def _extract_language(locale_string):
    """
    Extracts language from locale string.

    :param locale_string: Something like language_COUNTRY.encoding
    :return: language
    """
    return locale_string.split("_")[0].lower()


def _convert_to_unicode(value):
    """
    Returns provided `value` to unicode or raises ValueError if it can't
    be converted.
    """
    if PY2 and isinstance(value, str):
        value = value.decode("utf-8")
    elif not isinstance(value, text_type):
        raise ValueError(value)

    return text_type(value)


LANGUAGES = sorted(set([
    _extract_language(locale)
    for locale in locale_alias.values()
    if locale != "C"
]))


class MultiLingualString(text_type):
    """
    MultiLingualString (or it's alias `mls`) is a simple unicode-like storage
    for multiple language translation of one string. You can use it as normal
    string, but it can be easily translation to another language (using
    provided translations or using current locale translation if no language
    mutation for requested language provided).

    Usage examples:

        >>> import locale; locale.setlocale(locale.LC_ALL, "en_US.utf-8")
        'en_US.utf-8'
        >>> s = mls("Hello, world!")
        >>> print s
        Hello, world!
        >>> print repr(s)
        en'Hello, world!'
        >>> print s.language
        en
        >>> t = mls(en="Hello, world!", de="Hallo Welt!")
        >>> v = t.translate_to("de")
        >>> print v
        Hallo Welt!
        >>> w = v.translate_to("en", "Hi, world!")
        >>> print w
        Hi, world!

    """
    # pylint: disable=R0904
    def __new__(cls, mapping=None, language=None, **kwargs):
        # pylint: disable=W0212
        if isinstance(mapping, MultiLingualString):
            language = language or mapping.language
            instance = text_type.__new__(cls, text_type(mapping >> language))
            instance._mapping = mapping._mapping
            instance.language = language
            return instance

        language = _extract_language(language or _get_system_locale())
        if language not in LANGUAGES:
            raise ValueError("Unknown language: {}".format(language))

        if mapping is None:
            mapping = u("")
        if not isinstance(mapping, dict):
            mapping = {language: _convert_to_unicode(mapping)}

        mapping.update(kwargs)
        for key in mapping:
            if key not in LANGUAGES:
                raise ValueError("Unknown mutation mapping: {}".format(key))

        value = mapping.get(language, mapping.get(
            _extract_language(_get_system_locale()), u("")))

        instance = text_type.__new__(cls, value)
        instance._mapping = mapping
        instance.language = language

        return instance

    def translate_to(self, language, value=None):
        """
        Create copy of current MultiLingualString, translated to another
        `language` mutation. Example:

            >>> s = mls({"cs": "Ahoj", "en": "Hello"}, language="en")
            >>> t = s.translate_to("cs")
            >>> print t
            Ahoj
            >>> v = s.translate_to("en", "Hi")
            >>> print v
            Hi

        :param language: to translate current `mls`
        :param value: new translation for provided `language`
        :return: `mls` translated to `language`
        """
        mapping = self._mapping.copy()
        if value:
            mapping[_extract_language(language)] = _convert_to_unicode(value)

        return MultiLingualString(mapping, language)

    def __repr__(self):
        return u("%s%s") % (
            self.language,
            super(MultiLingualString, self).__repr__()[PY2:]
        )

    def __ilshift__(self, translation):
        """
        Syntax sugar which replaces current language translation to provided.
        Example:

            >>> s = mls("Hello", language="en")
            >>> s <<= "Hi"
            >>> print s
            Hi

        :param translation: new translation
        :return: copy of `mls` which will rewrite current object
        """
        mapping = self._mapping.copy()
        mapping[self.language] = _convert_to_unicode(translation)
        return MultiLingualString(mapping, self.language)

    def __rshift__(self, language):
        """
        Syntax sugar which returns another `language` mutation for current
        `mls`. Example:

            >>> s = mls(en="Hi", cs="Ahoj", language="en")
            >>> t = s >> "cs"
            >>> print t
            Ahoj

        :param language: request language
        :return: copy of `mls` translated to provided `language`
        """
        return MultiLingualString(self._mapping, language)

# pylint: disable=C0103
mls = MultiLingualString


if __name__ == "__main__":
    testmod()
