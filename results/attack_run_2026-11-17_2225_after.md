# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-17 22:25
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `9f9291f521c3` | unsure | 0.378 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c268a56f7bd5` | unsure | 0.394 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `a198f23c1d14` | unsure | 0.520 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `e0d1dd82f1a5` | unsure | 0.647 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `ac75b2a8d099` | human | 0.277 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `6b38377d70ab` | unsure | 0.445 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `018fb8583a93` | unsure | 0.360 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `2830449e628c` | unsure | 0.412 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `a73fc4a05058` | unsure | 0.605 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `4cdd2cc166d4` | ai | 0.923 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `fa2f847a497d` | unsure | 0.592 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `f349c8f5ad98` | unsure | 0.740 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `43d0d447c773` | unsure | 0.740 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `bcbe8ca23daf` | unsure | 0.740 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `568d1eb18801` | unsure | 0.740 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `05967509b806` | ai | 0.763 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `5b46ba515711` | unsure | 0.749 |  |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `9cb2f7fdb3e1` | unsure | 0.378 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ce232176698d` | human | 0.184 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `47606bec5cca` | unsure | 0.495 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `43bee487fe3b` | unsure | 0.438 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `7bfd097553ed` | unsure | 0.464 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `60ad1cccf479` | unsure | 0.557 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0927be7e788c` | human | 0.199 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6a77768d30f7` | human | 0.199 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `33880e5ed669` | human | 0.199 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7f80bc58267b` | human | 0.199 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `70bb28bf5dde` | human | 0.199 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `47ac2c1e663e` | human | 0.199 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4985ed370b5d` | human | 0.199 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `85a985779fd7` | human | 0.199 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `129de0b0e52a` | human | 0.199 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9208f747d783` | human | 0.199 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "9f9291f521c3",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3781,
  "model_score": 0.1635,
  "style_score": 0.7,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c268a56f7bd5",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3944,
  "model_score": 0.5943,
  "style_score": 0.0946,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "a198f23c1d14",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.52,
  "model_score": 0.6662,
  "style_score": 0.3006,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "e0d1dd82f1a5",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6468,
  "model_score": 0.6114,
  "style_score": 0.7,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "ac75b2a8d099",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2767,
  "model_score": 0.3212,
  "style_score": 0.21,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "6b38377d70ab",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4445,
  "model_score": 0.5727,
  "style_score": 0.2523,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "018fb8583a93",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.5862,
  "style_score": 0.0167,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "2830449e628c",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4124,
  "model_score": 0.2452,
  "style_score": 0.6631,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "a73fc4a05058",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6046,
  "model_score": 0.7042,
  "style_score": 0.4553,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "4cdd2cc166d4",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9228,
  "model_score": 0.9792,
  "style_score": 0.8381,
  "label": "This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "fa2f847a497d",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5921,
  "model_score": 0.6175,
  "style_score": 0.554,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "f349c8f5ad98",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.74,
  "model_score": 0.7387,
  "style_score": 0.8607,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "43d0d447c773",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.74,
  "model_score": 0.8051,
  "style_score": 0.6732,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "bcbe8ca23daf",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.74,
  "model_score": 0.8329,
  "style_score": 0.6266,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "568d1eb18801",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.74,
  "model_score": 0.8005,
  "style_score": 0.9698,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "05967509b806",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7629,
  "model_score": 0.8814,
  "style_score": 0.5852,
  "label": "This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "5b46ba515711",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.749,
  "model_score": 0.8816,
  "style_score": 0.55,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "9cb2f7fdb3e1",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3775,
  "model_score": 0.4625,
  "style_score": 0.25,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "ce232176698d",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1844,
  "model_score": 0.2044,
  "style_score": 0.1543,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "47606bec5cca",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4947,
  "model_score": 0.5943,
  "style_score": 0.3453,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "43bee487fe3b",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4378,
  "model_score": 0.4998,
  "style_score": 0.3449,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "7bfd097553ed",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4644,
  "model_score": 0.6401,
  "style_score": 0.2009,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "60ad1cccf479",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.557,
  "model_score": 0.5583,
  "style_score": 0.5551,
  "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "0927be7e788c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "6a77768d30f7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "33880e5ed669",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "7f80bc58267b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "70bb28bf5dde",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "47ac2c1e663e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "4985ed370b5d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "85a985779fd7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "129de0b0e52a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "9208f747d783",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.199,
  "model_score": 0.0287,
  "style_score": 0.4545,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
