# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard takes a piece of writing, guesses whether a person or an AI tool wrote it, says how sure it is, and gives the writer a way to push back. The path a submission takes:

1. **`POST /submit` receives JSON** with `text` and `creator_id` (`app.py::submit`).
2. **Input check.** Missing or empty text, text under 40 characters, text over 20,000 characters, a missing `creator_id`, or a body that isn't a JSON object all get a `400` with a plain reason. The rejection is still written to the audit log.
3. **Signal one, the model signal** (`detector.py::model_signal`). GPT-2 runs locally and measures how predictable the text is (perplexity), squashed to 0–1. Higher means more AI-like.
4. **Signal two, the style signal** (`stylometry.py::style_signal`). Measures the shape of the text (sentence-length spread, vocabulary variety, expressive punctuation) as a 0–1 score. Higher means more AI-like.
5. **Combine** (`scoring.py::combine_signals`). A weighted average, plus a rule that forces the score into "unsure" when the two signals strongly disagree.
6. **Label** (`scoring.py::score_to_label`). The score becomes one of three guesses (`human` / `unsure` / `ai`) and the sentence the reader sees.
7. **Log and answer.** Every decision goes to `logs/audit.jsonl` through `audit.log_decision`, with both signal scores, the combined score, the label and `status: decided`. The response returns a `content_id`, which the writer can pass to **`POST /appeal`**. The appeal is logged next to the original decision and moves the item to `under_review`.

**Stretch feature added:** `GET /content/<id>` returns one item's current status, its original decision, and any appeals.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** How predictable the text is to GPT-2 (perplexity over the first ~400 tokens), mapped to 0–1 with a logistic curve centred on perplexity 45.

**Why that might differ between human and AI writing:** A language model generates by picking likely next words, so its output tends to be text a model finds unsurprising. People make odder word choices, use personal references and break patterns.

**What it can't see:** Who wrote it or how. It only sees predictability. Plain, conventional human writing (instructions, formulaic school essays, non-native writers using safe phrasing) is predictable too and scores AI-like. That's the false positive this project is most worried about. In the other direction, AI text pushed toward unusual wording (a high-temperature sample, or a human paraphrasing it) scores human. Very short texts barely move it.

### Signal two — the style signal

**What it measures:** Three things about the text's shape, ignoring its meaning (`stylometry.py`):

| Measure | How it's computed | "AI-ish" end → "human-ish" end | Weight |
|---|---|---|---|
| `sentence_length_spread` | stdev ÷ mean of sentence lengths (words) | 0.25 → 0.65 | 0.45 |
| `type_token_ratio` | unique/total words over a moving 50-word window (MATTR), so length doesn't distort it | 0.70 → 0.85 | 0.30 |
| `punctuation_density` | `; : ! ? ( ) — –` quotes and ellipses per 100 words (full stops and commas ignored) | 0.5 → 5.0 | 0.25 |

Each measure is mapped linearly onto 0–1 "human-ness" between those two anchors (and clipped). The weighted sum is flipped so that **higher = more AI**, matching signal one. With fewer than two sentences there's no spread to measure, so that weight is dropped and the other two are renormalised. A missing measure shouldn't count as evidence of AI.

**Why that might differ between human and AI writing:** Generated prose tends toward even, mid-length sentences, a steady vocabulary and tidy punctuation. Human writing is lumpier: a three-word sentence next to a forty-word one, dashes, asides, questions.

**What it can't see:** Meaning. Anything that changes the shape without changing the substance moves it. Chopping AI sentences into uneven pieces, sprinkling in dashes and question marks, or pasting in a quotation all push it toward "human". In the other direction, a careful human writer with an even, plain style (or one writing a list-like piece) looks AI-ish. It's also noisy on short texts.

### The combining rule

**The rule:**
1. Take a weighted average that leans on the model signal, because the style signal is the cheaper one to fool.
2. **Disagreement rule:** if the two signals are more than 0.45 apart, the system isn't allowed to be confident. The combined score is clamped into the unsure band (0.36–0.74). Two methods disagreeing *is* uncertainty, and nobody should be labelled AI on the strength of one signal alone.

