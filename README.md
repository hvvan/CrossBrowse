# CrossBrowse

Anonymized repository for double-blind review.

CrossBrowse is a benchmark for browsing agents that must find and combine local facts published in different languages.
Each question asks for a single number that is derived by retrieving two to four facts, each reported by a regional news organization in a different language, and combining them with a sum or a difference.
One fact is always reported in English. The others are reported in Spanish, Japanese, Korean, Hindi, Georgian, or Nepali.
Every question is provided in all seven languages.

## Contents

| Path | Description |
|---|---|
| `data/crossbrowse.jsonl` | 310 questions, one JSON object per line |
| `data/response_format.json` | Response format instruction appended to each question at evaluation time, per language |
| `data/main_experiment_ids.txt` | IDs of the 100 questions used in the main experiments |
| `scripts/check_data.py` | Self-check that recomputes every answer from its supporting facts and prints the statistics below |

## Statistics

- 310 questions. Type-1 168, Type-2 90, Type-3 52. A Type-*k* question combines one English fact with *k* facts in *k* other languages.
- 282 distinct supporting facts from 80 regional news organizations.
- 8 global topics and 5 domains.

| Fact language | Questions | Facts | News organizations |
|---|---|---|---|
| English (`en`) | 310 | 60 | 22 |
| Spanish (`es`) | 102 | 50 | 10 |
| Japanese (`ja`) | 91 | 38 | 6 |
| Korean (`ko`) | 104 | 62 | 6 |
| Hindi (`hi`) | 65 | 17 | 11 |
| Georgian (`ka`) | 73 | 25 | 11 |
| Nepali (`ne`) | 69 | 30 | 14 |

## Record format

```json
{
  "id": "covid:sum_e04fc7732f_163cc8406f",
  "type": "type-1",
  "topic": "COVID-19 pandemic",
  "topic_period": "2020-2023",
  "domain": "Health",
  "metric": "COVID-19 deaths",
  "metric_description": "COVID-19 deaths reported",
  "operation": "sum",
  "answer": 33.0,
  "answer_unit": null,
  "fact_languages": [
    "en",
    "ja"
  ],
  "questions": {
    "en": "During the COVID-19 pandemic, what is the sum of the new COVID-19 deaths reported that day in Wakayama Prefecture (on 2022-02-16) and the new confirmed COVID-19 deaths reported that day (excluding probable deaths) in Massachusetts (on 2021-04-03)?",
    "...": "six more languages"
  },
  "fact_order": {
    "en": [
      1,
      0
    ],
    "...": "six more languages"
  },
  "facts": [
    {
      "fact_id": "e04fc7732f",
      "language": "en",
      "country": "US",
      "entity": "Massachusetts",
      "entity_local": "Massachusetts",
      "period": "2021-04-03",
      "value": 30.0,
      "unit": "deaths",
      "question_value": 30.0,
      "question_unit": null,
      "rounding": null,
      "source_url": "https://fallriverreporter.com/massachusetts-covid-19-active-cases-and-hospitalizations-increase-again-as-daily-case-count-hits-2263/",
      "source_domain": "fallriverreporter.com"
    },
    {
      "...": "one record per supporting fact"
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `type` | `type-1`, `type-2`, or `type-3`, the number of non-English facts the question requires |
| `topic`, `topic_period` | Global topic and the period it covers |
| `domain`, `metric`, `metric_description` | Domain and metric that the facts report |
| `operation` | `sum`, or `max_minus_min`, the difference between the largest and the smallest fact value. With two facts this is the absolute difference |
| `answer`, `answer_unit` | Gold answer. `answer_unit` is given only when the question asks for a specific unit of the result |
| `fact_languages` | Languages in which the supporting facts are reported |
| `questions` | The question in each of the seven languages |
| `fact_order` | For each question language, the order in which that version of the question mentions the facts, as indices into `facts` |
| `facts[].entity`, `entity_local` | Place that the fact describes, in English and as written in the source language |
| `facts[].period` | Reference period of the value, as `YYYY`, `YYYY-MM`, `YYYY-Qn`, `YYYY-MM-DD`, or `start..end` |
| `facts[].value`, `unit` | Value that the question asks for and its unit as written in the source |
| `facts[].question_value`, `question_unit` | The same value expressed in the unit that the question asks for. The answer is computed from these |
| `facts[].rounding` | Present when the question asks for a rounded value. Holds the unrounded value, the rounding step, and the wording used in the question. Two questions may ask for the same fact at different precision |
| `facts[].source_url`, `source_domain` | Article that reports the fact |

## Usage

```python
import json

items = [json.loads(line) for line in open("data/crossbrowse.jsonl", encoding="utf-8")]
response_format = json.load(open("data/response_format.json", encoding="utf-8"))

item, lang = items[0], "es"
prompt = item["questions"][lang] + response_format["separator"][lang] + response_format["instruction"][lang]
facts_in_question_order = [item["facts"][i] for i in item["fact_order"][lang]]
```

The instruction asks the agent to list the value of every fact in the order the question mentions them and then give the final answer.
This allows each fact to be graded separately from the final answer.

```
python scripts/check_data.py
```

## Source material

This repository contains questions, answers, and fact records written for the benchmark.
It does not contain any article text.
Each fact links to the article that reports it, and the linked pages remain subject to the terms of their publishers.
