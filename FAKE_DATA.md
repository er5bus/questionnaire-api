# Ergonomics

File path: /src/modules/stats/views/ergonomics_monitoring.py

details-of-troubles

```
fake_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
```

need-for-intervention

```
fake_data = {
20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
}

```

# HRD

need-for-intervention

```python
fake_kpis_data = {
20: {
      constants.PHYSIOTHERAPY: 20,
      constants.ERGONOMICS: 15,
      constants.MEDICINE: 10,
      constants.PSYCHOLOGY : 20,
      constants.COACH : 20,
      constants.NUTRITION: 20,
      constants.OSTEOPATHY: 20,
      constants.STOPP_WORKING : 20
    },
21: {
      constants.PHYSIOTHERAPY: 20,
      constants.ERGONOMICS: 15,
      constants.MEDICINE: 10,
      constants.PSYCHOLOGY : 20,
      constants.COACH : 20,
      constants.NUTRITION: 20,
      constants.OSTEOPATHY: 20,
      constants.STOPP_WORKING : 20
    }, 22: {
      constants.PHYSIOTHERAPY: 20,
      constants.ERGONOMICS: 15,
      constants.MEDICINE: 10,
      constants.PSYCHOLOGY : 20,
      constants.COACH : 20,
      constants.NUTRITION: 20,
      constants.OSTEOPATHY: 20,
      constants.STOPP_WORKING : 20
    }, 23: {
      constants.PHYSIOTHERAPY: 20,
      constants.ERGONOMICS: 15,
      constants.MEDICINE: 10,
      constants.PSYCHOLOGY : 20,
      constants.COACH : 20,
      constants.NUTRITION: 20,
      constants.OSTEOPATHY: 20,
      constants.STOPP_WORKING : 20
    }
}
fake_gpt_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
```

breakdown-of-failures

```python
fake_tms_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
fake_rps_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
fake_ergonomics_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
fake_nutrition_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
fake_physical_activity_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
```

# Nutrition

details-of-troubles

```
fake_answered_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
fake_others_data = { 20: 10, 21: 10, 22: 60, 23: 5 }

```

need-for-intervention

```python
fake_data = {
20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
}

```

# Pysical Activity

details-of-troubles

```python
fake_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
```

need-for-intervention

```
fake_data = {
20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
}

```


# RPS

details-of-troubles

```python
fake_data = { 20: 60, 21: 60, 22: 40, 23: 10 }
```

need-for-intervention

```python
fake_data = {
20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
}
```

# TMS

details-of-troubles

```python
fake_back_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
fake_upper_body_limbs_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
fake_lower_body_limbs_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
fake_headache_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
fake_abdominal_pains_data = { 20: 10, 21: 10, 22: 60, 23: 5 }
```

need-for-intervention

```python
fake_back_data = {
20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
}
fake_upper_body_limbs_data = {
20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
}
fake_lower_body_limbs_data = {
20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
}
fake_headache_data = {
20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
}
fake_abdominal_pains_data = {
20: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    21: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    22: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
    23: {tools.PREVENTIVE: 0, tools.MODERATE: 0, tools.IMPORTANT: 0, tools.URGENT: 0},
}

```
