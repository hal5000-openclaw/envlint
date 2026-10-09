"""envlint: lint .env files (stdlib only)."""
import argparse
import json
import re
import sys

KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def lint(text, name="<stdin>"):
    issues = []
    seen = {}

    def add(n, code, msg):
        issues.append({"file": name, "line": n, "code": code, "message": msg})

    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip("\r\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line != line.rstrip():
            add(n, "trailing-whitespace", "trailing whitespace")
        body = line.strip()
        if body.startswith("export "):
            body = body[7:].lstrip()
        if "=" not in body:
            add(n, "no-equals", "line has no '='")
            continue
        key, value = body.split("=", 1)
        key = key.strip()
        if not KEY_RE.match(key):
            add(n, "invalid-key", "invalid key name %r" % key)
        if key in seen:
            add(n, "duplicate-key", "duplicate key %r (first on line %d)" % (key, seen[key]))
        else:
            seen[key] = n
        value = value.strip()
        if value == "":
            add(n, "missing-value", "missing value for %r" % key)
        elif value[0] not in "\"'" and " " in value and not re.search(r"\s#", value):
            add(n, "unquoted-space", "unquoted value contains spaces")
        elif value[0] not in "\"'" and " " in value:
            if " " in re.split(r"\s#", value)[0]:
                add(n, "unquoted-space", "unquoted value contains spaces")
    return issues


def main(argv=None):
    p = argparse.ArgumentParser(prog="envlint", description="Lint .env files.")
    p.add_argument("files", nargs="*", help="files to lint (default: stdin, or '-')")
    p.add_argument("--json", action="store_true", help="JSON output")
    a = p.parse_args(argv)
    issues = []
    for f in a.files or ["-"]:
        try:
            if f == "-":
                issues += lint(sys.stdin.read())
            else:
                with open(f, encoding="utf-8") as fh:
                    issues += lint(fh.read(), f)
        except OSError as e:
            print("envlint: %s" % e, file=sys.stderr)
            return 2
    if a.json:
        print(json.dumps(issues, indent=2))
    else:
        for i in issues:
            print("%s:%d: %s: %s" % (i["file"], i["line"], i["code"], i["message"]))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
