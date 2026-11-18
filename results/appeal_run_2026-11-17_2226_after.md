# Appeal + bad-body run — after

- Produced by: `appeal_eval.py::one_trial`

**Trial 1**

```json
[
  {
    "check": "appeal 1",
    "content_id": "22a85fcd5188",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "22a85fcd5188",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "unsure",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 2",
    "content_id": "4e1dbe25d5ee",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "4e1dbe25d5ee",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "human",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 3",
    "content_id": "8fff294d9e2a",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "8fff294d9e2a",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "human",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 4",
    "content_id": "85c16994cf82",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "85c16994cf82",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "unsure",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 5",
    "content_id": "98e27ffcef8b",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "98e27ffcef8b",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "unsure",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "unknown content_id",
    "status_code": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No submission found with id 'does_not_exist_000'."
    },
    "pass": true
  },
  {
    "check": "bad body: body is a JSON array",
    "status_code": 400,
    "response": {
      "error": "invalid_json",
      "message": "Send a JSON object with 'text' and 'creator_id'."
    },
    "pass": true
  },
  {
    "check": "bad body: body is a JSON string",
    "status_code": 400,
    "response": {
      "error": "invalid_json",
      "message": "Send a JSON object with 'text' and 'creator_id'."
    },
    "pass": true
  },
  {
    "check": "bad body: body is unparseable",
    "status_code": 400,
    "response": {
      "error": "invalid_json",
      "message": "Send a JSON object with 'text' and 'creator_id'."
    },
    "pass": true
  },
  {
    "check": "/ping after bad input",
    "status_code": 200,
    "pass": true
  }
]
```

**Trial 2**

```json
[
  {
    "check": "appeal 1",
    "content_id": "2ef975df49af",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "2ef975df49af",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "unsure",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 2",
    "content_id": "cb5b716acf31",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "cb5b716acf31",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "human",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 3",
    "content_id": "25c3d3f442af",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "25c3d3f442af",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "human",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 4",
    "content_id": "3c1cebd5c43b",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "3c1cebd5c43b",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "unsure",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 5",
    "content_id": "c8e7a663c3ec",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "c8e7a663c3ec",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "unsure",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "unknown content_id",
    "status_code": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No submission found with id 'does_not_exist_000'."
    },
    "pass": true
  },
  {
    "check": "bad body: body is a JSON array",
    "status_code": 400,
    "response": {
      "error": "invalid_json",
      "message": "Send a JSON object with 'text' and 'creator_id'."
    },
    "pass": true
  },
  {
    "check": "bad body: body is a JSON string",
    "status_code": 400,
    "response": {
      "error": "invalid_json",
      "message": "Send a JSON object with 'text' and 'creator_id'."
    },
    "pass": true
  },
  {
    "check": "bad body: body is unparseable",
    "status_code": 400,
    "response": {
      "error": "invalid_json",
      "message": "Send a JSON object with 'text' and 'creator_id'."
    },
    "pass": true
  },
  {
    "check": "/ping after bad input",
    "status_code": 200,
    "pass": true
  }
]
```

**Trial 3**

```json
[
  {
    "check": "appeal 1",
    "content_id": "64a4c863c758",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "64a4c863c758",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "unsure",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 2",
    "content_id": "e19e0f4b3bfb",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "e19e0f4b3bfb",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "human",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 3",
    "content_id": "b97d1c6a1464",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "b97d1c6a1464",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "human",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 4",
    "content_id": "e5f0e60ce66d",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "e5f0e60ce66d",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "unsure",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "appeal 5",
    "content_id": "c0763d76cc10",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "c0763d76cc10",
      "message": "Thanks — your appeal is recorded. A person will review this piece, and the label won't be held against you in the meantime.",
      "original_guess": "unsure",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "original_decision_unchanged": true,
    "pass": true
  },
  {
    "check": "unknown content_id",
    "status_code": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No submission found with id 'does_not_exist_000'."
    },
    "pass": true
  },
  {
    "check": "bad body: body is a JSON array",
    "status_code": 400,
    "response": {
      "error": "invalid_json",
      "message": "Send a JSON object with 'text' and 'creator_id'."
    },
    "pass": true
  },
  {
    "check": "bad body: body is a JSON string",
    "status_code": 400,
    "response": {
      "error": "invalid_json",
      "message": "Send a JSON object with 'text' and 'creator_id'."
    },
    "pass": true
  },
  {
    "check": "bad body: body is unparseable",
    "status_code": 400,
    "response": {
      "error": "invalid_json",
      "message": "Send a JSON object with 'text' and 'creator_id'."
    },
    "pass": true
  },
  {
    "check": "/ping after bad input",
    "status_code": 200,
    "pass": true
  }
]
```
