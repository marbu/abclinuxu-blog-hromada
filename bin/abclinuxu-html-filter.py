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
    "a": {"href": None}, # spec. case: None means that href can have any value
    "pre": {"class": ["kod"]},
    }


def abclinuxu_filter_attributes(el):
    """
    Dropping html attributes or filtering values of html attributes.
    """
    if el.tag not in ALLOWED_ATTRIBUTES:
        msg = "dropping all attributes of tag {}: {}"
        print(msg.format(el.tag, el.attrib), file=sys.stderr)
        for attr in el.attrib:
            del el.attrib[attr]
    else:
        for attr in el.attrib:
            if attr not in ALLOWED_ATTRIBUTES[el.tag]:
                msg = "dropping attribute {} of tag {}"
                print(msg.format(attr, el.tag), file=sys.stderr)
                del el.attrib[attr]
            else:
                # filtering of value of html attribute
                if ALLOWED_ATTRIBUTES[el.tag][attr] is not None:
                    actual_attrib = el.attrib[attr].split(" ")
                    filtered_attrib = []
                    for aa in actual_attrib:
                        if aa in ALLOWED_ATTRIBUTES[el.tag][attr]:
                            filtered_attrib.append(aa)
                    if len(filtered_attrib) > 0:
                        msg = "filtering value {} of attribute {} of tag {}"
                        print(
                            msg.format(actual_attrib, attr, el.tag),
                            file=sys.stderr)
                        el.attrib[attr] = " ".join(filtered_attrib)
                    else:
                        msg = "dropping attribute {} of tag {}"
                        print(msg.format(attr, el.tag), file=sys.stderr)
                        del el.attrib[attr]


def abclinuxu_filter(tree):
    """
    Drop all html tags or attributes which abclinuxu.cz doesn't allow in html
    code of blogs.
    """
    for el in tree.iter():
        if type(el.tag) is not str:
            # this preserves all comments
            continue
        if el.tag not in ALLOWED_TAGS:
            msg = "dropping tag {}: {}".format(el.tag, el.text)
            print(msg, file=sys.stderr)
            el.drop_tag()
        elif el.tag == "a" and "href" not in el.attrib:
            print("dropping tag a without href", file=sys.stderr)
            el.drop_tag()
        elif len(el.attrib) > 0:
            abclinuxu_filter_attributes(el)


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
