"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# ── Human writing, for criterion 1 ───────────────────────────────────────────
# Ten real pieces of human writing: my own messages and emails, and messages
# people sent me. Names and private details swapped for neutral ones; the
# wording, typos and line breaks are untouched. None of it was generated.
# Pieces 1, 2, 5, 6, 7 and 10 are plain or formal; criterion 1 needs at least 3.

HUMAN = [
    # 1 — staffing-agency timesheet reminder (formal, plain)
    """Good morning,
This is a reminder that you have not submitted your time for the week ending in 11/14/2026 at 12:00 AM. These time sheets need to be submitted no later than noon on Monday, or this could result in a delay of your pay.
If you did not work any hours, you still need to submit a 0-hour timesheet in Pixid VMS and put your OOO (Out of Office) time in Workday.
If you are receiving this e-mail and have already put your time in, please double check to make sure it is not in DRAFT status.
Thank you!""",
    # 2 — my message to a roommate (plain)
    """Hello Maria!

I was wondering if we can get our own renter's insurance instead of taking it from the apartment complex.""",
    # 3 — my essay, part 1
    """Though the government service providers play their role
perfectly in this war , it is in our hands whether we make it a
successful war or ruin it because “UNITED WE STAND
DIVIDED WE FALL”""",
    # 4 — my essay, part 2
    """Still there are people in the society who feel
ashamed of telling about their sickness . This
causes a very great problem in making many
corona cases unknown .

The only solution is to conduct door to door
corona tests and make a list of cases.

Instead of sending them to the hospitals that are
near to the villages , isolation wards should be
kept in isolated areas so that we can stop the
spreading in villages (as many govt hospitals
are situated near rural areas).""",
    # 5 — my email to a recruiter (formal)
    """Hello Victoria,

I hope you are doing well. I'm a little concerned about my interview decision because I'm in the process of applying for a work permit, and the last date to apply is the end of this month. Knowing the decision beforehand would help me set a start date on my application.
Hope you understand my concern.
Thanks and regards,
Priya""",
    # 6 — a friend's referral message (plain)
    """Hi Priya,
I referred your profile. The role is related to Promt Engineering. If HR contacts you let me know. I can guide you on what type of questions you can expect in technical round.
Thanks,
Ravi""",
    # 7 — a recruiter's work email (plain, formal)
    """Hey Priya,

I just sent you the RTR and Rate Confirmation email. Please review and confirm them at your earliest convenience.
Also, please update your resume with your Angular project experience and send me the latest version as soon as possible.""",
    # 8 — a recruiter's LinkedIn message
    """Hi!

I wanted to see if you were available for new opportunities. A client of ours in Little Rock, AR is looking for an AWS Cloud Solutions Engineer to provide primary operational support and engineering for the public cloud platform, and debug and optimize systems and automate routine tasks. Let me know if this is something you would be interested in!!

Thank you!!""",
    # 9 — my LinkedIn reply
    """Hello Anna! thank you for reaching out. The role kind of sounds that needs more expertise and I may not be able to do justice for the role. But please do keep updating me on any Full-stack development roles your clients might be needing""",
    # 10 — an employee's LinkedIn answer about interviews (plain)
    """For this position, you should expect 2 interviews: one phone interview and one face to face. We do ask about technical experience but as a company, we emphasize personality and ones ability to collaborate and fit with the team. That being said you can expect more behavioral questions as well as questions regarding your background. In my experience the most important part of the interview was being personable as opposed to demonstrating technical skill. I hope that answers your questions!""",
]

# ── Clearly AI, for criteria 2 and 3 ─────────────────────────────────────────
# Generated in the style of a default chatbot answer: even sentences, stock
# transitions, no voice.

