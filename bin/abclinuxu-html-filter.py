#!/usr/bin/env python3
# -*- coding: utf8 -*-


import argparse
import sys

from lxml import html


ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "br",
    "blockquote",
    "cite",
    "code",
    "div",
    "em",
    "i",
    "hr",
    "h1",
    "h2",
    "h3",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "tt",
    "ul",
    "var",
    "table",
    "thead",
    "tbody",
    "th",
    "tr",
    "td",
    ]


ALLOWED_ATTRIBUTES = {
    "a": ["href"],
    "pre": ["class"],
    }


def abclinuxu_filter(tree):
    """
    Drop all html tags or attributes which abclinuxu.cz doesn't allow in html
    code of blogs.
    """
    for el in tree.iter():
        if type(el.tag) is not str:
            # this will skip eg. all comments
            continue
        if el.tag not in ALLOWED_TAGS:
            msg = "dropping tag {}: {}"
            print(msg.format(el.tag, el.text), file=sys.stderr)
            el.drop_tag()
            continue
        if el.tag == "a" and "href" not in el.attrib:
            print("dropping tag a without href", file=sys.stderr)
            el.drop_tag()
            continue
        if len(el.attrib) > 0:
            if el.tag not in ALLOWED_ATTRIBUTES:
                msg = "dropping attributes of tag {}: {}"
                print(msg.format(el.tag, el.attrib), file=sys.stderr)
                for attr in el.attrib:
                    del el.attrib[attr]
            else:
                for attr in el.attrib:
                    if attr not in ALLOWED_ATTRIBUTES[el.tag]:
                        msg = "dropping attribute {} of tag {}"
                        print(msg.format(attr, el.tag), file=sys.stderr)
                        del el.attrib[attr]


def main():
    ap = argparse.ArgumentParser(
        description="Drop html attributes and tags forbidden by abclinuxu.cz")
    ap.add_argument("file", help="input html file to be filtered")
    ap.add_argument(
        "-o",
        dest="output",
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help="output file (if not set, stdout is used)")
    args = ap.parse_args()

    with open(args.file, "r") as fo:
        tree = html.fromstring(fo.read())
        abclinuxu_filter(tree)
        print(html.tostring(tree, encoding='unicode'), file=args.output)


if __name__ == '__main__':
    sys.exit(main())
