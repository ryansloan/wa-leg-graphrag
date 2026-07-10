"""Thin fetch layer over wa-leg-api: https patch, disk cache, retry, None-vs-[] guards.

The upstream package hardcodes http:// (port 80), which is blocked on some
networks; WSL web services serve the same endpoints over https.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from pathlib import Path

from wa_leg_api import waleg as _waleg

_waleg.WSLSITE = "https://wslwebservices.leg.wa.gov"

from wa_leg_api import legislation, sponsor  # noqa: E402  (import after patch)

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

_RETRIES = 3
_BACKOFF_S = 2.0


def _fetch(cache_key: str, call: Callable[[], dict], root: str) -> list[dict]:
    """Call an endpoint with disk cache + retry. Unwraps the root key; empty results -> []."""
    path = RAW_DIR / f"{cache_key}.json"
    if path.exists():
        return json.loads(path.read_text())
    last_err: Exception | None = None
    for attempt in range(_RETRIES):
        try:
            data = call().get(root) or []
            break
        except Exception as err:  # WaLegApiException or transport error
            last_err = err
            time.sleep(_BACKOFF_S * (attempt + 1))
    else:
        raise RuntimeError(f"fetch failed after {_RETRIES} attempts: {cache_key}") from last_err
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, default=str))  # datetimes -> ISO strings
    return json.loads(path.read_text())


def roster(biennium: str) -> list[dict]:
    """All members who served in the biennium, with party/district/chamber."""
    return _fetch(f"sponsors_{biennium}", lambda: sponsor.get_sponsors(biennium), "array_of_member")


def passed_bill_numbers(biennium: str) -> list[int]:
    """Union of bills that passed the legislature, house, or senate (i.e. had a floor vote that carried)."""
    lists = [
        _fetch(f"passed_legislature_{biennium}",
               lambda: legislation.get_legislation_passed_legislature(biennium), "array_of_legislation_info"),
        _fetch(f"passed_house_{biennium}",
               lambda: legislation.get_legislation_passed_house(biennium), "array_of_legislation_info"),
        _fetch(f"passed_senate_{biennium}",
               lambda: legislation.get_legislation_passed_senate(biennium), "array_of_legislation_info"),
    ]
    return sorted({rec["bill_number"] for lst in lists for rec in lst})


def bill_versions(biennium: str, bill_number: int) -> list[dict]:
    """Detailed records, one per version (HB/SHB/ESHB...)."""
    return _fetch(f"legislation_{biennium}_{bill_number}",
                  lambda: legislation.get_legislation(biennium, bill_number), "array_of_legislation")


def bill_sponsors(biennium: str, bill_id: str) -> list[dict]:
    """Sponsors for a bill; bill_id is the base form like 'HB 1110'."""
    key = f"sponsors_{biennium}_{bill_id.replace(' ', '_')}"
    return _fetch(key, lambda: legislation.get_sponsors(biennium, bill_id), "array_of_sponsor")


def roll_calls(biennium: str, bill_number: int) -> list[dict]:
    """All recorded roll calls for a bill (per motion)."""
    return _fetch(f"rollcalls_{biennium}_{bill_number}",
                  lambda: legislation.get_roll_calls(biennium, bill_number), "array_of_roll_call")