3. **Model floor (added after calibration):** the AI label is only possible when the model signal *by itself* is at least 0.85. Otherwise the score is capped at 0.74 (unsure). The style signal is cheap to max out (plain, even prose hits 0.99), so it's never allowed to tip text into an accusation.

**The numbers** (all in `config.py`):
- `combined = 0.6 × model_score + 0.4 × style_score`
- `DISAGREEMENT_GAP = 0.45`
- `MODEL_FLOOR_FOR_AI = 0.85`
- `HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.75`. The AI band is deliberately narrower than the human band (0.25 wide vs 0.35), because calling a real writer's work AI is the expensive mistake.

**The split case this rule handles:** A short, punchy paragraph about climate change (dashes, a semicolon, a question, three-word sentences) scored **model 0.80** (predictable wording, so it reads AI) and **style 0.00** (lumpy, heavily punctuated, so it reads human). The gap is 0.80, well over 0.45, so the system isn't allowed to be confident. The weighted average (0.6 × 0.80 + 0.4 × 0.00 = **0.48**) already lands in the unsure band, and the disagreement rule guarantees it stays there. Label: *unsure*.

**A finding from calibration:** A plain, conventional report-style paragraph ("The purpose of this report is to describe the results of the quarterly review...") scored **model 0.78, style 0.99 → 0.865 → high-confidence AI**. Both signals agreed, so the disagreement rule didn't help. Writing like this could just as easily come from a person, and this is the false positive my criterion 1 exists to catch. Plain, even prose is the blind spot both signals share, and I expect next unit's attack set to hit it.

**What I changed because of it:** I added the model floor (rule 3). With it, that paragraph's 0.865 is capped to 0.74 and labelled *unsure* rather than AI. The trade-off: AI text that the model scores between 0.75 and 0.85 now gets through as "unsure" instead of being flagged. I accept that, because a missed detection costs less than a wrong accusation.

**Where it lives:** `scoring.py::combine_signals`

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – below 0.35 | We think this was written by a person. |
| unsure | 0.35 – 0.75 | We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way. |
| high-confidence AI | above 0.75 – 1.00 | This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it. |

Every score from 0 to 1 falls into exactly one band (`scoring.label_ranges()` prints them), and all three were reached in testing.

**Why I worded the "unsure" one this way:**
The person reading "unsure" may well have written every word themselves, so the label must not sound like a softer accusation. It says plainly that the system couldn't tell, says that this happens with lots of genuine writing (so the reader knows it isn't about them), and says outright that no claim is being made either way. It deliberately leaves out the word "AI-generated" on its own, any score, and any mention of appealing. Offering an appeal would imply there's something to defend against.

---

## Sample Run

