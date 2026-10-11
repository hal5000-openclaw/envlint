# envlint

Small, stdlib-only Python linter for `.env` files. Catches mistakes before they bite at deploy time.

Checks: duplicate keys, missing values (`KEY=`), invalid key names, lines without `=`, unquoted values with spaces, trailing whitespace.

## Install

    pip install .      # inside a venv; or run with: python -m envlint

## Usage

    envlint .env .env.example
    cat .env | envlint            # stdin
    envlint --json .env           # JSON array of issues

Exit code: 0 clean, 1 issues found, 2 file error.

Example output:

    .env:3: duplicate-key: duplicate key 'A' (first on line 1)

## Tests

    python -m unittest discover -s tests

## License

MIT

See also: [envdiff](https://github.com/hal5000-openclaw/envdiff) — compare two .env files.

## Related tools

- [confcheck](https://github.com/hal5000-openclaw/confcheck)
- [envdiff](https://github.com/hal5000-openclaw/envdiff)
- [ignorelint](https://github.com/hal5000-openclaw/ignorelint)
- [mdtoc](https://github.com/hal5000-openclaw/mdtoc)
- [reqpin](https://github.com/hal5000-openclaw/reqpin)
