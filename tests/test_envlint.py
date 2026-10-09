import io, json, os, sys, tempfile, unittest
from contextlib import redirect_stdout
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from envlint.cli import lint, main


def codes(t):
    return [i["code"] for i in lint(t)]


class T(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(codes("# c\nA=1\nB=\"x y\"\n\n"), [])

    def test_dup(self):
        self.assertEqual(codes("A=1\nA=2"), ["duplicate-key"])

    def test_missing(self):
        self.assertEqual(codes("A="), ["missing-value"])

    def test_invalid_key(self):
        self.assertEqual(codes("1A=x"), ["invalid-key"])

    def test_no_equals(self):
        self.assertEqual(codes("JUNK"), ["no-equals"])

    def test_space(self):
        self.assertEqual(codes("A=x y"), ["unquoted-space"])

    def test_trailing(self):
        self.assertEqual(codes("A=1 "), ["trailing-whitespace"])

    def test_cli(self):
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as f:
            f.write("A=\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--json", f.name])
        os.unlink(f.name)
        self.assertEqual(rc, 1)
        self.assertEqual(json.loads(buf.getvalue())[0]["code"], "missing-value")


if __name__ == "__main__":
    unittest.main()