Run after the model-floor change (see Signals and Scoring), so this is the current behaviour.

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "In today'"'"'s fast-paced world, technology plays an important role in our daily lives. It is important to note that technology has many benefits. It helps us communicate with others, access information, and complete tasks more efficiently. In conclusion, technology is an important part of our lives and will continue to be important in the future.", "creator_id": "sravanthi"}'
```

```json
{
  "confidence": 0.9262,
  "content_id": "e59a109d4d56",
  "creator_id": "sravanthi",
  "guess": "ai",
  "label": "This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it.",
  "model_score": 0.947,
  "status": "decided",
  "style_score": 0.8949
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "e59a109d4d56", "reasoning": "I wrote this myself for a class assignment."}'
```

```json
{
  "content_id": "e59a109d4d56",
  "message": "Thanks \u2014 your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
  "original_guess": "ai",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.4786,
      "content_id": "ca2f58c0b6a1",
      "creator_id": "sravanthi",
      "guess": "unsure",
      "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.",
      "model_score": 0.7977,
      "status": "decided",
      "style_score": 0.0,
      "text_length": 228,
      "timestamp": "2026-11-17T02:45:06+00:00"
    },
    {
      "combined_score": 0.9262,
      "content_id": "e59a109d4d56",
      "creator_id": "sravanthi",
      "guess": "ai",
      "label": "This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it.",
      "model_score": 0.947,
      "status": "decided",
      "style_score": 0.8949,
      "text_length": 345,
      "timestamp": "2026-11-17T03:06:55+00:00"
    },
    {
      "content_id": "e59a109d4d56",
      "creator_id": "sravanthi",
      "event": "appeal",
      "reasoning": "I wrote this myself for a class assignment.",
      "status": "under_review",
      "timestamp": "2026-11-17T03:07:43+00:00"
    }
  ]
}
```

The original decision for `e59a109d4d56` is untouched. The appeal sits after it with `status: under_review`.

---

## How I Used AI

I used Claude for most of the implementation and for drafting my criteria.

**Moment 1: building the service, then catching a false positive in my own testing**

- *What I asked for:* Help finishing the build: `/submit`, `/appeal`, the style signal and the combining rule.
- *What came back:* Working code: `stylometry.py` (three measures ramped to 0–1 and weighted 0.45/0.30/0.25), `scoring.py::combine_signals` (0.6 model / 0.4 style, plus a rule forcing strong disagreements into "unsure"), input validation, and the appeal route.
- *What I changed:* When I ran my own test inputs, a plain report-style paragraph ("The purpose of this report is to describe the results of the quarterly review...") was labelled **high-confidence AI** at 0.865, even though it reads like ordinary human writing. Both signals agreed, so the disagreement rule didn't catch it. Of three possible fixes (a model-score floor, lower style weight, or gentler label wording), I chose the **model floor**: the AI label now needs `model_score >= 0.85` on its own. That paragraph now scores 0.74 (unsure), and clearly generic AI text (model 0.947) still gets the AI label.

**Moment 2: the acceptance criteria**

- *What I asked for:* Five acceptance criteria with reasons.
- *What came back:* Criteria covering false positives, score spread, label coverage, the appeal path and bad input, each with a number.
- *What I changed:* I reviewed them against my own build before committing them first (commit `9841913`), so they existed before any results. Running my tests afterwards showed criterion 1 (at most 1 of 10 human pieces labelled AI) is a real risk for plain writing, which is what led to the change in Moment 1.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 100 per day (set in `config.py`, applied with `@limiter.limit(...)` on `app.py::submit`)

**Why those numbers and not others:** A real writer submits a few pieces an hour, perhaps resubmitting a couple of times after edits. Ten a minute never gets in their way, even if they paste several drafts in quick succession. A script trying to map my thresholds by sending 1,000 small variations of one text would be capped at 100 a day, so it needs ten days per `creator_id` instead of a few minutes. I didn't go lower (say 3 a minute) because a writer fixing typos and resubmitting would hit it. I didn't go higher on the daily cap because nobody genuinely needs 100+ verdicts a day on their own writing.

**What a caller counts as:** The `creator_id` in the request body, falling back to the caller's IP address when there's no usable `creator_id` (`app.py::rate_limit_key`). Per-creator means a household or office sharing one IP doesn't share one limit. The weakness is the opposite: an attacker can rotate through made-up `creator_id`s and look like a thousand different writers. Real per-creator limits need `creator_id` to be an authenticated account, not a free-text field.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15`, from `results/flood_2026-11-17_2135.md`:

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

Each `429` is also written to the audit log by the starter's 429 handler:

```json
{"timestamp": "2026-11-18T03:35:41+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"}
```

**The log:** every decision records all nine fields: `timestamp`, `content_id`, `creator_id`, `guess`, `model_score`, `style_score`, `combined_score`, `label`, `status`. Requests my own route refuses (missing, empty, too short or too long text, missing `creator_id`, non-object JSON) are logged as `rejected` with a reason, through `audit.log_rejection` in `app.py::_reject`.

---

## Attack Run — Before

`python run_attacks.py --set attack_set --label before`, giving `results/attack_run_2026-11-17_2141_before.md`. 56 attacks, 0 crashes, 0 5xx responses.