AI = [
    "In today's fast-paced world, technology plays an important role in our daily lives. It is important to note that technology has many benefits. It helps us communicate with others, access information, and complete tasks more efficiently. In conclusion, technology is an important part of our lives and will continue to be important in the future.",
    "Effective time management is essential for success in both personal and professional settings. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can improve their productivity. Additionally, taking regular breaks can help maintain focus and prevent burnout. Overall, developing strong time management skills can lead to greater efficiency and a better work-life balance.",
    "Climate change is one of the most significant challenges facing the world today. It is caused by the increase of greenhouse gases in the atmosphere, primarily due to human activities. The effects of climate change include rising temperatures, melting ice caps, and more frequent extreme weather events. It is important for individuals, businesses, and governments to work together to reduce emissions and protect the planet.",
    "Regular exercise offers numerous benefits for both physical and mental health. It helps strengthen the heart, improve circulation, and maintain a healthy weight. Furthermore, exercise can reduce stress, boost mood, and improve sleep quality. Incorporating physical activity into your daily routine is a simple yet effective way to enhance your overall well-being.",
    "Artificial intelligence is transforming the way businesses operate. By automating routine tasks, AI allows employees to focus on more strategic work. It also enables organizations to analyze large amounts of data and make better decisions. As AI technology continues to evolve, it is expected to play an even greater role in shaping the future of work.",
]

# ── Borderline, for criterion 3 ──────────────────────────────────────────────
# AI text that's been lightly edited by hand: a contraction here, a short
# sentence there, one aside. Meant to land in the middle of the range.

BORDERLINE = [
    "Remote work has changed how a lot of teams operate. It offers flexibility and cuts out the commute, which most people love. But it isn't perfect. Communication can suffer, and some people feel isolated working alone all day. Companies that want it to work need clear expectations and regular check-ins.",
    "Learning a new programming language can feel overwhelming at first. The syntax is unfamiliar, and the tooling takes time to set up. Still, the core ideas usually carry over. Start small, build something you actually care about, and don't worry too much about doing it the right way on day one.",
    "Social media has both positive and negative effects on society. On one hand, it keeps us connected with friends and family. On the other, it can spread misinformation pretty quickly. Honestly, I think the answer is somewhere in the middle: use it, but don't believe everything you read.",
    "Healthy eating doesn't have to be complicated. Focus on whole foods, lots of vegetables, and drinking enough water. Cutting back on processed snacks helps too. Small changes, made consistently, tend to stick better than big diets that last two weeks.",
    "Public libraries remain valuable community resources. Beyond books, they offer free internet access, study spaces, and programs for kids and adults. In many towns, the library is one of the few places you can spend an afternoon without spending money. That matters more than people think.",
]

SCENARIOS = [
    {
        "name": "human writing",
        "criterion": 1,
        "texts": HUMAN,
    },
    {
        # First five are clearly AI, last five clearly human (pieces 2, 3, 4, 8, 9).
        # Criterion 2 compares the average score of each half.
        "name": "score spread",
        "criterion": 2,
        "texts": AI + [HUMAN[1], HUMAN[2], HUMAN[3], HUMAN[7], HUMAN[8]],
    },
    {
        # 5 AI, 5 human, 5 borderline. Each label has to appear at least twice.
        "name": "label coverage",
        "criterion": 3,
        "texts": AI + [HUMAN[1], HUMAN[2], HUMAN[3], HUMAN[7], HUMAN[8]] + BORDERLINE,
    },
    # Criterion 4 (the appeal path) can't be expressed as submissions alone,
    # so it's tested by appeal_eval.py, which submits, appeals and checks the log.
    {
        # Each must come back 400 with a readable message, never a 500.
        # A body that isn't a JSON object can't be written here (bodies must be
        # dicts), so appeal_eval.py sends those too.
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},                       # no text field
            {"text": "", "creator_id": "eval_bad_empty"},             # empty
            {"text": "   \n\t  ", "creator_id": "eval_bad_space"},    # whitespace only
            {"text": "Too short.", "creator_id": "eval_bad_short"},   # under 40 chars
            {"text": "word " * 5000, "creator_id": "eval_bad_huge"},  # 25,000 chars
            {"text": "This has text but nobody sent a creator id with it at all."},  # no creator_id
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
