# Revision plan — *Urban Transportation Economics Under Planetary Boundaries* (TRC-26-01219)

Inputs reviewed: submitted manuscript (`main.tex`, Draft 1), reviewer comments and the draft response letter (`Response_Letter.tex`), and the notebook in this repo. I independently reproduced the Sioux Falls baseline and tested several claims in the paper and letter. The scripts are in `revision/checks/` and the results are in §1.

---

## 0. Bottom line

1. **The draft response letter is mostly right in direction, but it promises results that haven't been computed, and some of its numbers and claims are wrong or contradict each other** (§2). Before it goes out, each blue "revised text" block needs a computed result behind it.
2. **The best way to strengthen the paper is to add, not just rename, on the viability point (R1.1).** The structural dynamics already in the paper give a *genuine* viability kernel for free. In one dimension it has a clean all-or-nothing result, and that result *is* the policy content of the "sign of the admissibility gap" proposition (§3, D1). This one move answers R1.1, R2.2, R2.5 and much of R2.6 together. It also makes the new proposition hard to call "trivial".
3. **The Sioux Falls story holds up when checked and gets sharper.** At s = 0 the minimum attainable emissions over *all* feasible flows is about 0.936·E0. So under Ē = 0.8E0 the admissible domain really is empty, and Proposition 2 really does apply. The marginal-emissions toll already gets most of that 6.4% routing headroom. Pricing "fails" because of the domain, not the instrument. This is a much stronger statement than the current "pricing reduces emissions <1%".
4. **Two findings in the current numerics must be fixed before any new numbers are reported:** (a) the convergence test can stop on a *negative* gap; (b) the accessibility loss under pricing is about 97–99% the toll payment itself, with no revenue recycling. The second point will be the first thing a careful referee raises in round 2.
5. **The code needs a rewrite before the new experiments.** The promised experiments are threshold sweeps, elastic demand, Latin-hypercube sensitivity and possibly a second network. They are not feasible with `iterrows` + networkx + loose convergence. The vectorised prototype in `revision/checks/model.py` already runs a 1,500-iteration UE in seconds.

---

## 1. What I verified (independent re-implementation, TNTP Sioux Falls data)

| Check | Result | Implication |
|---|---|---|
| Baseline E0 | 631.63 M vs paper's 631.77 M (0.02%) | Notebook model reproduced; the checks below are trustworthy. |
| Notebook stopping rule | Stops at iter 119 with "gap" = **−1.3e-4**; true multiclass gap = **1.1e-3** | The weighted-average-cost gap can go negative, and `gap < tol` then passes. The reported 1.663e-5 "convergence" is very likely spurious. |
| Convergence noise in emissions | Tightening to a true gap of 2.6e-5 changes E0 by **0.11%** | Same size as the PV-toll effect (0.6%, and non-monotone in μ in the notebook output) and as the margin by which s = 0.20 clears 0.8E0 (0.08%). Every small effect must be re-run at a tight gap. |
| Speed clip [10, 90] km/h | Binds on **4%** of links (3% of VKT); median raw speed 29 km/h; median v/c 1.58 | The clip is not doing the work, so the letter can say so. But the network is heavily over capacity (daily-scale demand against hourly-scale capacities). Avoid saying "tonnes per day" (see §2). |
| Monotonicity of xₐ·eₐ(xₐ) | Increasing on all 76 links over [0, 3·cap] | Because operation sits on the low-speed branch of the U-curve, the "non-monotone emissions" caveat matters less in practice than the text implies. Say so, and check convexity, which is what Prop. 1 needs. |
| **min over x∈F(q) of Φ(x)** at s=0 | **≈ 0.936·E0** (Frank–Wolfe with line search on the marginal-emissions cost, two starts: 0.9359 / 0.9377) | Ē = 0.8E0 ⇒ the domain is **empty at s=0** ⇒ Prop. 2 applies. **s_viab ≈ 0.145** (Ē=0.8E0), **≈ 0.391** (Ē=0.57E0). |
| Thresholds at Ē = 0.8E0 | s_viab ≈ 0.145 < s_UE ≈ 0.20 < s* = 0.229 | The equilibrium is admissible and self-sustaining. |
| Thresholds at Ē = 0.57E0 | s* ≈ 0.331 < s_viab ≈ 0.391 < s_UE ≈ 0.43 | The stationary state is not just equilibrium-inadmissible: **no allocation at all** is admissible there. This is stronger than the letter claims. |
| Contraction (from notebook scan, Ē=0.8E0) | H̃′ ∈ **[−1.96, −1.06]** ⇒ modulus ≤ **0.735** at λ=0.25 | The letter's placeholder "[−1.9, −1.2], ≤ 0.70" is wrong. Monotone (non-oscillating) convergence holds for λ < 0.51; divergence only for λ > ~1.02. |
| Accessibility loss under PV toll (peripheral) | μ=1.36e-4: −5.1% total, of which −0.1% is route/congestion; μ=2.51e-4: −9.2% vs −0.3%; μ=1e-2: −84.9% vs −3.4% | **The floor violation is almost entirely the toll payment entering Cᵢⱼ.** Without revenue recycling this is close to mechanical. It must be decomposed and reported with a recycling variant. |

