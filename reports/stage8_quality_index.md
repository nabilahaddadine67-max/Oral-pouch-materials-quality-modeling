# Stage 8 — Pouch Quality Prediction Score: method and strict evidence boundaries

## Objective and status

This is an **exploratory proposed decision-support index**, not a validated overall pouch-quality metric, an optimized pouch formula, or a regulatory/safety assessment. Only published flavor-marker retention observations support a computed **partial** score for matched conditions. The six-domain total is **illustrated using fictional desirabilities only**.

## Proposed mathematical framework

For domains \(i = 1,\ldots,6\), normalized desirabilities \(0 \leq d_i \leq 1\) and weights \(w_i \geq 0\) summing to one:

\[
PQPS = 100 \exp\left(\sum_{i=1}^{6} w_i \ln d_i\right).
\]

Any positively weighted zero desirability yields zero. **If a domain is unmeasured, return missing (NA), not zero, not 100, and not a renormalized total score.** Domains and preliminary, *subjective* weights are moisture (0.25); physical properties (0.20); release consistency (0.20); flavor retention (0.15); chemical stability (0.10); storage robustness (0.10). No weights or specifications have been validated against an external quality endpoint.

A target-based transformation for an attribute with an independently justified setpoint \(T\) and tolerance parameter \(s\) may be proposed as \(d(x)=\exp[-((x-T)/s)^2]\), **but neither \(T\) nor \(s\) is established by the current published dataset**. A release *target* must be defined independently; maximizing speed is not synonymous with improving quality. Multiple correlated metrics within a domain (e.g., bulk density / porosity) should not be double-counted.

## A real measured partial score, not an overall product score

US11844368B2 Tables 3b and 4b report limonene and linalyl acetate retention percentages for the *same* five matrix conditions at 3 weeks (30 °C; 75% RH). A limited **two-marker flavor-retention subscore** is computed as:

\[
S_{F,2} = 100\sqrt{(R_{limonene}/100)(R_{linalyl\ acetate}/100)}
          =\sqrt{R_{limonene}\,R_{linalyl\ acetate}}.
\]

A 100-point subscore indicates both selected markers fully retained relative to their own baseline; it does *not* capture other flavors, sensory perception, microbiological safety, seal integrity, or nicotine performance. The published concentrations are means; replicate data and measurement variances are not available. **Matrix fat content and water content vary together**, so differences are not attributable to fat alone. For each of these five conditions five of the six overall domains are missing, therefore no complete PQPS is calculated.

See `data/stage8_measured_flavor_partial_scores.csv` and `figures/stage8_measured_flavor_partial_scores.png`.

## Hypothetical six-domain demonstration

`data/stage8_hypothetical_scenarios.csv` contains three expressly **SYNTHETIC** profiles. Scores are arithmetic demonstrations, never measurements or predictions for a named product. The sensitivity simulation draws 5,000 weight vectors from a Dirichlet distribution with concentration \(40w\) and fixed seed 20261122; its 5–95% bands reflect **only arbitrary weighting sensitivity**, not sampling uncertainty, model validation or confidence intervals. A scenario ranking is conditional on weights and on imaginary desirability inputs; it is not a best pouch.

## Data source provenance and boundaries

- Source: [US11844368B2](https://patents.justia.com/patent/11844368), Tables 3a–4b, secondary transcription in `data/stage7_patent_flavor_retention.csv`; patent applicant-reported experiment, not independent lab validation.
- Original project: [Scientific Reports pouch materials](https://doi.org/10.1038/s41598-025-34556-5), [formulation patent](https://patents.google.com/patent/US20260232007A1/en), [binder patent](https://patents.google.com/patent/US20250072472A1/en). These are **different, unmatched experiments** and must not be row-joined into an artificial formulation-wide quality label.
- `data/stage7_patent_seal_strength.csv` references different matrix formulations and conditions; it is **not** merged with the flavor-retention data.
- Separate sources include [2025 flavor aging in e-liquids](https://doi.org/10.1021/acsomega.5c01266), which is not directly applicable as pouch-retention measurement.

## What would permit validation?

A properly designed and repeated study should jointly quantify, **on the same experimental formulations**, the six attributes with preregistered objective specifications, measurement uncertainty, and a genuinely independent reference for performance or quality. Sensitivity to weights, test medium, temperature, RH, and ingredient co-variation must be quantified before ranking commercial materials. Missing responses must be measured before full PQPS is reported.

## Reproduce

```bash
python scripts/stage8_quality_score.py
python -m unittest discover -s tests
```

Publication claim: **a reproducible, explicit scoring proposal with a measured flavor-only subscore and simulated weight sensitivity; NOT experimentally validated optimum formulation**.
