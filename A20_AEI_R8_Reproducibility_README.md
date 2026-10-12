# A20–AEI R8: executable operating contracts

Executable Operating Contracts Linking Anytime Localization to Engineering Task Evidence

This is a complete research revision, with original A19/A20 and the latest R4/R5 evidence retained separately. It contains actual computed simulation observations, fair procedural controls, source-history authorization, compiled manuscripts, editable figures, raw seeds and audit records. It does not add physical robot localization trials. Final independent AEI review is 8.2/10; mathematics 8.8/10 and statistics 8.5/10 are separate dimensions. The 9.0 revision target was not achieved. No Strong Accept outcome is asserted.

## Read first

- `main.pdf`: complete English AEI-oriented manuscript.
- `supplement.pdf`: independent supplementary material, full prospective tables and retained valid experiments.
- `REVISION_REPORT_CN.md`: six-defect evidence–change–verification report.
- `INDEPENDENT_REVIEW_CN.md`: three independent simulated reviews and remaining submission risks.
- `AUTHOR_DECLARATIONS.md`: actual author information still required for submission.
- `data/r8_final/protocol.json`: frozen population, methods, task requests and analysis protocol.
- `qa/r8/final_evidence_verification.json`: read-only audit of the delivered results.

## Independent inputs and paired executions

The R8 final study uses 13,824 disjoint episode seeds: 8,192 calibration, 4,096 confirmation and 1,536 unsupported stress. Forty-eight characterization/audit pilot inputs are excluded. Each source has one actual native ICP prefix, immutable scan/prior arrays and measured motion. The 22-policy × four-service comparisons are 1,216,512 paired controlled outcomes, not that many independent scans. The integrated confirmation driver actually performs 131,072 task/validator executions on the same 4,096 inputs; these add no independent sample size.

Thirty-six prescribed 600-s route inputs (three geometries × three conditions × four stochastic/design replicates) have 12 live method executions each: 432 runs, 72 simulated hours. Each geometry/condition is reported separately. The four replicates retain predeclared distinct noise/discrepancy settings and are descriptive rather than iid samples of one route population. Time samples and repeated policy runs are never counted as independent confirmation inputs.

The earlier 2,680-source, 81-route-execution R4 study and secondary R5 event-selection analysis are preserved with their original populations, seeds and confidence families. They are not pooled with R8. Four original physical-platform JPEGs and all five supplied simulation screenshots are kept unchanged. The photos show operating context, not new measured localization/latency evidence.

## Frozen chronology and limitations

F0: 2026-10-11 19:07:18.664676 UTC. Numerical models, code, maps, sensor/policy definitions, timing conventions and 528-member event family were sealed before final inputs existed.

A source-history claim observer was amended after F0 without changing the canonical numerical/event map. V1 and V2 are superseded and retained. V3: 19:46:40.196132 UTC. Independent audit checks 16,896 excluded-pilot paths and 5,632 first-calibration-chunk paths for projection equality. That audit emitted conformance counts/hashes, not policy rankings used to tune confirmation behavior.

F1: 19:59:17.439444 UTC. Calibration cards and all 96 request plans were sealed before confirmation/stress generation. The F1–V3 binder and preconfirmation inventory followed at 19:59:32 UTC. Local manifests establish consistency/chronology, not externally registered preregistration. The prospective study was designed after seeing the separately retained R4/R5 results.

Two predeclared geometry-confirmation JSONL records were absent even though their original NPZ files and successful collector log existed. The unchanged frozen collector regenerated only those original seeds (8,602,046/47). All 15 arrays and complete NPZ file hashes matched the preserved originals exactly. The recovery audit retains the original index, original files, cause uncertainty and repeated invocation. There was no excluded/replaced source, new independent observation or policy change.

The initial inventory gate used an incorrect singular route-file glob. Its actual executed source and record are preserved. The future gate was corrected to `*/inputs.npz`; the chronological execution ledger places all 36 route input generations after F1 and after the six confirmation/stress collectors. This orchestration correction does not alter F0/V3/F1 methods or outcomes.

## Data and code map

