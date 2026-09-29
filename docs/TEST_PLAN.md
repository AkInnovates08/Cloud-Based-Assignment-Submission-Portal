# Manual Test Matrix

| ID | Scenario | Input | Expected Result | Actual | Pass/Fail |
|---|---|---|---|---|---|
| T01 | Student registration | Valid student | Account created | Fill after run | |
| T02 | Teacher login | Valid credentials | Token returned | | |
| T03 | Invalid login | Wrong password | 401 | | |
| T04 | Student dashboard authorization | Student calls teacher endpoint | 403 | | |
| T05 | Teacher dashboard authorization | Teacher calls teacher endpoint | 200 | | |
| T06 | Create assignment | Valid course/data | 201 | | |
| T07 | View assignment | GET list | Assignment visible | | |
| T08 | Valid PDF upload | PDF <= limit | 201 | | |
| T09 | Invalid extension | EXE | 400 | | |
| T10 | Oversized file | > configured limit | 413 | | |
| T11 | On-time submission | Before deadline | SUBMITTED | | |
| T12 | Late submission | After deadline | LATE | | |
| T13 | Resubmission | Second valid file | Existing submission updated | | |
| T14 | Own submission | Student A reads A | 200 | | |
| T15 | Other submission | Student A reads B | 403 | | |
| T16 | Teacher submissions | Owner teacher | 200 | | |
| T17 | Grade | Valid marks | GRADED | | |
| T18 | Over-max marks | 101/100 | 400 | | |
| T19 | Feedback | Student reads own | 200 | | |
| T20 | Unauthorized grading | Student grades | 403 | | |
| T21 | File retrieval | Authorized download | File returned | | |
| T22 | Storage failure | Missing file | 404 | | |
| T23 | Database failure | Stop DB | Graceful 503/5xx | | |
| T24 | Logout | Logout | Client token removed | | |
| T25 | Protected after logout | No token | 401 | | |

Automated tests are in `tests/test_api.py`.