Scripts: `check_baseline_and_gap.py`, `check_min_emissions.py`, `check_accessibility_decomposition.py`. My baseline A_P level (96.8k) differs from the paper's (107.3k) because I grouped nodes independently; the *relative* decomposition is the result that matters.

---

## 2. Problems in the current draft response letter (fix before sending)

**Internal contradictions**
- **Viability kernel.** The (commented) opening summary and the closing paragraph promise a "viability-theoretic reformulation" with a genuine kernel and capture basin. Protocol step 7 uses `Viab_f(S_adm)`. But the R1.1 response says the term is *removed* and nothing dynamic is defined. → Resolve with D1 (§3).
- **Two-link operator.** R1.4 and R2.4 say the ad hoc H = −0.5x₂ is *replaced* by the logistic map. The new §5.4 regime (ii) text still uses H = −0.5x₂ to derive ((2,8),1). → Pick one. Recommendation: keep −0.5x₂ for the closed-form VI solution (it's correct: λ_E = 1.8 checks out) and *add* a logistic-map variant so §5 and §6 share an operator class. Then say exactly that.
- **Proposition numbering** is inconsistent: "Proposition 3" (strong monotonicity), "Proposition 4" (sign of gap), and the earlier Props 1/3 demoted to Remarks. Fix the final numbering once (see §5).
- **Voice.** The letter mixes "I" and "we" (single-author paper). Pick one.

**Mathematical issues**
- **Sign convention of the structural block.** In §4–5 (two-link) a *negative* H pushes s *up* (⟨H, r−s⟩ ≥ 0 ⇒ s* = 1). In §6, H = ŝ − s is *positive* when s should rise, and the discrete map is s + λH. These are opposite conventions. In the VI the structural operator must be F_s = s − ŝ(x,s) = −H. This changes the monotonicity condition: Ĥ = ŝ − s is *decreasing*, so condition (ii) of the new strong-monotonicity proposition fails as written.
- **Strong-monotonicity proposition doesn't cover the paper's own application:**
  - (ii) requires H(s,x) = Ĥ(s), but §6's H depends on x through E(x,s). Generalise: let F_s be Lipschitz in x with constant L_H. The cross terms then give (L_C + L_H)² < 4αβ, or the asymmetric version.
  - (i) requires α > 0 strong monotonicity of C in x. That fails for (a) the raw multiclass operator (the letter itself notes the indefinite symmetric part) and (b) BPR-type tₐ = a₀ + a₄x⁴, which has t′(0) = 0. State it on *aggregate* link flow after VOT rescaling, on a compact set bounded away from zero flow, or use strict monotonicity plus compactness. Also say uniqueness is in (aggregate x, s), not in class flows.
- **Contraction numbers:** replace with [−1.96, −1.06] and ≤ 0.735 (recompute at the new reference ceiling). Fix "would oscillate or diverge for λ > 1": oscillation begins at λ ≈ 0.51 and divergence at λ ≈ 1.02.
- **Pricing claim "emissions fall by less than one per cent"** is true for the PV toll only. The ME toll gives 5.1%. Report both against the min-Φ benchmark (6.4%).
- **"s* > s_adm ⇔ ψ(0) > s_adm" proposition** is correct but is a two-line consequence of definitions. Reviewer 2's exact complaint will apply again unless it is embedded in the dynamic/viability result (D1) and given the cost-of-sustaining corollary.

**Claims stated as results before being computed** (flagged `% VERIFY` or `[·]`, but some are unflagged):
- Elastic demand: "pricing violates the peripheral floor before reaching the ceiling", "rebound raises s_adm above 1 − Ē/E0", "materially larger reduction". These are predictions. Write the response only after running them, and be ready for them to come out differently.
- Absolute (sufficientarian) floor results, LHS sensitivity outcomes, Table 6.

**Grounding of the ceiling (R1.5)**
- "E0 ≈ 632 t CO₂ per modelled day ≈ 231 kt/yr": Sioux Falls OD totals combined with hourly-scale capacities give median v/c ≈ 1.6. The "day" is not a defensible period, so drop the annualisation. Say "per modelled period" and let the ceiling be a *ratio* to E0, which is all the analysis needs.
- "IPCC AR6: −43% by 2030" is the *all-GHG, economy-wide* figure (CO₂ is about −48%). Applying it to one sector on one network from a non-2019 baseline is a stretch a referee will notice. Better: present Ē/E0 as a policy parameter, anchor a *range* with 2–3 sources (economy-wide 1.5°C, transport-sector pathways from AR6 WGIII Ch.10 or IEA, an equal-per-capita downscaled budget), and make the sweep the result. Optionally add a **cumulative-budget** variant tied to the steering problem (∫E(s(t))dt ≤ B), which is the planetary-boundary-faithful form of a carbon budget. *Verify all cited figures before use.*

---

## 3. Strategic decisions (my recommendation first)

**D1. Viability: rename and add a genuine kernel (recommended), rather than rename only.**
- Rename Eq. (17) → admissible structural set 𝒮_adm (static), as the letter does.
- Add a short subsection using the dynamics already in §4.6 / §6.4. Controlled adjustment: ṡ = λH̃(s) + u, u ∈ [0, u_max]. Constraint set K_UE = [s_UE, 1] (or 𝒮_adm). Define Viab(K) and the capture basin.
- **Result (1-D, H̃ decreasing):** Viab(K) = K if λ(ψ(0) − s_UE) + u_max ≥ 0; otherwise Viab(K) = ∅. *All-or-nothing.* The only exit point is the lower boundary, and if the field points outward there, every trajectory from inside converges to a root below it.
  - Corollary 1: with u = 0, the admissible set is self-sustaining iff ψ(0) ≥ s_UE. This is exactly the letter's "sign of the gap" proposition, now with dynamic content.
  - Corollary 2: the minimal *sustaining* control is u_hold = λ(s_UE − ψ(0))⁺. The steady-state cost of holding admissibility is ∝ the admissibility gap and **independent of G_E**. This gives the "move the intercept, not the feedback" policy reading a quantitative cost.
  - Corollary 3: the steering problem (Eq. 26) gets a terminal *viability* condition, not just s(T) ∈ 𝒮_adm. Redo the §5.5 example with drift. After T a holding cost remains whenever s* < s_target.
- Benefit: turns R1.1 from a concession into a contribution and supplies R2.2's "new and unique" result. Gives R2.5 its policy implication and R2.6's protocol a well-defined step 7. It costs about 1–1.5 pages.
- Multi-dimensional s: state the general definition, then note that the 1-D all-or-nothing property does not carry over. Cite Aubin (1991), Aubin–Bayen–Saint-Pierre (2011), Saint-Pierre (1994) for computation.

**D2. Make the Sioux Falls implementation match the stated model.** The paper uses 2 classes with fleet-average cost c̄(s). The code uses **4 subclasses** (P/C × ICE/EV) with **s-dependent demand split**, so s enters the *feasible set*, not the cost.
- *Recommended:* keep the 4-subclass implementation (more realistic) and rewrite §6.2–6.3 to match. The flow block is then a VI on F(q(s)), a *quasi*-VI in (x,s). Note this, and state that for fixed s it is a standard multiclass VI. Under VOT rescaling it is equivalent to a convex programme in aggregate flow (classes differ by constant per-km terms). That is what makes x(s) single-valued and H̃ well defined. Coupling constant L then comes via the demand split, and should be derived accordingly.
- *Alternative:* recode to the paper's fleet-average formulation. This is simpler for the theory but less defensible behaviourally (EV and ICE users would face the same cost).
- Also align the **assignment classes with the accessibility groups.** Currently the "peripheral/low-income" VOT class is 50% of *every* OD pair, while peripheral accessibility is measured from peripheral *origin nodes*. Assign class shares by origin zone, e.g. peripheral origins mostly class P, or say explicitly that VOT class and location are independent.

**D3. Elastic demand (R1.6, R2.3): do it, but scope it tightly.**
- Single-level formulation via Gartner's excess-demand transformation or a direct VI with inverse demand Dᵢⱼ⁻¹. Use exponential or constant-elasticity demand calibrated so that q(c₀) = q₀ and the elasticity is a sensitivity parameter (e.g. −0.1 to −0.5).
- With elastic demand, switch or add a **logsum-consistent accessibility / consumer-surplus** measure. That removes the "83% accessibility loss with unchanged trips" inconsistency at the root.
- Report the PV and ME tolls **with and without revenue recycling** (lump-sum per traveller by group, or to a transit/EV subsidy), plus the decomposition from §1. Expect the "floor before ceiling" result to depend on recycling. That dependence is itself a finding worth reporting.

**D4. Empirical grounding (R2.3): go beyond "out of scope". Recommended middle path:**
- (a) Replace ad hoc parameters with sourced ones: COPERT or MOVES speed–CO₂ curves for a petrol Euro-6 car, observed op-cost ratios, VOT from national guidelines, and a G₀ chosen so σ(G₀) equals an observed new-sales or fleet EV share. Cite each source in Table 1.
- (b) **Add a second network with real link lengths**, e.g. Anaheim or Chicago-Sketch from TNTP, or a Sydney/Melbourne strategic network if available to you. This removes the pseudo-length criticism (R1.6) and gives "multiple case studies" (R2.3) at modest cost once the code is vectorised.
- Keep the honest framing paragraph at the head of §6 ("what this application can and cannot establish") — it's good.

**D5. Length.** The additions are substantial: viability subsection, 3–4 new results, positioning table, H-specification table, thresholds, sensitivity, elastic demand, protocol. Compensate by tightening §2–3 (the literature review is long and no reviewer asked for it), moving proofs and the functional-form figure to an appendix, and moving full sensitivity tables to supplementary material.

---

## 4. Comment-by-comment plan

Legend: **P** = paper change, **C** = code/computation, **L** = letter change. Effort: S/M/L.
Citations suggested below are from memory. Check each one (authors, year, venue) before adding it to `cas-refs.bib`.

### Reviewer 1

**R1.1 — "viability kernel" is not a viability kernel.** Draft: rename only. Plan: D1.
- P: rename to 𝒮_adm throughout (abstract, intro para 9, §4.3 heading, §4.4 closing, §4.5 steering, §5.3, §7). Add §4.x "Admissible dynamics and the viability kernel" with the all-or-nothing proposition and corollaries. Revise §5.5 steering with drift.
- C: compute Viab and u_hold for Sioux Falls at both ceilings (cheap: H̃ is already scanned).
- L: rewrite the response as "renamed **and** reformulated", and make the summary paragraph and closing consistent. **M**

**R1.2 — behavioural interpretation and enforcement of the joint VI.** Draft response is strong; keep the new §4.5.1.
- P: in the side-constrained reading, be explicit that the multiplier-augmented Wardrop equivalence needs the *flow* block to be a convex programme. That is true after VOT rescaling with constant op-cost terms, but **not** with flow-dependent tolls divided by class VOT. Note the asymmetry under pricing.
- P: say who sets Ē (a regulator or cap authority). Under the credit-market reading, credits are per veh-km × e(v), so implementation needs speed-dependent metering; note this as a practical caveat.
- C: show the side-constrained equilibrium *numerically* on Sioux Falls for one case where the ceiling binds and K ≠ ∅. Example: Ē = 0.8E0 at s ∈ [0.145, 0.20], where pricing *can* reach admissibility. Report λ_E (= the required credit price) as a function of s. This is the empirical counterpart of regime 2 and closes R1.4's "ceiling binds" promise. **M**

**R1.3 — formal results standard or wrong.**
- P: demote Props 1 and 3 to Remarks (agree). Fix the strong-monotonicity proposition per §2 (sign, x-dependence of H, aggregate-flow α, BPR at zero flow). Replace the global-stability claim with the contraction condition using correct numbers.
- P: consider citing day-to-day / projected-dynamical-system stability results (Smith 1984; Nagurney & Zhang 1996; Yang & Zhang 2009) for the discrete scheme.
- C: compute H̃′ by finite differences on a fine grid at each reported Ē, with tight UE convergence. **S–M**

**R1.4 — theory/numerics alignment; two-link example not stationary.**
- P: equivalence lemma (keep). Add the D2 rewrite of §6.2–6.3. Two-link: keep ((2,8),1) with λ_E = 1.8 (verified) and add the logistic-map variant.
- C: **fix the gap measure** (subclass-specific: Σ_k c^k·(x^k − y^k) / Σ_k c^k·x^k, which is ≥ 0). Store 4 subclass flows. Use a line search on the VOT-rescaled potential (now valid) or a path/bush-based algorithm. Target relative gap ≤ 1e-6 for any effect < 1%. Correct "MSA" → FW with predetermined steps (or the new algorithm). Report the gap for every reported equilibrium.
- C: compute s_adm by **bisection** (not on a 0.05 grid; the true value at 0.8E0 is about 0.199). **M**

**R1.5 — ceilings and floors not grounded.**
- P: ceiling per §2 (ratio framing, range of anchors, sweep, optional cumulative budget). Floors: keep the non-degradation vs sufficientarian framing (good). Note that with only 6 nodes per group, results are sensitive to group definition, and add a group-definition sensitivity check.
- C: sweep Ē/E0 ∈ [0.5, 0.95] for s_viab, s_UE, s*, the gap, Viab and u_hold; absolute-floor variant. **M**

**R1.6 — Sioux Falls limitations; pricing claim overstated.** This is the most important comment, and the draft response is the right one.
- P: narrow the claim (agree). Add the **min-Φ benchmark** to Fig. 1(e). The headline becomes: at s=0 even the emissions-minimising allocation is 6.4% below E0, so no instrument acting on routes can get near 0.8E0. The ME toll achieves about 80% of that headroom. That turns "pricing is weak" into "the domain is empty", which is the paper's own thesis.
- P: accessibility decomposition (payment vs network effect), with and without revenue recycling. Elastic demand per D3.
- C: OAT + LHS sensitivity (parameters as listed in the letter, plus class shares, group definition, recycling rule). Report the robustness of the *ordering* of thresholds and of the sign of the gap rather than point values. Use PRCC or Sobol' indices if time permits. **L**

### Reviewer 2

**R2.1 — what is fundamentally new?** Draft response and positioning table are good.
- P: tighten the three novelty claims. Add citations for the "coupled adoption–network models" row (e.g. EV/BEV network equilibrium: Jiang et al.; He, Yin & Lawphongpanich; Xu et al.) and for co-evolution / network growth (Yerra & Levinson; Levinson & Xie). With D1, add a fourth claim: the dynamic admissibility (viability) characterisation and the cost of sustaining admissibility. **S**

**R2.2 — propositions follow from definitions.**
- P: the substantive new results should be (i) the viability all-or-nothing proposition with its holding-cost corollary (D1); (ii) the threshold ordering s_viab ≤ s_UE and the regime classification, with a *formal* statement of when s* falls into each regime; (iii) the corrected coupling condition for uniqueness; (iv) the multiclass rescaling lemma.
- P: optionally add comparative statics of the thresholds in Ē. Since E(x(s),s) = (1−s)Φ(x(s)), ds_UE/dĒ ≈ −1/Φ and ds*/dĒ = −G_E σ′/(…) can be derived. This gives the switch ceiling Ē† = (1 − σ(G₀))·Φ in closed form, plus a statement about how it moves with demand elasticity (rebound). **M**

**R2.3 — usefulness / realism.** D4 plus the elastic-demand and sensitivity work. Reword the letter from "not able to complete" to what has actually been done (sourced parameters, second network). **L**

**R2.4 — H generic.** New §4.5.2 and Table 3 are good.
- P: add the regularity checklist tied to the corrected results (continuity → existence; coupling condition → uniqueness; −2/λ < H̃′ < 0 → stability; boundary inward-pointing → viability). Show *in the case study* that the logistic H passes each check numerically. Add a short "how to estimate G₀, G_E" paragraph: G₀ from the observed adoption level; G_E from the response of adoption to an emissions-gap proxy (e.g. policy-stringency indices) in panel data. **S**

**R2.5 — Prop. 2 trivial; policy implications.** Three thresholds plus four regimes — the response is good.
- P/C: now computable (see §1). Report a Table 6 at both ceilings with gaps, using bisection for s_UE and min-Φ for s_viab, including the nonconvexity caveat and multi-start evidence. Add a 1-D "regime map" figure: x-axis s, coloured regime bands, markers s*, s_viab, s_UE, as Ē varies (a 2-D heat map over (s, Ē/E0) works well). **M**

**R2.6 — practitioner use.** Protocol in §7.1 is good.
- P: make step 7 refer to the viability result (D1). Add a flowchart figure. Add a worked "protocol applied" box using the Sioux Falls numbers (each step → number → decision). Give the computational cost in assignments: about 1 + (bisection ≈ 10) + (min-Φ ≈ 1 multi-start) + (H̃ scan ≈ 20). **S–M**

### Unrequested corrections (keep the letter's list, with additions)
- Algorithm naming; proper multiclass gap (**plus the negative-gap stopping bug**); units; clip frequency (4% of links); accessibility under pricing (**plus the payment-vs-network decomposition**); replication.
- Add: the s_adm grid-resolution issue (0.20 → bisection ≈ 0.199); the 2-class vs 4-subclass description mismatch; the sign convention of H; Fig. 1 caption still says "model units"; the abstract claim "structural change may enable feasibility in principle, but equilibrium outcomes can remain inadmissible without adjustments to behavioural incentives" needs rewriting around the new findings.

---

## 5. Proposed structure and numbering of results in the revised paper

- §1 Intro: trim; restate contributions as 4 bullets.
- §2–3: compress by about 30–40%.
- §4.1 Preliminaries; Remark 1 (dual equivalence, was Prop. 1).
- §4.2 Structural infeasibility; **Prop. 1** (was Prop. 2).
- §4.3 Structural states and the admissible structural set 𝒮_adm; Lemma 1 (closedness).
- §4.4 Joint flow–structure VI; Remark 2 (existence, was Prop. 3); **Prop. 2** (coupling condition, corrected); **Lemma 2** (equivalence under inactive constraints); **Lemma 3** (multiclass VOT rescaling).
  - §4.4.1 Enforcement and behavioural interpretation (side-constrained, credits).
  - §4.4.2 Specifying and estimating H (Table 3 + regularity checklist).
- §4.5 **Thresholds and regimes** (s_viab ≤ s_UE, s*), **Prop. 3** (sign of the gap).
- §4.6 **Admissible dynamics and the viability kernel**: **Prop. 4** (all-or-nothing), Cor. (holding cost); steering problem with viability terminal condition.
- §4.7 Positioning (Table 2).
- §5 Two-link examples (with VI solution ((2,8),1), λ_E, logistic variant, steering with drift).
- §6 Applications: 6.1 scope statement; 6.2 data and specification (sourced parameters, D2 alignment); 6.3 algorithm and convergence; 6.4 thresholds and regimes vs Ē; 6.5 dynamics, viability and holding cost; 6.6 floors (non-degradation vs sufficientarian); 6.7 pricing (fixed vs elastic demand, recycling, decomposition, λ_E); 6.8 second network; 6.9 sensitivity.
- §7 Discussion: 7.1 implementation protocol (+ flowchart, worked box); 7.2 limitations; 7.3 future work (calibration data needs, multi-dimensional 𝒮_adm and viability computation).
- Appendix: proofs, functional forms, algorithm details. Supplement: full sensitivity tables.

---

## 6. Work packages and order

Critical path: **WP1 → WP2 → (WP3, WP4, WP5 in parallel) → WP6 → WP7.** Don't finalise any blue text in the letter until WP2–WP5 numbers exist.

| WP | Content | Depends on | Size |
|---|---|---|---|
| **WP0** | Decide D1–D5 (the questions in §7 below) | — | — |
| **WP1 Code foundation** | Package `jfse/`: vectorised FW / bush-based UE with 4 subclasses, correct gap, VOT-rescaled line search, elastic-demand option, toll + recycling options, min-Φ solver (multi-start), bisection thresholds, H̃ scan and contraction check, viability/holding-cost calc; data included; `requirements.txt`; config file per reported table; tests (two-link closed form; reproduce E0) | — | L |
| **WP2 Re-baseline** | Re-run all §6 numbers at tight gap; s_UE by bisection; s_viab via min-Φ; contraction numbers | WP1 | S |
| **WP3 Ceiling sweep and regimes** | Ē/E0 ∈ [0.5, 0.95]: s_viab, s_UE, s*, gap, Viab, u_hold; regime-map figure; Table 6 | WP2 | M |
| **WP4 Pricing redo** | Fixed demand: PV/ME vs min-Φ benchmark, accessibility decomposition, recycling; λ_E (side-constrained) for s ∈ [s_viab, s_UE]; elastic demand variant | WP1 | M–L |
| **WP5 Sensitivity and second network** | OAT + LHS; group-definition check; sourced-parameter set; Anaheim or Chicago-Sketch run | WP1 | L |
| **WP6 Theory write-up** | Corrected Prop. 2; Lemmas 2–3; Prop. 3; viability Prop. 4 + corollaries; two-link updates; sign-convention fix | can start now, in parallel with WP1 | M |
| **WP7 Paper and letter** | Restructure per §5; rewrite abstract and highlights; figures; finalise letter with actual numbers; latexdiff for the editor | all | M |

---

## 7. Decisions I need from you

1. **D1:** add a genuine viability kernel (recommended) or rename only?
2. **D2:** describe the 4-subclass model the code uses (recommended), or recode to the paper's 2-class fleet-average model?
3. **D3:** elastic demand in this round (recommended, since the letter already promises it), and which revenue-recycling rule(s) to report?
4. **D4:** second network? If so, a TNTP network with real lengths (Anaheim / Chicago-Sketch), or do you have a Sydney/Melbourne network you can use?
5. **Ceiling anchor:** happy to present Ē/E0 as a policy parameter with a sourced range rather than a single "IPCC-consistent" 0.57?
6. **Code:** shall I start WP1 (refactor into a tested package under this repo) next?
