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

**The numbers** (all in `config.py`):
- `combined = 0.6 × model_score + 0.4 × style_score`
- `DISAGREEMENT_GAP = 0.45`
- `HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.75`. The AI band is deliberately narrower than the human band (0.25 wide vs 0.35), because calling a real writer's work AI is the expensive mistake.

**The split case this rule handles:** A short, punchy paragraph about climate change (dashes, a semicolon, a question, three-word sentences) scored **model 0.80** (predictable wording, so it reads AI) and **style 0.00** (lumpy, heavily punctuated, so it reads human). The gap is 0.80, well over 0.45, so the system isn't allowed to be confident. The weighted average (0.6 × 0.80 + 0.4 × 0.00 = **0.48**) already lands in the unsure band, and the disagreement rule guarantees it stays there. Label: *unsure*.

**A finding from calibration:** A plain, conventional report-style paragraph ("The purpose of this report is to describe the results of the quarterly review...") scored **model 0.78, style 0.99 → 0.865 → high-confidence AI**. Both signals agreed, so the disagreement rule didn't help. Writing like this could just as easily come from a person, and this is the false positive my criterion 1 exists to catch. Plain, even prose is the blind spot both signals share, and I expect next unit's attack set to hit it.

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

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "Artificial intelligence is transforming many industries. It improves efficiency and helps organizations make better decisions. Many companies are adopting AI tools to streamline their operations. These technologies offer significant benefits for businesses of all sizes.", "creator_id": "sravanthi"}'
```

```json
{
  "confidence": 0.7628,
  "content_id": "c55df9d9e7ad",
  "creator_id": "sravanthi",
  "guess": "ai",
  "label": "This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it.",
  "model_score": 0.8046,
  "status": "decided",
  "style_score": 0.7
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "c55df9d9e7ad", "reasoning": "I wrote this myself for a class assignment."}'
```

```json
{
  "content_id": "c55df9d9e7ad",
  "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
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
  "count": 2,
  "entries": [
    {
      "combined_score": 0.7628,
      "content_id": "c55df9d9e7ad",
      "creator_id": "sravanthi",
      "guess": "ai",
      "label": "This piece reads a lot like text generated by an AI tool. That's an automated guess, not a verdict, and it can be wrong. If you wrote this yourself, you can ask for a person to review it.",
      "model_score": 0.8046,
      "status": "decided",
      "style_score": 0.7,
      "text_length": 270,
      "timestamp": "2026-11-17T02:42:19+00:00"
    },
    {
      "content_id": "c55df9d9e7ad",
      "creator_id": "sravanthi",
      "event": "appeal",
      "reasoning": "I wrote this myself for a class assignment.",
      "status": "under_review",
      "timestamp": "2026-11-17T02:43:24+00:00"
    }
  ]
}
```

The original decision is untouched. The appeal sits after it with `status: under_review`.

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



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
