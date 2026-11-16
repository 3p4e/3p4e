# LTX-2.5 Frame Contract — SETTLED

## Rule
LTX-2.5 requires **frames = 8n + 1**.

| Candidate | 8n+1? | (f-1)%8 | Duration @24fps | 18-shot total |
|-----------|-------|---------|-----------------|---------------|
| 80 (old)  | ❌ FAIL | 7 | 3.333s | 60.00s — **INVALID** |
| **81 (FINAL)** | ✅ | 0 | **3.375s** | **60.75s** |
| 97 | ✅ | 0 | 4.042s | 72.75s |
| 121 | ✅ | 0 | 5.042s | 90.75s |
| 48 CU (old) | ❌ FAIL | 7 | 2.000s | — |
| **49 CU (FINAL)** | ✅ | 0 | **2.042s** | — |

## Authoritative cut: ~60s Sunder
- **Main shots s01–s18:** `frames = 81`
- **CU inserts sCU1–3:** `frames = 49`
- **Total main timeline:** 18 × 81 = **1458 frames = 60.75 s** @ 24 fps
- Jobfile: `p23_sunder_ltx25.json` / `.jsonl`

## Optional cinematic alternate
- **Main:** `frames = 121` → 90.75 s
- Jobfile: `p23_sunder_ltx25_121f_90s.json`

## Why not 80
`(80 - 1) % 8 = 7` — fails native LTX grid. Bump **80 → 81** (+0.75 s total over pure 60s).
