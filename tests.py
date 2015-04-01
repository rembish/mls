#!/usr/bin/env python
# coding=utf-8
from locale import LC_ALL, setlocale
from six import u, text_type, PY3
from unittest import TestCase as BaseTestCase, main

from mls import mls


class TestCase(BaseTestCase):
    def setUp(self):
        setlocale(LC_ALL, "en_US.UTF-8")

    def test_translate_to(self):
        s = mls("Hello, world")
        t = s.translate_to("ru", u("Здравствуй, мир"))
        p = t.translate_to("en")
        v = s.translate_to("cs")

        self.assertEqual(s, p)
        self.assertEqual(s, v)

    def test_dict_init(self):
        a = mls({"ru": u("Привет"), "cs": "Ahoj", "en": "Hi"})
        b = a.translate_to("ru_RU")
        c = b.translate_to("cs", "Nazdar")

        self.assertEqual(repr(a), "en'Hi'")
        self.assertEqual(repr(b), "ru'\u041f\u0440\u0438\u0432\u0435\u0442'" if PY3 else "ru'\\xd0\\x9f\\xd1\\x80\\xd0\\xb8\\xd0\\xb2\\xd0\\xb5\\xd1\\x82'")
        self.assertEqual(repr(c), "cs'Nazdar'")

    def test_empty(self):
        x = mls()

        self.assertEqual(str(x), u(""))
        self.assertEqual(x.language, "en")

    def test_lshift(self):
        x = mls()
        x <<= "Hello"

        self.assertEqual(str(x), u("Hello"))
        self.assertTrue("ll" in x)

    def test_rshift(self):
        p = mls("Hello, world")
        t = p.translate_to("ru", u("Здравствуй, мир"))
        y = t >> "ru"

        self.assertEqual(text_type(y), u("Здравствуй, мир"))

        z = mls(y)

        self.assertEqual(text_type(z), text_type(y))
        self.assertEqual(z.language, "ru")
        self.assertEqual(z >> "en", "Hello, world")

    def test_from_mls(self):
        p = mls("Hello, world")
        t = p.translate_to("ru", u("Здравствуй, мир"))

        w = mls(t, language="en")
        self.assertEqual(w, "Hello, world")


if __name__ == "__main__":
    main()
