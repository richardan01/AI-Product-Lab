# RegEval experiment 2026-06-24-01 — rubric-graded-v4

**Verdict:** DISCARD
**κ:** 0.570 (95% CI [0.434, 0.697])  vs champion 0.820  Δ=-0.250
**Diagnostics:** TPR=0.690 · TNR=0.975 · abst=0.160 · N=100
**Harness:** subagent-harness (batched, comparable-with-caveat)
**Parent:** current

## Result narrative
73/100 correct. Per-class κ: compliant=0.640 · non-compliant=0.741 · unclear=0.150.
Mismatches: reg-0005, reg-0007, reg-0009, reg-0010, reg-0022, reg-0023, reg-0024, reg-0025, reg-0026, reg-0028, reg-0029, reg-0037, reg-0039, reg-0054, reg-0059, reg-0062, reg-0064, reg-0074, reg-0075, reg-0079, 


## Per-item
| id | gold | judge | match |
|---|---|---|---|
| reg-0001 | compliant | compliant | ✓ |
| reg-0002 | compliant | compliant | ✓ |
| reg-0003 | compliant | compliant | ✓ |
| reg-0004 | compliant | compliant | ✓ |
| reg-0005 | compliant | non-compliant | ✗ |
| reg-0006 | compliant | compliant | ✓ |
| reg-0007 | compliant | unclear | ✗ |
| reg-0008 | compliant | compliant | ✓ |
| reg-0009 | compliant | non-compliant | ✗ |
| reg-0010 | compliant | unclear | ✗ |
| reg-0011 | non-compliant | non-compliant | ✓ |
| reg-0012 | non-compliant | non-compliant | ✓ |
| reg-0013 | non-compliant | non-compliant | ✓ |
| reg-0014 | non-compliant | non-compliant | ✓ |
| reg-0015 | non-compliant | non-compliant | ✓ |
| reg-0016 | non-compliant | non-compliant | ✓ |
| reg-0017 | non-compliant | non-compliant | ✓ |
| reg-0018 | non-compliant | non-compliant | ✓ |
| reg-0019 | non-compliant | non-compliant | ✓ |
| reg-0020 | non-compliant | non-compliant | ✓ |
| reg-0021 | compliant | compliant | ✓ |
| reg-0022 | unclear | compliant | ✗ |
| reg-0023 | compliant | non-compliant | ✗ |
| reg-0024 | unclear | compliant | ✗ |
| reg-0025 | unclear | non-compliant | ✗ |
| reg-0026 | unclear | non-compliant | ✗ |
| reg-0027 | unclear | unclear | ✓ |
| reg-0028 | unclear | compliant | ✗ |
| reg-0029 | unclear | non-compliant | ✗ |
| reg-0030 | unclear | unclear | ✓ |
| reg-0031 | compliant | compliant | ✓ |
| reg-0032 | compliant | compliant | ✓ |
| reg-0033 | compliant | compliant | ✓ |
| reg-0034 | compliant | compliant | ✓ |
| reg-0035 | compliant | compliant | ✓ |
| reg-0036 | compliant | compliant | ✓ |
| reg-0037 | compliant | unclear | ✗ |
| reg-0038 | compliant | compliant | ✓ |
| reg-0039 | compliant | unclear | ✗ |
| reg-0040 | compliant | compliant | ✓ |
| reg-0041 | non-compliant | non-compliant | ✓ |
| reg-0042 | non-compliant | non-compliant | ✓ |
| reg-0043 | non-compliant | non-compliant | ✓ |
| reg-0044 | non-compliant | non-compliant | ✓ |
| reg-0045 | non-compliant | non-compliant | ✓ |
| reg-0046 | non-compliant | non-compliant | ✓ |
| reg-0047 | non-compliant | non-compliant | ✓ |
| reg-0048 | non-compliant | non-compliant | ✓ |
| reg-0049 | non-compliant | non-compliant | ✓ |
| reg-0050 | non-compliant | non-compliant | ✓ |
| reg-0051 | non-compliant | non-compliant | ✓ |
| reg-0052 | non-compliant | non-compliant | ✓ |
| reg-0053 | non-compliant | non-compliant | ✓ |
| reg-0054 | compliant | unclear | ✗ |
| reg-0055 | compliant | compliant | ✓ |
| reg-0056 | compliant | compliant | ✓ |
| reg-0057 | compliant | compliant | ✓ |
| reg-0058 | compliant | compliant | ✓ |
| reg-0059 | compliant | unclear | ✗ |
| reg-0060 | compliant | compliant | ✓ |
| reg-0061 | compliant | compliant | ✓ |
| reg-0062 | compliant | unclear | ✗ |
| reg-0063 | compliant | compliant | ✓ |
| reg-0064 | compliant | unclear | ✗ |
| reg-0065 | compliant | compliant | ✓ |
| reg-0066 | non-compliant | non-compliant | ✓ |
| reg-0067 | non-compliant | non-compliant | ✓ |
| reg-0068 | non-compliant | non-compliant | ✓ |
| reg-0069 | non-compliant | non-compliant | ✓ |
| reg-0070 | non-compliant | non-compliant | ✓ |
| reg-0071 | non-compliant | non-compliant | ✓ |
| reg-0072 | non-compliant | non-compliant | ✓ |
| reg-0073 | non-compliant | non-compliant | ✓ |
| reg-0074 | unclear | compliant | ✗ |
| reg-0075 | unclear | non-compliant | ✗ |
| reg-0076 | unclear | unclear | ✓ |
| reg-0077 | unclear | unclear | ✓ |
| reg-0078 | unclear | unclear | ✓ |
| reg-0079 | unclear | non-compliant | ✗ |
| reg-0080 | unclear | non-compliant | ✗ |
| reg-0081 | unclear | non-compliant | ✗ |
| reg-0082 | compliant | compliant | ✓ |
| reg-0083 | compliant | unclear | ✗ |
| reg-0084 | compliant | compliant | ✓ |
| reg-0085 | compliant | compliant | ✓ |
| reg-0086 | compliant | unclear | ✗ |
| reg-0087 | compliant | compliant | ✓ |
| reg-0088 | non-compliant | non-compliant | ✓ |
| reg-0089 | non-compliant | non-compliant | ✓ |
| reg-0090 | non-compliant | non-compliant | ✓ |
| reg-0091 | non-compliant | non-compliant | ✓ |
| reg-0092 | non-compliant | non-compliant | ✓ |
| reg-0093 | non-compliant | non-compliant | ✓ |
| reg-0094 | non-compliant | non-compliant | ✓ |
| reg-0095 | non-compliant | unclear | ✗ |
| reg-0096 | non-compliant | non-compliant | ✓ |
| reg-0097 | unclear | non-compliant | ✗ |
| reg-0098 | compliant | compliant | ✓ |
| reg-0099 | compliant | compliant | ✓ |
| reg-0100 | unclear | non-compliant | ✗ |