`source/r8_protocol.py`: predeclared populations and hypothesis family.
`r8_collect.py`, `r8_geometry.py`, `r4_sensor.py`: sensor raycasts, perturbations, procedural geometry and actual solver prefixes.
`r8_policy.py`: 22 matched policies, same forecast models/prices, time/profile guards and common budget enforcement.
`r8_service.py`: version publication, installation, causal replay, rollback and events.
`r8_contracts.py`: typed dependencies, independent procedural dispatch/checks, source identities and statement applicability.
`r8_claim_layer.py`: source-scoped monotone attachment history; separate from the frozen numerical execution.
`r8_confirmation_services.py`: independently executed Full/validated-procedural task services.
`r8_routes.py`, `r8_parallel_driver.py`: live full routes and resource-bounded orchestration.
`r8_audit_provider.py`: exact lazy-versus-hydrated route-input conformance; archive reading is offline.
`r8_audit_real_cards.py`: constructed malformed/stale/history cases using actual F1 cards; stripped variants are diagnostic ablations, not the main competitor.
`r8_analyze.py`: full original-denominator summaries, 16 prespecified paired-bootstrap intervals, tail/influence/Pareto analyses and certificate sensitivity.
`r8_figures_static.py`, `r8_figures_data.py`: data-based PDF/SVG/PNG/TIFF figures.
`r8_verify_release.py`: read-only final-data, frozen-code, CP, asset and route-metric verification.

`data/r8_final/episode_inputs/<seed>.npz` stores raw/processed scans, sensor time/ring, immutable priors and source posteriors, measured past/future motion increments and truth for offline scoring. `episodes.jsonl` stores native prefix records, feature traces, error arrays and each raw file hash. `results/<phase>/chunk_*.csv.gz` has paired controlled outcomes with decisions/installations/CPU/event traces and matching manifests. `integrated/<phase>/chunk_*.csv.gz` has actual source claims, timing and admission results. `routes/<geometry>_<condition>_<rep>/` stores shared inputs, all 12 live traces/captures, per-method journals and input manifests. `analysis/` contains complete derived tables. F0, V3, F1 and binding JSON files are immutable evidence records.

## Environment and provenance

Linux x86_64; AMD EPYC 9V74 virtualized host; effective CPU quota eight cores and memory quota eight GiB. Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, pandas 2.2.3, Matplotlib 3.10.8, scikit-learn 1.8.0. Numerical worker processes use `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`. Exact package/platform/hardware details are in `data/r8_final/environment.json`. Native BVH uses the retained C++ source compiled with g++; TeX Live/elsarticle and Poppler generate and inspect manuscripts. The provided native dependency must remain in the archive's ancestor layout.

B767/C172 models are pinned licensed FlightGear artifacts and retained prescribed paths; the new UnfittedAirframe is a code-defined procedural surface/ellipse. The raw sensor is synthetic rolling raycasting, motion is stochastic odometry, and processor contention is an exogenous modeled multiplier, not measured embedded hardware. Routes are prescribed rather than controller feedback. Exact artifacts, licenses, generators, perturbation distributions and hashes are retained.

The deterministic work clock uses excluded-pilot mean/median costs and counted operations. It is a modeled CPU-equivalent service clock, not WCET or physical real-time assurance. B is a registration-stage cap; common frontend, receiver replay and stream costs are included in total work and availability outside that cap. The controlled component CPU ledger charges actual native prefix/component costs. The inclusive replay ledger also contains offline assertion/scoring CPU and is separately labeled. Whole-route online CPU times actual frontend/ICP/features/forecast/dispatch/validation/replay/scheduling and excludes sensor generation, truth scoring, model/registry startup and archive decompression. Worker manifests separately record startup/offline archive CPU. A paired provider audit verifies numerical/clock/event invariance after moving lazy archive decompression outside this timer.

## Reproduce the delivered evidence

Extract all archive parts with their member paths unchanged. Work from `A20_release/output/A20_AEI_R8`. Install the versions in `requirements-R8.txt`; Python, g++, TeX Live and Poppler are required. The original native dependency is available in `A20_release/work/a19/RAS_A19`; `python3 source/bootstrap_release.py` restores it from the preserved archive if needed.

