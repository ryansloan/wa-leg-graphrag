"""Fetch one biennium from the WA leg APIs and normalize to data/dataset.json.

Substrate-independent: both the HelixDB graph and the flat-vector control are
built from the dataset this produces. Raw API responses are cached under
data/raw/, so re-runs are free.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import waleg

DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "dataset.json"

_FETCH_WORKERS = 4


def _pick_current_version(versions: list[dict]) -> dict:
    """The record for the version currently in play (falls back to the last listed)."""
    active = [v for v in versions if v.get("active")]
    return (active or versions)[-1]


def _fetch_bill(biennium: str, bill_number: int) -> dict | None:
    versions = waleg.bill_versions(biennium, bill_number)
    if not versions:
        return None
    current = _pick_current_version(versions)
    # shortest bill_id among versions is the original form (HB 1110 vs E2SHB 1110; covers SJM, HJR, etc.)
    base_bill_id = min(versions, key=lambda v: len(v["bill_id"]))["bill_id"]
    return {
        "bill_number": bill_number,
        "bill_id": base_bill_id,
        "current_version_id": current["bill_id"],
        "title": current.get("legal_title") or "",
        "digest": current.get("long_description") or "",
        "short_description": current.get("short_description") or "",
        "status": (current.get("current_status") or {}).get("status") or "",
        "sponsors": waleg.bill_sponsors(biennium, base_bill_id),
        "roll_calls": waleg.roll_calls(biennium, bill_number),
    }


def build_dataset(biennium: str) -> dict:
    # A few members serve in both chambers in one biennium (mid-term Senate appointments);
    # the roster lists them twice under the same id, sometimes with blank fields. One
    # person = one member record; VOTED edges carry the roll call's own chamber.
    by_id: dict[int, dict] = {}
    for m in waleg.roster(biennium):
        rec = {
            "member_id": int(m["id"]),
            "name": m["name"] or "",
            "last_name": m["last_name"] or "",
            "chamber": m["agency"],
            "party": m["party"] or "",
            "district": m["district"] or "",
        }
        prev = by_id.get(rec["member_id"])
        if prev is None:
            by_id[rec["member_id"]] = rec
        else:
            chambers = sorted({prev["chamber"], rec["chamber"]})
            merged = rec if rec["name"] else prev
            merged["chamber"] = "/".join(chambers)
            by_id[rec["member_id"]] = merged
    members = sorted(by_id.values(), key=lambda m: m["member_id"])
    known_ids = set(by_id)

    numbers = waleg.passed_bill_numbers(biennium)
    print(f"{biennium}: {len(members)} members, {len(numbers)} bills with floor passage")

    bills, sponsorships, votes = [], [], []
    with ThreadPoolExecutor(max_workers=_FETCH_WORKERS) as pool:
        raw_bills = list(pool.map(lambda n: _fetch_bill(biennium, n), numbers))

    unknown_voters: set[int] = set()
    for raw in filter(None, raw_bills):
        bills.append({k: raw[k] for k in (
            "bill_number", "bill_id", "current_version_id", "title", "digest",
            "short_description", "status")})
        seen_sponsors: set[int] = set()
        for s in raw["sponsors"]:
            member_id = int(s["id"])
            if member_id not in known_ids:
                continue  # e.g. committee-sponsored bills list the committee
            if member_id in seen_sponsors:
                continue  # the API repeats the sponsor list once per bill version
            seen_sponsors.add(member_id)
            sponsorships.append({
                "bill_number": raw["bill_number"],
                "member_id": member_id,
                "role": "primary" if s["type"] == "Primary" else "cosponsor",
                "order": s["order"],
            })
        for rc in raw["roll_calls"]:
            for v in rc["votes"]:
                member_id = int(v["member_id"])
                if member_id not in known_ids:
                    unknown_voters.add(member_id)
                    continue
                votes.append({
                    "bill_number": raw["bill_number"],
                    "member_id": member_id,
                    "vote": v["v_ote"],  # upstream XML tag is literally <VOte>
                    "motion": rc["motion"],
                    "sequence_number": rc["sequence_number"],
                    "vote_date": rc["vote_date"],
                    "chamber": rc["agency"],
                    "version_voted": rc["bill_id"],
                })
    if unknown_voters:
        print(f"warning: {len(unknown_voters)} voter ids not in roster, votes skipped: {sorted(unknown_voters)}")

    return {
        "biennium": biennium,
        "members": members,
        "bills": bills,
        "sponsorships": sponsorships,
        "votes": votes,
    }


def main() -> None:
    dataset = build_dataset("2025-26")
    DATASET_PATH.write_text(json.dumps(dataset, indent=1))
    print(f"wrote {DATASET_PATH}: {len(dataset['bills'])} bills, "
          f"{len(dataset['sponsorships'])} sponsorships, {len(dataset['votes'])} votes")


if __name__ == "__main__":
    main()
