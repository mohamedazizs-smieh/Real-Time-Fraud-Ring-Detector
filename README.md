# Real-Time Fraud Ring Detector
A project I'm building to learn data engineering. The goal is a streaming pipeline that spots groups of coordinated accounts manipulating product ratings. So far I have completed the first stage: a generator that creates synthetic rating events, including normal user activity and a simulated fraud ring.
## What works now
The generator creates 10,000 normal ratings from random users and products, plus 25 fraud ratings from 5 coordinated accounts. The fraud accounts all act within a one-hour burst window. Some give a product 5 stars to push it up (`allies_boost`), while others give a competing product 1 star to push it down (`competitors_nerf`). Every event includes an `is_fraud` ground-truth label, so downstream detection algorithms can be evaluated accurately.
Everything is configurable in `configs.yaml`: number of events, ID ranges, rating distributions, time windows, fraud attack strategies, and the random seed. Using the same seed guarantees reproducible data generation.


## Files

- `main.py`: reads the config, generates the events and writes the file
- `generate_events.py`: the code that creates normal and fraud events
- `configs.yaml`: all the settings
- `LICENCE`, `.python-version`, `.gitignore`


The events are written to `output/data.jsonl`, one JSON object per line:

```json
{"user_id": 2920, "product_id": 29, "rating": 3, "timestamp": "2025-04-14T12:29:33", "is_fraud": false}
{"user_id": 5003, "product_id": 10, "rating": 5, "timestamp": "2025-08-02T02:32:10", "is_fraud": true}
```

## What is missing

The title promises more than the repo does. There is no Kafka and no PySpark yet, only the data generator. My plan is to send these events through Kafka and then detect the fraud bursts with PySpark.

The data is also too easy. Fraud accounts use their own ID range (5001 to 5005), all attacks happen in one hour, and only two products are targeted. A very simple rule would catch them, so a good result on this data would prove little. I want to make the fraud harder to separate before judging any detector.


## What I'm doing next

- Write unit tests for event distributions and timestamp constraints
- Connect the generator to an Apache Kafka producer
- Build a PySpark Structured Streaming consumer to detect coordinated bursts