Run in order:

```bash
python3 source/r8_verify_release.py
python3 source/r8_analyze.py
python3 source/r8_figures_static.py
python3 source/r8_figures_data.py
python3 source/r8_results_author.py
python3 source/build_papers.py
python3 source/r8_visual_release_qa.py
```

The first command is read-only with respect to frozen evidence. The remaining commands regenerate derived tables, figures and manuscript text from all retained outcomes. CPU summary values use the archived measurements rather than pretending that a different host reproduces identical CPU. The final-data review reports are preserved; re-running analysis does not reselect F1.

To recompute controlled results from the delivered raw/native-prefix files in a separate extracted copy, archive/move its `data/r8_final/results` and `integrated` directories and invoke `r8_evaluate.py --phase <block>` for every frozen block, then `r8_confirmation_services.py`. New native validator/dispatch CPU measurements differ; deterministic work, numeric events and selection use the original sealed service profile and cards. To replay routes, move only the copied route method JSON/NPZ outputs while retaining `inputs.npz` and manifests, then run `r8_parallel_driver.py --routes --workers 4`. These are repeated executions of the same inputs, never new statistical evidence.

A genuinely new experiment requires a distinct copied study, freshly documented protocol/seed blocks, new pilot/service clock, F0, full independent calibration and F1 before any confirmation. Do not overwrite these final artifacts, refit on confirmation, transfer an old card after changing execution/population, or combine native CPU from different hosts/runs. Never rerun the one-time freeze/claim-verification scripts in the immutable delivered study, because those scripts create their original audit/freeze records.

## Evidence semantics

The exact one-sided Clopper–Pearson cards correct for K=528 at family confidence 0.95, assuming iid complete simulator inputs for each fixed population/service/policy/event. The seed-derived Random2or4 coin is included in the ideal independent pseudorandom-input model; fixed heterogeneous coin conditioning is not that binomial model. Dependence across paired policies/services/events is allowed by the union-bound proof. Trajectory/observation marginals and their directly calibrated union are distinct. Cards give unconditional episode-population risk, not scan-conditional confidence, a remaining-receipt-conditioned guarantee, subgroup/route/mission assurance or detection of physical distribution change.

Full and the primary task-aware calibrated validated procedural baseline share all predictors, cards, task/risk requirements, budgets, prices and history semantics. Numerical/authorization equivalence is retained as an informative result. The graph representation is evaluated for explicit dependencies, source/evidence lifecycle and auditability, without attributing a procedural-capable safety predicate exclusively to graph notation.

A refused request remains in the denominator and keeps the source prior. Unsupported stress/route populations carry no episode card. Route recommendations are explicitly provisional. Source-history refusal persists in the same trusted registry lifetime; restart requires restored history or withholding attachment. Serialized receipts are historical assessments; consumers must recheck current dependencies and source scope before using them after a change.

## Incoming baseline preservation

The incoming 25-page PDF, 18-page SI and original figure ZIP are byte-preserved in `preserved/latest_AEI_25p_baseline`. The 516,369,145-byte original source ZIP is stored as two unchanged byte segments to keep delivery groups small. After extracting all historical groups, `python3 source/r8_restore_original_baseline.py` reassembles and verifies its original SHA without modifying an existing original. `ORIGINAL_BASELINE_MANIFEST.json` records all input sizes/hashes and part hashes. Earlier archives, text snapshots and native dependencies are also retained.

## Publication state

The AEI official scope was checked against its engineering-knowledge requirement. Fifteen published primary works have verified publication/DOI metadata; ten mechanisms received accessible primary full-text reading and the remaining works were read through official previews/metadata, as itemized in `qa/r8_literature_verified.md`. Access to the full current ScienceDirect Guide for Authors returned 403, so no unverified journal-specific mandatory graphical-abstract/length rule is claimed.

No editor message or submission was made. Author COI, corresponding email, CRediT, approval and exclusivity require actual author facts. The declarations file makes these administrative requirements concrete without inventing responses. AI assistance and author responsibility are described in `AI_ASSISTANCE_RECORD.md`.
