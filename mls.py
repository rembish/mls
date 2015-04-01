# coding=utf-8
from locale import getlocale, getdefaultlocale, locale_alias
from six import text_type, u, PY2

__all__ = ["mls", "MultiLingualString"]


def _get_system_locale():
    locale = getlocale()[0]
    if not locale:
        locale = getdefaultlocale()[0]
    return locale


def _extract_language(locale):
    return locale.split("_")[0].lower()


def _convert(value):
    if PY2 and isinstance(value, str):
        value = value.decode("utf-8")
    elif not isinstance(value, text_type):
        raise ValueError(value)

    return text_type(value)


languages = sorted(set([
    _extract_language(locale)
    for locale in locale_alias.values()
    if locale != "C"
]))


class MultiLingualString(text_type):
    def __new__(cls, mapping=None, language=None, **kwargs):
        if isinstance(mapping, MultiLingualString):
            language = language or mapping.language
            instance = text_type.__new__(cls, text_type(mapping >> language))
            instance._mapping = mapping._mapping
            instance.language = language
            return instance

        language = _extract_language(language or _get_system_locale())
        if language not in languages:
            raise ValueError("Unknown language: {}".format(language))

        if mapping is None:
            mapping = u("")
        if not isinstance(mapping, dict):
            mapping = {language: _convert(mapping)}

        mapping.update(kwargs)
        for key in kwargs:
            if key not in languages:
                raise ValueError("Unknown mutation mapping: {}".format(key))

        value = mapping.get(language, mapping.get(
            _extract_language(_get_system_locale()), u("")))

        instance = text_type.__new__(cls, value)
        instance._mapping = mapping
        instance.language = language

        return instance

    def translate_to(self, language, value=None):
        mapping = self._mapping.copy()
        if value:
            mapping[_extract_language(language)] = _convert(value)

        return MultiLingualString(mapping, language)

    def __repr__(self):
        return u("%s%s") % (
            self.language,
            super(MultiLingualString, self).__repr__()[PY2:]
        )

    def __ilshift__(self, other):
        mapping = self._mapping.copy()
        mapping[self.language] = _convert(other)
        return MultiLingualString(mapping, self.language)

    def __rshift__(self, language):
        return MultiLingualString(self._mapping, language)

mls = MultiLingualString