**How I marked them.** *Evasion* and *prompt-injection* rows built on AI text are **BROKE** if the AI text didn't get the high-confidence AI label. "Unsure" counts as getting through, because only the AI label stops anything. *False-positive* rows are **BROKE** if real human writing got the AI label. *Malformed* rows are **HELD** if refused cleanly (400) and **BROKE** if junk got a verdict. *Flood* rows are **HELD** if the limiter stepped in once the creator passed 10 a minute.

| Family | Held | Broke |
|---|---|---|
| evasion | 1 | 9 |
| false_positive | 7 | 1 |
| prompt_injection | 3 | 3 |
| malformed | 17 | 3 |
| flood_same_creator | 12 | 0 |
| **Total** | **40** | **16** |

| ID | Family | Targeting | Status | Guess | Score | model | style | Verdict | Note |
|---|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.378 | 0.164 | 0.700 | **BROKE** | AI text not labelled AI. Typos sent signal one to 0.16; style stayed 0.70 |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.394 | 0.594 | 0.095 | **BROKE** | AI text landed unsure; style fell to 0.09 |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.520 | 0.666 | 0.301 | **BROKE** | AI text landed unsure |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.647 | 0.611 | 0.700 | **BROKE** | unusual words cut model to 0.61; unsure |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.277 | 0.321 | 0.210 | **BROKE** | labelled human outright; both signals fooled |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.445 | 0.573 | 0.252 | **BROKE** | AI text landed unsure; style 0.25 |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.360 | 0.586 | 0.017 | **BROKE** | punctuation padding drove style to 0.02; unsure |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.412 | 0.245 | 0.663 | **BROKE** | too short for signal one (model 0.25); unsure |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.605 | 0.704 | 0.455 | **BROKE** | human opening diluted both signals; unsure |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.923 | 0.979 | 0.838 | **HELD** | repetition made it more predictable; caught as AI |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.592 | 0.618 | 0.554 | **HELD** | not accused (unsure) |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.740 | 0.739 | 0.861 | **HELD** | unsure, but only because the model floor capped it at 0.74 |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.740 | 0.805 | 0.673 | **HELD** | unsure, capped by the model floor (would be 0.752, AI) |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.740 | 0.833 | 0.627 | **HELD** | unsure, capped by the model floor (would be 0.750) |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | 0.740 | 0.800 | 0.970 | **HELD** | unsure, capped by the model floor (would be 0.868, AI) |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | 0.763 | 0.881 | 0.585 | **BROKE** | human cover letter labelled AI (model 0.88 cleared the floor) |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.749 | 0.882 | 0.550 | **HELD** | unsure at 0.749, 0.001 under the AI line |
| FP08 | false_positive | very short genuine human submission | 400 | — | — | — | — | **HELD** | not accused, but refused with 400 (under 40 chars) |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.378 | 0.463 | 0.250 | **BROKE** | instruction ignored, but the AI text underneath landed unsure, not AI |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.184 | 0.204 | 0.154 | **BROKE** | got the human label it asked for (0.18): the prefix raised perplexity |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.495 | 0.594 | 0.345 | **BROKE** | AI text underneath landed unsure |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.438 | 0.500 | 0.345 | **HELD** | label text is a fixed constant; the script tag never reaches it |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.464 | 0.640 | 0.201 | **HELD** | log line intact; json.dumps escaped the injected quotes |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.557 | 0.558 | 0.555 | **HELD** | real human text not accused; instruction had no effect |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | **HELD** | rejected with 400 |
| MF02 | malformed | text is a single character | 400 | — | — | — | — | **HELD** | rejected with 400 |
| MF03 | malformed | text is control characters | 400 | — | — | — | — | **HELD** | rejected with 400 |
| MF04 | malformed | text is only punctuation | 400 | — | — | — | — | **HELD** | rejected with 400 |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.740 | 0.998 | 0.455 | **BROKE** | junk got a verdict (unsure 0.74) instead of a 400 |
| MF06 | malformed | text is emoji only | 200 | ai | 0.998 | 0.997 | 1.000 | **BROKE** | emoji-only post labelled AI at 0.998 |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.944 | 0.906 | 1.000 | **BROKE** | Arabic text labelled AI at 0.944 |
| MF08 | malformed | text is 60,000 characters | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ01 | malformed | no text field at all | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ02 | malformed | no creator_id | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ03 | malformed | text is a number | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ04 | malformed | text is a list | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ05 | malformed | text is null | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ06 | malformed | creator_id is an object | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ09 | malformed | body is empty | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | — | — | **HELD** | rejected with 400 |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | — | — | **HELD** | rejected with 400 |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.199 | 0.029 | 0.455 | **HELD** | under the limit, served normally |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | rate limited (429), logged |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | rate limited (429), logged |
| `evasion` | 10 | 0 | None | — | — | — | — | **?** |  |
| `false_positive` | 8 | 0 | None | — | — | — | — | **?** |  |
| `flood_same_creator` | 12 | 0 | None | — | — | — | — | **?** |  |
| `malformed` | 20 | 0 | None | — | — | — | — | **?** |  |
| `prompt_injection` | 6 | 0 | None | — | — | — | — | **?** |  |

