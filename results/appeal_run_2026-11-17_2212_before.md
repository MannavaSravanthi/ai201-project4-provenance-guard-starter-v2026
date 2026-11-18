# Appeal + bad-body run — before

- Produced by: `appeal_eval.py::one_trial`

**Trial 1**

```json
[
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
  },
  {
    "check": "appeal 2",
    "content_id": "f8be975dddd8",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "f8be975dddd8",
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
    "content_id": "5a994a306239",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "5a994a306239",
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
    "content_id": "374a8c66bfa3",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "374a8c66bfa3",
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
    "content_id": "38b2b21efa4e",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "38b2b21efa4e",
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
    "content_id": "da1ecc2c3a5d",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "da1ecc2c3a5d",
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
    "content_id": "76d4d768b0d9",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "76d4d768b0d9",
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
    "content_id": "443a6b29892f",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "443a6b29892f",
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
    "content_id": "15138b6b2130",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "15138b6b2130",
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
    "content_id": "a6f38eee8411",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "a6f38eee8411",
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
    "content_id": "ada529130cfd",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "ada529130cfd",
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
    "content_id": "a795809b9360",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "a795809b9360",
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
    "content_id": "25c1aa927aa9",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "25c1aa927aa9",
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
    "content_id": "404bb1a19853",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "404bb1a19853",
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
    "content_id": "c54d0e4bd10e",
    "appeal_status_code": 200,
    "appeal_response": {
      "content_id": "c54d0e4bd10e",
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
  },
  {
    "check": "/ping after bad input",
    "status_code": 200,
    "pass": true
  }
]
```
