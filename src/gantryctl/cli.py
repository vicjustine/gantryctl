"""gantryctl command line interface."""

import argparse
import json
import sys

from . import __version__
from .envelope import FLEET, check_lift


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gantryctl")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="check one planned lift")
    c.add_argument("--gantry", required=True, choices=sorted(FLEET))
    c.add_argument("--outreach", required=True, type=float)
    c.add_argument("--load", required=True, type=float)

    sub.add_parser("fleet", help="list the gantry fleet")

    args = p.parse_args(argv)

    if args.cmd == "fleet":
        rows = [
            {
                "name": g.name,
                "max_swl_t": g.max_swl_t,
                "max_outreach_m": g.max_outreach_m,
            }
            for g in FLEET.values()
        ]
        print(json.dumps(rows, indent=2))
        return 0

    try:
        verdict = check_lift(args.gantry, args.outreach, args.load)
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(verdict, indent=2))
    return 0 if verdict["safe"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