**Ten audit log entries from the run**

From `logs/audit.jsonl`. These are the interesting failures plus one route rejection and one rate-limit rejection:

```json
{"timestamp": "2026-11-18T03:41:33+00:00", "content_id": "48535a7efe52", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 1.0, "combined_score": 0.9438, "label": "This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it.", "status": "decided", "text_length": 105}
{"timestamp": "2026-11-18T03:41:31+00:00", "content_id": "c0311b5418c6", "creator_id": "attacker_FP06", "guess": "ai", "model_score": 0.8814, "style_score": 0.5852, "combined_score": 0.7629, "label": "This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it.", "status": "decided", "text_length": 353}
{"timestamp": "2026-11-18T03:41:33+00:00", "content_id": "97139eb6400a", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 1.0, "combined_score": 0.9981, "label": "This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it.", "status": "decided", "text_length": 200}
{"timestamp": "2026-11-18T03:41:31+00:00", "content_id": "88f4bdf6cf01", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.1543, "combined_score": 0.1844, "label": "We think this was written by a person.", "status": "decided", "text_length": 322}
{"timestamp": "2026-11-18T03:41:30+00:00", "content_id": "1a7162d8805a", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.21, "combined_score": 0.2767, "label": "We think this was written by a person.", "status": "decided", "text_length": 460}
{"timestamp": "2026-11-18T03:41:27+00:00", "content_id": "2d5c0d3ead14", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.7, "combined_score": 0.3781, "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.", "status": "decided", "text_length": 657}
{"timestamp": "2026-11-18T03:41:31+00:00", "content_id": "0462337c0fa8", "creator_id": "attacker_FP03", "guess": "unsure", "model_score": 0.8051, "style_score": 0.6732, "combined_score": 0.74, "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.", "status": "decided", "text_length": 418}
{"timestamp": "2026-11-18T03:41:32+00:00", "content_id": "e3ad9fcb3a3b", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.2009, "combined_score": 0.4644, "label": "We couldn't tell whether this was written by a person or with an AI tool. That happens with lots of genuine writing, so we're not making any claim about it either way.", "status": "decided", "text_length": 213}
{"timestamp": "2026-11-18T03:41:33+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "text_too_long", "text_length": 57639}
{"timestamp": "2026-11-18T03:41:33+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"}
```

In order: Arabic text accused (MF07); a human cover letter accused (FP06); emoji accused (MF06); an injection prefix that got the human label (PI02); a heavy human edit of AI text passing as human (EV05); typos collapsing signal one (EV01); a non-native writer saved only by the model floor (FP03); the log-injection attempt sitting harmlessly escaped in its own line (PI05); a 60,000-character body refused with 400 (MF08); and a flood row rejected with 429.

**The single worst outcome:** **MF07.** A short paragraph of ordinary Arabic was labelled *high-confidence AI* at 0.944. Nothing about the writing caused that: my style signal only counts Latin letters (`[a-z0-9']`), so it found zero words, scored the text as having no vocabulary and no punctuation, and returned 1.0. GPT-2, which barely knows Arabic, also scored it as predictable (0.91). Every writer who doesn't write in English would be told their work looks AI-generated. That isn't a borderline call I could defend to them; it's the system not being able to read their language at all.

