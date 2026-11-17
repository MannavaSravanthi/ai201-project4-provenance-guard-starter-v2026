# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Human writing is rarely called AI

Of 10 pieces of human writing I didn't generate (at least 3 of them plain or formal, such as instructions, emails or school-style essays), **at most 1** gets the high-confidence AI label. This must hold in **each of 3 trials**.

**Why this target:** On a writing site, wrongly accusing a real person is the expensive mistake, much worse than letting some AI text through. One in ten is the most I'd accept. The plain and formal pieces are included on purpose, because that kind of writing is what a predictability-based detector most often gets wrong.

---

## 2. Clearly-AI and clearly-human text score far apart

The average combined score of 5 clearly AI-generated texts is **at least 0.30 higher** than the average of 5 clearly human texts, in each of 3 trials.

**Why this target:** The labels only mean something if the score separates the two kinds of text. My unsure band runs from 0.35 to 0.75, which is 0.40 wide, so a gap smaller than 0.30 would mean most texts land in "unsure" and the score tells the reader almost nothing.

---

## 3. All three labels are reachable

Across a test set of 15 texts (5 clearly AI, 5 clearly human, 5 borderline or lightly edited AI), **each of the three labels appears at least 2 times**.

**Why this target:** A label that never appears means my score ranges have a gap and I've built a three-label system that behaves like a two-label one. Requiring two appearances rather than one rules out a single lucky hit.

---

## 4. Every appeal is recorded and changes status

**5 out of 5** appeals sent with a real `content_id` return `status: under_review`. Each one adds an appeal entry to `logs/audit.jsonl` after the original decision, and the original decision is left unchanged. An appeal with an unknown `content_id` returns a **404** in 3 out of 3 attempts and never a 500.

**Why this target:** The appeal is the writer's only protection against a wrong label. If it fails even once, that writer has no way to push back. That's why the target is 100% and not a percentage.

---

## 5. Bad input never crashes the service

Each of these returns a **400** with a readable error message, in 3 out of 3 attempts, and the service keeps answering `/ping` afterwards:
- a missing `text` field
- empty or whitespace-only text
- text under 40 characters
- text over 20,000 characters
- a missing `creator_id`
- a body that isn't a JSON object

Each rejection is also written to the audit log.

**Why this target:** Malformed input is one of the most common real failures, and next unit's attack set will send exactly these. A crash gives the writer no answer and leaves no trace in the log, so I can't diagnose it.

---


<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
