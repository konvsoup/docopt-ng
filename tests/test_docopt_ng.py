import pytest
import docopt
from docopt import DocoptExit, DocoptLanguageError, Option, Argument, Command, OptionsShortcut, Required, NotRequired, parse_argv, Tokens
from pytest import raises


def test_docopt_ng_more_magic_spellcheck_and_expansion():
    o = [Option("-h"), Option("-v", "--verbose"), Option(None, "--file", 1)]
    TS = lambda s: Tokens(s, error=DocoptExit)
    assert parse_argv(TS(""), options=o) == []
    assert parse_argv(TS("-h"), options=o) == [Option("-h", None, 0, True)]
    assert parse_argv(TS("-V"), options=o, more_magic=True) == [Option("-v", "--verbose", 0, True)]
    assert parse_argv(TS("-h --File f.txt"), options=o, more_magic=True) == [Option("-h", None, 0, True), Option(None, "--file", 1, "f.txt")]
    assert parse_argv(TS("-h --fiLe f.txt arg"), options=o, more_magic=True) == [
        Option("-h", None, 0, True),
        Option(None, "--file", 1, "f.txt"),
        Argument(None, "arg"),
    ]
    assert parse_argv(TS("-h -f f.txt arg arg2"), options=o, more_magic=True) == [
        Option("-h", None, 0, True),
        Option(None, "--file", 1, "f.txt"),
        Argument(None, "arg"),
        Argument(None, "arg2"),
    ]


def test_docopt_ng_dot_access():
    doc = """Usage: prog [-vqr] [FILE]
              prog INPUT OUTPUT
              prog --help

    Options:
      -v  print status messages
      -q  report only file names
      -r  show all occurrences of the same error
      --help

    """
    arguments = docopt.docopt(doc, "-v file.py")
    assert arguments == {"-v": True, "-q": False, "-r": False, "--help": False, "FILE": "file.py", "INPUT": None, "OUTPUT": None}
    assert arguments.v == True
    assert arguments.FILE == "file.py"
    arguments = None
    arguments = docopt.docopt(doc, "-v file.py")
    assert arguments == {"-v": True, "-q": False, "-r": False, "--help": False, "FILE": "file.py", "INPUT": None, "OUTPUT": None}
    assert arguments.v == True
    assert arguments.FILE == "file.py"
    arguments = None


def test_docopt_ng_negative_float():
    args = docopt.docopt("usage: prog --negative_pi=NEGPI NEGTAU", "--negative_pi -3.14 -6.28")
    assert args == {"--negative_pi": "-3.14", "NEGTAU": "-6.28"}


def test_docopt_ng_doubledash_version():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args = docopt.docopt("usage: prog", version=1, argv="prog --version")
    assert pytest_wrapped_e.type == SystemExit


def test_docopt_ng__doc__if_no_doc_indirection():
    import sys

    __doc__, sys.argv = "usage: prog --long=<a>", [None, "--long="]

    def test_indirect():
        return docopt.docopt()

    assert test_indirect() == {"--long": ""}

    def test_even_more_indirect():
        return test_indirect()

    assert test_even_more_indirect() == {"--long": ""}