---

## Run Log and Verdicts

`python run_eval.py --label before` (criteria 1, 2, 3, 5), giving `results/run_2026-11-17_2211_before.md`. Then `python appeal_eval.py --label before` (criterion 4 and the non-object bodies of criterion 5), giving `results/appeal_run_2026-11-17_2212_before.md`. The scenarios are in `scenarios.py`. `run_eval.py` can't send appeals, so I wrote `appeal_eval.py` to submit, appeal and read the log back.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Human writing rarely called AI | ≤ 1 of 10 labelled AI | 0/10 | 0/10 | 0/10 | **MET** |
| 2. Clearly-AI vs clearly-human spread | AI avg − human avg ≥ 0.30 | 0.548 | 0.548 | 0.548 | **MET** |
| 3. All three labels reachable | each label ≥ 2 of 15 | AI 3 · unsure 9 · human 3 | AI 3 · unsure 9 · human 3 | AI 3 · unsure 9 · human 3 | **MET** |
| 4. Every appeal recorded and changes status | 5/5 appeals OK and unknown id → 404 | 5/5 · 404 | 5/5 · 404 | 5/5 · 404 | **MET** |
| 5. Bad input → 400, never a crash | 9/9 bad requests → 400, `/ping` still up | 9/9 | 9/9 | **7/9** (two came back 429) | **MISSED** |

All three trials gave identical scores. Neither signal has any randomness in it, so that's expected.

**How I decided each verdict:**
1. Of my 10 human pieces, the highest score was 0.553 (piece 10). None reached the AI band in any trial.
2. Clearly-AI average was 0.823 (0.926, 0.740, 0.875, 0.827, 0.748) and clearly-human average was 0.275 (0.360, 0.101, 0.315, 0.369, 0.230). The gap is 0.548 in every trial.
3. All three labels appeared at least twice in every trial. All 5 borderline texts landed in unsure, and 2 of the 5 "clearly AI" texts also landed in unsure (capped at 0.74 by the model floor).
4. Every appeal returned `under_review`, the log held exactly one original decision followed by the appeal, and the made-up id returned 404 in all three trials.
5. Trials 1 and 2 were 9/9. In trial 3, two of the non-object bodies came back **429, not 400**. The target was 400 in 3 out of 3 attempts, so this is a miss, even though nothing crashed and `/ping` stayed up.

**Real output from one trial** (trial 1).

Criterion 1, `run_eval.py::main`, the first three of ten:

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4995,
    "model_score": 0.6647,
    "style_score": 0.2517,
    "sent": "Good morning,\nThis is a reminder that you have not submitted your time"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.36,
    "model_score": 0.5117,
    "style_score": 0.0132,
    "sent": "Hello Maria!\n\nI was wondering if we can get our own renter's insurance"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.1009,
    "model_score": 0.104,
    "style_score": 0.0963,
    "sent": "Though the government service providers play their role\nperfectly in t"
  }
]
```

Criterion 3, `run_eval.py::main`, label counts across the 15 texts: `{'ai': 3, 'unsure': 9, 'human': 3}`.

Criterion 4, `appeal_eval.py::one_trial`, the first appeal:

```json
{
  "check": "appeal 1",
  "content_id": "a10be89d65e6",
  "appeal_status_code": 200,
  "appeal_response": {
    "content_id": "a10be89d65e6",
    "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
    "original_guess": "unsure",
    "status": "under_review"
  },
  "log_entries_for_id": 2,
  "original_decision_unchanged": true,
  "pass": true
}
```

Criterion 5, `run_eval.py::main`, the first three bad bodies:

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "   \n\t  "
  }
]
```

Criterion 5, `appeal_eval.py::one_trial`, **trial 3**, the two that missed:

```json
[
  {
    "check": "bad body: body is a JSON string",
    "status_code": 429,
    "response": {
      "error": "rate_limited",
      "limit": "10 per 1 minute",
      "message": "Too many submissions. Try again shortly."
    },
    "pass": false
  },
  {
    "check": "bad body: body is unparseable",
    "status_code": 429,
    "response": {
      "error": "rate_limited",
      "limit": "10 per 1 minute",
      "message": "Too many submissions. Try again shortly."
    },
    "pass": false
  }
]
```

