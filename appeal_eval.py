#!/usr/bin/env python3
"""
Criterion 4 (the appeal path), plus the part of criterion 5 that
scenarios.py can't express (bodies that aren't JSON objects).

    python app.py                               # in one terminal
    python appeal_eval.py --label before        # in another

Per trial:
  - submits 5 texts, appeals each content_id, and checks that the appeal
    returned under_review, that an appeal entry landed in the log after the
    original decision, and that the original decision is unchanged;
  - appeals 1 made-up content_id and checks for a 404;
  - sends 3 non-object / unparseable bodies to /submit and checks for 400s,
    then checks /ping still answers.

Three trials by default. Writes results/appeal_run_<stamp>_<label>.md.
"""

import argparse
import datetime as dt
import json

import requests

import config

URL = f"http://{config.HOST}:{config.PORT}"

TEXTS = [
    "I wrote this paragraph myself for a class discussion about remote work and whether it helps or hurts teams.",
    "Our team meeting moved to Thursday because half the people were out sick on Tuesday, so the demo is pushed too.",
    "The new bus schedule is confusing. The 7:40 used to come every day and now it skips Wednesdays for some reason.",
    "Grandma's recipe calls for way more butter than I expected, but honestly that's probably why it tastes so good.",
    "I finally fixed the bug that was crashing the build. It was a missing null check in the config loader all along.",
]


def log_entries(cid):
    entries = requests.get(f"{URL}/log", timeout=10).json()["entries"]
    return [e for e in entries if e.get("content_id") == cid]


def one_trial(trial):
    results = []
    for i, text in enumerate(TEXTS, 1):
        sub = requests.post(f"{URL}/submit", timeout=90,
                            json={"text": text, "creator_id": f"eval_appeal_{i}"})
        cid = sub.json().get("content_id")
        app = requests.post(f"{URL}/appeal", timeout=30,
                            json={"content_id": cid, "reasoning": f"Trial {trial}: I wrote this myself."})
        body = app.json()
        hist = log_entries(cid)
        decided = [e for e in hist if e.get("status") == "decided"]
        appeals = [e for e in hist if e.get("event") == "appeal"]
        ok = (app.status_code == 200
              and body.get("status") == "under_review"
              and len(decided) == 1
              and len(appeals) >= 1
              and hist.index(appeals[-1]) > hist.index(decided[0]))
        results.append({"check": f"appeal {i}", "content_id": cid,
                        "appeal_status_code": app.status_code,
                        "appeal_response": body,
                        "log_entries_for_id": len(hist),
                        "original_decision_unchanged": len(decided) == 1,
                        "pass": ok})

    bad = requests.post(f"{URL}/appeal", timeout=30,
                        json={"content_id": "does_not_exist_000", "reasoning": "test"})
    results.append({"check": "unknown content_id", "status_code": bad.status_code,
                    "response": bad.json(), "pass": bad.status_code == 404})

    for name, data in [("body is a JSON array", "[1, 2, 3]"),
                       ("body is a JSON string", '"just a string"'),
                       ("body is unparseable", "{not json")]:
        r = requests.post(f"{URL}/submit", data=data, timeout=30,
                          headers={"Content-Type": "application/json"})
        results.append({"check": f"bad body: {name}", "status_code": r.status_code,
                        "response": r.json(), "pass": r.status_code == 400})

    ping = requests.post(f"{URL}/ping", json={"message": "still alive?"}, timeout=10)
    results.append({"check": "/ping after bad input", "status_code": ping.status_code,
                    "pass": ping.status_code == 200})
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--trials", type=int, default=3)
    p.add_argument("--label", default="")
    args = p.parse_args()

    trials = []
    for t in range(1, args.trials + 1):
        res = one_trial(t)
        trials.append(res)
        appeals = sum(r["pass"] for r in res[:5])
        print(f"trial {t}: appeals {appeals}/5 · unknown id 404: {res[5]['pass']} · "
              f"bad bodies 400: {sum(r['pass'] for r in res[6:9])}/3 · ping: {res[9]['pass']}")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeal_run_{stamp}{label}.md"
    lines = [f"# Appeal + bad-body run{f' — {args.label}' if args.label else ''}", "",
             "- Produced by: `appeal_eval.py::one_trial`", ""]
    for t, res in enumerate(trials, 1):
        lines += [f"**Trial {t}**", "", "```json", json.dumps(res, indent=2, ensure_ascii=False), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
