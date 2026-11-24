# Real-Time Fraud Ring Detector
A project I'm building to learn data engineering. The goal is a streaming pipeline that spots groups of coordinated accounts manipulating product ratings. So far I have completed the first stage: a generator that creates synthetic rating events, including normal user activity and a simulated fraud ring.
## What works now
The generator creates 10,000 normal ratings from random users and products, plus 25 fraud ratings from 5 coordinated accounts. The fraud accounts all act within a one-hour burst window. Some give a product 5 stars to push it up (`allies_boost`), while others give a competing product 1 star to push it down (`competitors_nerf`). Every event includes an `is_fraud` ground-truth label, so downstream detection algorithms can be evaluated accurately.
Everything is configurable in `configs.yaml`: number of events, ID ranges, rating distributions, time windows, fraud attack strategies, and the random seed. One seeded `random.Random` object is passed through the generators, events are sorted by timestamp (ties by user, then product), and the same seed always produces a byte-identical file. Normal events have `ring_id: null`; today's single fraud ring has `ring_id: 0`.


## Files

- `main.py`: reads the config, builds the sorted event stream and writes the file
- `generate_events.py`: the code that creates normal and fraud events
- `configs.yaml`: all the settings
- `tests/`: pytest checks for counts, timestamps, ordering, ring IDs and byte-identical reruns
- `requirements.in` / `requirements.txt`: pip-tools source and pinned lock
- `LICENCE`, `.python-version`, `.gitignore`


The events are written to `output/data.jsonl`, one JSON object per line:

```json
{"ring_id": null, "user_id": 2920, "product_id": 29, "rating": 3, "timestamp": "2025-04-14T12:29:33", "is_fraud": false}
{"ring_id": 0, "user_id": 5003, "product_id": 10, "rating": 5, "timestamp": "2025-08-02T02:32:10", "is_fraud": true}
```

## How to run

From the project root, create a virtual environment and activate it:

- `python -m venv .venv`
- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

Then:

1. `pip install -r requirements.txt`
2. `python main.py`

To run the tests:

`python -m pytest -q`

The test suite includes a byte-identity check: running the generator twice with the same seed must produce the same file.

## What is missing

The title promises more than the repo does. There is no Kafka and no PySpark yet, only the data generator. My plan is to send these events through Kafka and then detect the fraud bursts with PySpark.

The data is also too easy. Fraud accounts use their own ID range (5001 to 5005), all attacks happen in one hour, and only two products are targeted. A very simple rule would catch them, so a good result on this data would prove little. I want to make the fraud harder to separate before judging any detector.