**Diagnoses**

*Criterion 5 (missed).* **Stage: the route, specifically the rate limiter in front of it.** **Mechanism:** a request with no usable `creator_id` (a JSON array, a bare string, unparseable JSON) can't be keyed by creator, so `app.py::rate_limit_key` falls back to the caller's IP address. Every such request in the whole eval came from my laptop's one address. By trial 3, the earlier trials' bad bodies plus `run_eval.py`'s no-`creator_id` body had used up the 10-a-minute allowance for that address. Flask-Limiter runs *before* my handler, so those requests were refused with 429 before my validation could return 400. Nothing crashed, and both refusals are in the audit log. But a caller sending a bad request got "slow down" instead of "your request is malformed", which is the wrong answer.

*Attack set: 16 broken, falling into four patterns.*

1. **Text my style signal can't read gets scored as maximally AI (MF06, MF07, MF05).** **Stage: signal two, and the route for letting it through.** `stylometry.words()` only matches `[a-z0-9']`. Arabic and emoji contain zero matches, so there are no sentences of words, a type-token ratio of 0 and no punctuation it recognises, and every measure ramps to "AI". The result is `style_score = 1.0`. GPT-2 also finds repetitive or out-of-vocabulary byte sequences predictable (0.91–0.997). Both signals point the same way, so neither the disagreement rule nor the model floor applies, and the combined score clears 0.75. MF05 (one 400-character word) got the same treatment, only clamped to unsure by the disagreement rule. **This is the worst failure: a non-English writer is told their work looks AI-generated.**

2. **Evasion lands in "unsure" because the AI band is deliberately hard to reach (EV01–EV04, EV06–EV09, PI01, PI03).** **Stage: the combining rule.** **Mechanism:** an AI label needs `combined > 0.75` *and* `model_score ≥ 0.85`. Any edit that knocks the model score below 0.85 or pulls the style score down lands in unsure: unusual words (EV04, model 0.61), typos (EV01), a short text (EV08), a bolted-on human opening (EV09, model 0.70), or chopped-up and punctuation-padded sentences (EV02, EV06, EV07, style 0.02–0.25). This is the cost of the model floor I added in unit 7 to protect human writers. The same floor is why FP02–FP05 held, so it's a trade I chose, not an accident.

3. **Odd tokens raise perplexity, and signal one reads that as human (EV01, PI02, EV05).** **Stage: signal one.** **Mechanism:** perplexity goes up for anything GPT-2 didn't expect, not only for human choices. Typos took EV01 to `model_score` 0.16. PI02's injected line (all-caps "SYSTEM:", `guess=human`, `confidence=0.02`) took AI text to 0.20, which earned the **human** label (0.18). The instruction itself was never *obeyed*, since nothing in my pipeline reads text as commands. It just looked statistically strange. EV05 is a real human edit of AI text, so labelling it human is arguably correct.

4. **Formulaic human writing clears the model floor (FP06).** **Stage: signal one.** **Mechanism:** a stock cover letter ("Dear Sir or Madam, I am writing to enquire...") is as predictable to GPT-2 as AI text (model 0.88, above the 0.85 floor). The style signal was only middling (0.59), so the 0.6/0.4 average reached 0.763, just over 0.75. FP07 (0.749) and FP02–FP05 (capped at 0.74) were within 0.01 of the same outcome.

**Patterns:** patterns 3 and 4 are the same blind spot of signal one seen from opposite sides: predictable means AI, surprising means human, regardless of who wrote it. Pattern 1 is a separate, more serious hole: the system scores text it can't read rather than refusing it.

**Were my targets too low?** Criteria 1–4 were all met, and criterion 1 was met comfortably (0/10). But the attack set's own false-positive family got one accusation through and nearly five more, so my 10 pieces were easier than real plain writing can be. If I tightened anything, it would be criterion 1: at least 5 of the 10 pieces should be template-style formal writing, the kind FP06 shows can break it.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
