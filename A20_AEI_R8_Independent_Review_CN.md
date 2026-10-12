# A20–AEI R8 独立模拟审稿报告

**最终AEI综合评价8.2/10；不支持9.0或Strong Accept结论。** 三轮分别由数学/算法、AEI领域和统计审查助手进行只读审查及独立复算。以下为作者修订过程中的模拟同行评审，不是AEI编辑或实际受邀审稿人的意见。原始完整报告及缺陷—证据—修订—复核记录作为附录逐字保留，初评未被覆盖。

## 1. 最终评审结果

| 审查轮次 | 真实评价 | 已闭合的问题 | 仍存在的研究边界 |
| --- | --- | --- | --- |
| 第一轮：数学、理论与算法 | 严谨性8.8/10；无剩余数学阻断 | 随机时刻积分、乐观deadline说明、二项随机化条件、after-check历史门、不同CPU范围、错误glob与恢复来源 | 理想随机流；不变量部分依赖实现与审核；物理/多源时序未证明 |
| 第二轮：AEI领域 | 初评8.0，最终综合8.2/10；本轮指定科学文本修订已闭合，建议Minor | 最近邻逐机制表、5依赖撤销/未受影响集合、具体事件请求、OldRAVC规则、故障判错语义、图与方法AI披露 | 新颖性7.2、一般性6.8未提高；表示特有工程效益无实测 |
| 第三轮：统计 | 统计严谨性8.5/10，Minor；无重采样/重校准阻断 | 全原始分母/OR/CP/选择/16区间、强Flat等价、拒绝计入、恢复/provider、覆盖时间定义、26文件快照澄清 | 条件模拟证书；百分位bootstrap近似；路线四个异质实现；硬件计时非随机因果研究 |

8.2为最终领域综合判断；数学与统计分数是各自维度，不能平均后当成新的论文评分。Minor指本轮检查出的具体稿件问题已经闭合，不预测AEI实际会给Minor或录用。

## 2. AEI最终维度评价

| 维度 | 最终评分 | 依据 |
| --- | ---: | --- |
| 范围匹配 | 8.7 | 显式知识依赖实际参与选择、来源事务与证据失效，具体请求链可查 |
| 新颖性/最近邻增量 | 7.2 | 清楚的相关来源修订—证据生命周期对象；基础预测/合同/校准已成熟 |
| 实证严谨/可复查性 | 8.8 | 前瞻新确认、完整控制、冻结与实际原始数据，负结果保留 |
| 工程决策/证据价值 | 8.3 | 事件资格、选择性失效与历史拒绝有可执行后果，强程序式也同样正确 |
| 一般性/应用覆盖 | 6.8 | 只验证两个模拟总体、四声明服务、单活动源与可信记录 |
| 主张—证据一致性 | 9.2 | 区分精度、任务与协议适用性；拒绝/未知不写成安全保证 |
| 方法自足性/表达 | 8.8 | 实际选择的旧策略、随机策略、关键先例和测量对象定义完整 |

报告使用原领域审查相同权重，实际加权值8.15，四舍五入8.2。文字修复改善自足性及知识可查性，没有提高创新或一般性，也没有增加独立样本。

## 3. 审稿人现在可以接受的结论

1. 构造并执行任务—来源版本—证据接口，卡选择在扫描之前完成，规范数值安装与统计声明状态分开管理。
2. 标准服务下既有CART计算策略相对Fixed2降低名义/未拟合总体积分损失15.68%/12.61%，伴随约16%更多模拟工作；FlatCART共享该收益。
3. 时间筛选在争用时改变动作，可减少工作和部分观测失败，也会增加积分损失；profile在本研究无额外数值贡献。
4. 528卡的计数/精确CP及96请求选择独立复算一致；直接union与两边际分离；δ=0.15只有18/32配置可行。
5. 构造软件案例中的协议错误附加16/4/2/0/0逐层归因，完整程序式控制亦零错；不把此16案例当真实随机故障率。
6. 全部36新路线、432执行完整，Fixed2普通航线优势、严重几何失败和0路线证书保留。
7. 全部13,824输入、配对结果、三次冻结、缺失索引恢复、计时provider纠正及历史资产可查。

## 4. 剩余Major/Reject风险与投稿建议

**外部Major风险中至高，Reject风险中等。** 这是领域审查的定性风险，未换算为虚构录用概率。

决定性剩余问题是工程知识表示的研究增量：数值收益属于原学习策略，完整程序式实现能等价执行契约语义，profile没有额外行动功效，尚未测表示在维护/变更/跨任务中的效益。增加同输入复用次数不能回答这些问题。若AEI要求一般知识推理或表示特有能力，编辑仍可能认为增量有限。

普通航线无全面优势。新未拟合几何需单独匹配校准，不是zero-shot风险保证。卡条件依赖固定模拟资产与平均操作时钟，种子coin独立性是模型条件；它们不是物理时序、OOD、剩余获授权子集或任务期证书。受控CPU和整路线CPU不同，Full先Flat后的小计时差不能作为硬件因果优势。

本版可按“可执行工程任务—来源—证据接口及其有边界验证”的研究定位准备AEI投稿，保留全部零差和不利结果。若作者坚持以9分为提交门槛，需要新的独立研究，例如跨工程任务或表示维护/变更质量评价，另设冻结协议与确认集。本轮不会继续利用当前确认数据调参制造优胜。

实际投稿前的作者事实单列在AUTHOR_DECLARATIONS：通讯作者邮箱、COI、CRediT、作者审核/责任、独占投稿及funding核实。官方完整Guide访问受限这一行政核验问题未用于给研究扣分。没有提交论文或发送编辑消息。

## 5. 审查原件与复核标准

附录依次收录三轮原报告。每轮的初评、缺陷、证据、建议和最后定点复核一并保留。数学/统计审查实际执行独立只读计算；不是只转述项目PASS。领域审查复核了主表、风险数值和知识机制，并区分全文可得的先例与只读预览。

最终项目核验与各审查一致：1,216,512控制行、131,072重复集成行、432路线执行、528风险卡、96选择、16预定bootstrap区间以及所有原始输入及冻结哈希完整。论文排版/矢量图另由最终QA检查。整个判断以真实证据为依据，未预设Strong Accept。


\newpage

# 附录1：独立审查原件

# R8 round 1: final mathematical, algorithmic and provenance review

Review date: 2026-10-11. Reviewed the current `main.tex`, `r8_formulation`, `r8_knowledge`, `r8_method`, `r8_theory`, `r8_design`, relevant supplementary protocol, F0 numerical implementation, final V3 claim layer/audit, F1 and attachment/inventory records. This reviewer changed no method, strategy or data file and did not inspect unfinished confirmation/stress/route performance to tune a method. No empirical score is assigned to unfinished experiments.

## Assessment

**The current mathematical and algorithmic core is coherent under its stated canonical simulation, iid complete-input and trusted-service assumptions. F0, V3 and F1 remain intact. No numerical-method change or new calibration is requested by this review.** The initially found exposure equation, optimistic time-screen description and policy-randomization assumption have now been corrected in prose and were reread. The V3 history layer preserves the calibrated projection and properly withholds a source's statement after a detected invalid attempt, including after reconstruction.

The CP theorem is exact under its model assumptions. In particular, its Random2or4 interpretation relies on the explicitly stated ideal independent pseudorandom/seed-coin model; it is not an exact conditional theorem for a fixed heterogeneous cap assignment. Native timing is a measured component/inclusive-program/online-route ledger with the stated boundaries, rather than physical service latency. Those qualifications are substantive definitions of the claimed result.

Two small precision edits remain recommended: make the latch's after-check ordering explicit, and replace “all their online bookkeeping” by the measured-component wording in the first timing paragraph. Neither requires changing frozen execution. The numerical and receipt evidence is still subject to final outcome completeness and subsequent empirical review.

## Independent checks actually executed

| Read-only check | Result |
|---|---|
| F0 component hashes | Every frozen component matches |
| Final V3 component, protocol, clock, F0 and audit hashes | Every reference matches |
| F1 sealed files and calibration-result files | Every reference matches |
| Attachment binding references to F0/F1/V3/audit/binder | Match the actual current artifacts |
| All real cards | 528 distinct cells; n = 4096, K = 528, finite schema, correct seal and CP inversion |
| Independent CP recomputation | Maximum absolute upper-bound discrepancy = 0 |
| All F1 requests | 96 Full/procedural status, selected policy, eligible catalogue and witness records reproduced without changing any strategy |
| Independent current V3 normal checks | 32 amended executions on an excluded pilot input, covering all four services/tasks and both implementations; numerical/clock/event projection and candidate-to-receipt authorization/upper bounds agree |
| Independent current V3 fault checks | 10 executions: wrong source, payload, replay, rollback and commit identity, each in both implementations; original numerical projection unchanged, faulted receipts have no upper bound |
| Reconstructed fault scope and clean successor scope | Both latches remain faulted after reconstruction; an independent clean scope remains usable; reusable operational plans remain unrevoked |
| Scoped entry points | Original Transaction and procedural-check entry points restored |

The stored V3 audit additionally reports 16,896 paired pilot paths and 5,632 first-calibration-chunk policy/service paths, PASS, entry-point restoration, and no inspected performance summaries. These counts are the project's broader audit, not a second independent full execution by this reviewer. Its 16,896 count denotes paired contexts: 48 inputs × 22 policies × four services × four tasks. Canonical rollback coverage comes from dedicated fixtures: the reported ordinary pilot-path rollback count is zero. This distinction should be preserved.

## Defect — evidence — recommendation — recheck

### D1. Deadline screening was described as including prior receiver work

**Evidence.** The initial `r8_knowledge` paragraph said it included already accumulated replay work. Frozen `r8_policy.decide` computes `sender = paid_work + predicted_remaining_work` and a tick from sender, receiver base and the candidate's own replay denominator. It has no accumulated receiver-work argument. Actual `controlled()` delivery does include accumulated `receiver_work`.

**Recommendation.** Preserve F0. Describe this predicate as an optimistic mean-work screen that omits previous receiver work; distinguish it from the actual modeled installation and directly calibrated event.

**Recheck: resolved.** The current paragraph explicitly makes those distinctions. A valid late numerical update can still install while its observation attachment is expired. No hard deadline guarantee is asserted.

### D2. Exposure expectation used potentially random integration limits outside expectation

**Evidence.** The initial equation put expected error difference inside an integral from tau_c to tau_f, while the text allowed random delivery times. That right-hand side would still have random limits and need not equal the scalar expectation on the left.

**Recommendation.** State 0 ≤ tau_c < tau_f ≤ T and use

\[
 \mathbb E[L_{\mathrm{hold}}-L_{\mathrm{publish}}]
 =\int_0^T\mathbb E\!\left[
 \mathbf1\{\tau_c\le t<\tau_f\}
 (\|e_0(t)\|^2-\|e_c(t)\|^2)\right]dt,
\]

with integrability for exchanging expectation and integration. The deterministic-time expression is a special case. Alignment of final installation remains a premise, rather than a fact about the held-publication experimental intervention.

**Recheck: resolved.** The current proposition and proof use the indicator inside expectation, an explicit horizon and integrability. The text correctly says the held intervention can alter final arrival and therefore includes another timing effect. The proposition establishes an exposure identity, not a guaranteed improvement from eligibility.

### D3. Independent inputs alone did not spell out the Random2or4 randomization model

**Evidence.** `r4_policy.act` chooses the cap using SHA-256 of the source seed. If the analysis conditions on a fixed cap sequence a_i, independent geometric outcomes need not be identically distributed: Y_i can have risk r_2 or r_4. Their count has generating polynomial `product_i (1 - r_(a_i) + r_(a_i) z)`, generally a Poisson-binomial rather than a binomial law. Independence across method executions cannot repair that distinction.

**Recommendation.** State iid complete inputs, including independent policy randomization, and disclose that the reproducible seed-hash comparator uses the ideal independent pseudorandom-stream model. Do not claim the same exact theorem conditional on a fixed heterogeneous allocation. That alternative requires another sampling/bounding argument; silently changing F1 is not an acceptable remedy.

**Recheck: resolved as an explicit modeling condition.** The current theorem now says independent, identically distributed complete inputs including policy randomization. The following paragraph explicitly describes the seed-hash assumption and the different conditional interpretation. This disclosure does not prove independence of a concrete hash function from its input generator; it identifies the idealized probability model under which exact CP is claimed. No frozen card or policy was changed.

### D4. Controlled native CPU, inclusive replay and complete-route online CPU needed separate names

**Evidence.** V3 `execute_with_claims` maintains `native_charged_cpu_s` from measured components plus unaccounted claim bookkeeping; `executed_replay_including_scoring_cpu_s` and `inclusive_replay_charged_cpu_s` additionally cover offline truth assertions/scoring. The frozen route executor measures the online loop directly. These do not share one end-to-end timing boundary.

**Recommendation.** Report each boundary explicitly and never label the inclusive replay program as pure online service CPU. The component ledger charges shared measured front end/solver/forecast/stream prefixes and individually timed checks/replay; it is not a single complete online timer. Added observer native CPU must remain separate from the frozen operation clock.

**Recheck: substantively resolved.** The current formulation includes an explicit final paragraph separating these ledgers; V3 and the supplement agree. One earlier sentence still says wrappers time “all their online bookkeeping.” Replace “all” with “their measured claim bookkeeping and receiver components” for consistency with the component accounting. This is a wording correction, not a recalibration request.

### D5. Preconfirmation route-absence glob had the wrong filename

**Evidence.** The executed gate used `routes/*/input.npz`, whereas actual route files are `inputs.npz`. That assertion could not establish route absence. The episode inventory separately checked the actual seed files and exactly 8,192 calibration records.

**Recommendation.** Preserve the executed gate/inventory; disclose the route-glob error; correct future executions; establish actual chronology from generation records. Do not rewrite the historical inventory to pretend a corrected check ran earlier.

**Recheck: resolved with preserved provenance.** `preserved/preconfirmation_gate_v1/r8_preconfirmation_gate.py` matches the original inventory's gate hash, and the preserved inventory matches the original file. The corrected future gate uses `inputs.npz`, and `preconfirmation_gate_correction.json` records the error. Actual generation records show the first confirmation collector starts after binding, and route collection starts after all six confirmation/stress collectors. No F0/V3/F1 numerical or selection artifact changed. The original route assertion remains defective; the chronology is supported by the independent local execution records below, not by that assertion.

### D6. Latch equation should make after-check issuance order explicit

**Evidence.** The current equation gives M_(j+1) = M_j AND C_j, followed by A_issued,j = A_candidate,j AND M_j. In the actual observer, conformance is recorded before the matching installation/receipt. Reusing one j for a current check and a current issuance can suggest an off-by-one gate.

**Recommendation.** Define M_j as the state after all receiver checks preceding receipt j, or write the receipt for the newly processed prefix using M_(j+1). Add one sentence that every final receipt reads the updated latch. Stored earlier receipt objects are marked revoked in the ledger; do not imply an unimplemented network notification or independent remote attestation.

**Recheck: code correct; small formal clarification still recommended.** Full invokes `observe` before original installation/`issue`; procedural validation also invokes the observer before its result is used. Tests establish sticky revocation and unchanged numerical installation. The original operational plan is preserved.

### D7. Amendment history should name V3 and the intermediate record unambiguously

**Evidence.** Main design discusses the initial and final versions as “both versions.” The archive actually contains V1, V2 and final V3; the duplicate V2 manifest has the same timestamp and represents no additional method revision. V3 is the one bound to F1 and used by the guarded driver.

**Recommendation/recheck.** The supplementary chronology already names all three and the correct final timestamp. Main text can say “initial, intermediate and final amendment records are archived” to avoid ambiguity. No obsolete V1/V2 hash is used by the actual binding.

### D8. Two missing confirmation JSONL records required recovery, not exclusion

**Evidence.** Recovery audit reports the final two predetermined unfitted-confirmation seeds, 8602046/8602047, absent from JSONL despite their NPZ files existing and collector logs reporting 2,048. Exact file-write cause is not established. The unchanged collector was reinvoked for those same seeds, retaining original archives and the old log.

**Recommendation.** Keep the recovery audit, preserve original arrays, compare deterministic contents and file hashes, restore both records, and retain every predetermined sample. Recomputed host CPU for those shared prefixes is recovery-time measurement and must not be described as a bytewise reconstruction of the lost timing metadata.

**Recheck.** The audit says PASS, all 15 arrays bitwise equal and each original/recovered complete archive hash equal. Counts are restored to the predetermined 13,824 inputs, with zero added independent inputs. F1 calibration and methods are unchanged. This is record recovery, not removal or replacement of adverse samples. This reviewer additionally verified the preserved and current archive hashes and numeric arrays without reading performance summaries.

## Properties and their necessary assumptions

**Source replacement.** The state really has an 18-dimensional perturbation: translation/rotation (six), bias (six), map translation/rotation (six). The relative-error equation agrees with the implementation's row-vector expression. The prior term, robust residual term and local curvature covariance use the same source prior. PSD curvature is a local approximation; it is not a calibrated error covariance. Given unchanged retained solve, exogenous motion and no interleaved independent measurement, final replacement/replay assigns the same state and covariance as final-only delivery at that same time. Earlier exposure can differ. Cold/live-prefix evidence tests the implementation of these assumptions.

**Loss and objective units.** The right-endpoint loss sum is m²·s. In selection, lambda_sel in m² multiplies normalized seconds. The online four-second MSE term, price-weighted remaining seconds and omega in m²·s have matching units. Development remaining-work forecasts retain their original native-label scale as a heuristic inside the new clock; equality of units does not make the forecast an exact operation-cost estimate.

**Hard normalized sender B.** For a delta-iteration stage, at most six correspondence queries per new iteration plus a checkpoint query, nonnegative frozen coefficients, maximum frozen tree path lengths, one decision and one publication form a conservative reservation. Registration completion rejection does not simultaneously emit its rejected positive candidate, so the publication reservation can cover rollback. All policies use the same wrapper/fallback. The acquired cloud is capped at 1,500 float64 xyz rows and the sealed 18D state arrays have fixed sizes; their maximum modeled seal charge is 0.00043723935403809487 s, below the minimum B = 0.006 s. Source sealing itself therefore cannot violate B in this admissible input family before the stage check. This is a hard bound inside the defined operation clock, not on host CPU or arbitrary unbounded input clouds.

**Delivery and observer work.** The self-consistent delivery denominator includes the candidate's own replay; prior receiver work accumulates in actual delivery. The four frozen denominators are 0.099182178375, 0.09836435675, 0.09672871350000001 and 0.09509307025000001 s, all positive. Same-tick versions and rollback are processed before assessment. The two-slot receiver metadata reservation is a constant experimental-clock convention, sufficient for the maximum two marginal statements; additional real claim CPU is measured rather than refitted into that clock. Native timer noise never alters event labels.

**CP and selection.** Condition on the independently characterized, frozen pilot profile/predictors/artifacts, then use iid complete inputs from each declared deployment mixture. The 528 bounds require no independence across policies/services/events on the same input. Selection using those same calibration costs and counts is safe on the simultaneous confidence event, but does not prove score optimality or an unbiased selection advantage. Four tasks and three allowances query the same cards and add no family member. Sensitivity prefixes/confidence grids remain descriptive and do not supply simultaneous coverage across all diagnostic grids. The iid/ideal-stream assumption and matched deployment population are prerequisites, not properties certified by hashes.

**Marginals and union.** Two requested marginal bounds at delta imply only min(1, U_tr + U_obs) for their union. The direct union indicator is trajectory OR observation on the same complete input, and has its own calibrated card. No-positive-version/refusal outcomes remain in observation failure; a superseded candidate does not count at D. A generic M-episode union bound additionally requires each deployment episode to retain its matched marginal risk, on the same calibration confidence event. It cannot be transferred to the dependent route population simply by counting route opportunities.

**Registry lifecycle and trust.** Card counts/bounds/seals are checked at startup in a trusted registry; producer records bind actual finite state bytes to source/version identity. Current configuration match does not establish distribution match. Graph dependencies revoke affected permissions, while the source transaction preserves numerical ordering and legal rollback. The V3 claim child is separate from the reusable operational plan and its persistent scope includes trusted execution identity/source/prior/data/witness. That scope must stay stable across reconstruction; re-enrolling the same faulted execution under a fresh identity is outside the trust contract. The procedural competitor has the same information and a persistent manual latch. The demonstrated equivalence concerns frozen canonical traces and monitored source faults, not every possible history of arbitrary external system reconfiguration.

**Noninterference.** Normal receiver checks return the frozen result unchanged, installation calls the frozen method, and only claim state/child nodes change. Induction preserves numerical decisions, source states, arrival ticks, work and all events. Graph revocation does not climb to the operational parent. After a detected invalid attempt, a later good version can install but cannot reattach a bound in either implementation. The projection theorem transfers original cards for canonical execution without adding a family member. It supplies neither a faulty-history risk nor a receipt-conditioned bound. Missing packets, compromised producer/process, hidden shift, physical timing failures and interleaved updates remain outside this model.

## Binder, inventory and actual chronology

| Record/action | UTC on 2026-10-11 |
|---|---|
| F0 numerical/service freeze | 19:07:18.664676 |
| First calibration collector starts | 19:07:53.248261 |
| V1 attachment amendment | 19:33:16.321415 |
| V2 attachment amendment | 19:41:43.423974 |
| Final V3 attachment amendment | 19:46:40.196132 |
| F1 selection/cards freeze | 19:59:17.439444 |
| Original preconfirmation inventory | 19:59:32.211933 |
| F1–V3 attachment binding | 19:59:32.903035 |
| Nominal confirmation collector starts | 19:59:32.959195 |
| Unfitted confirmation collector starts | 20:01:46.200174 |
| Four stress collectors start | 20:03:44.705431 through 20:05:05.917671 |
| Route input collector starts | 20:05:33.164004 |
| Two missing confirmation records recovered | 20:13:30.154866 through 20:13:47.616647 |

The actual generation ledger confirms the required ordering. At the earlier filesystem check, the earliest noncalibration episode archive timestamp was 19:59:34.886616 and earliest route archive timestamp 20:05:40.517734, both after binding; timestamps are supporting local metadata, not external attestation. The gate's route filename error does not demonstrate outcome leakage, and it must not be erased from provenance.

Verified final manifest hashes:

- F0: `1fb774ff51255dabcf983e800ba291042f77058305d035829ff4f551b52f4c39`
- Final V3: `4be0606be135f4f8be4c39404fd2c7108ae5698ffb220d77ead1f4b628eab7ef`
- F1: `99f832222f54fd931fc4cbfbe6076201c7f21bc424d5b46a75a4278224684cbe`
- V3 audit: `4525804720a1eeec7ec6dcdfcecdae01bfb750ad03393b40278f28303cce45bf`

The currently corrected future gate differs from the original inventory's hash by design; the preserved executed V1 gate matches that hash. It is not a frozen F0/V3 numerical component. The original inventory and F1–V3 binding remain unchanged. The amendment and recovery are explicitly identified rather than hidden in a new F0.

## Completion boundary

Mathematical review does not establish final empirical superiority, route stability, physical localization accuracy or submission readiness. Preserve the reported null/adverse/Flat/Fixed2 outcomes, all predetermined inputs and the separate inference units as the running evaluations finish. Final result tables, hashes, receipt parity, tails, the 16 approximate bootstrap intervals and complete-route timing still require completed-artifact review. No target score was used to reach the judgment above.

## Final read-only recheck after evidence completion

The two remaining precision edits are now verified in the current source text. `r8_knowledge` uses `A_issued,j = A_candidate,j AND M_(j+1)` and explicitly says issuance reads the updated after-check latch. It distinguishes marking local stored receipts from network revocation notification and states the registry-lifetime/process-restart condition. `r8_formulation` now says “measured claim bookkeeping and receiver components,” consistently distinguishing the component ledger, inclusive replay with offline assertions/scoring, and directly timed route online computation. This closes the outstanding wording items D4 and D6 above; the original review is preserved.

The corrected random-time exposure identity, iid complete-input/Random2or4 assumption, exact simultaneous CP argument, marginal-versus-union requirement and attachment noninterference proposition remain consistent. F0, final V3 and F1 were hashed again with zero component/sealed-file mismatches. `final_evidence_verification.json` reports PASS at 2026-10-11 20:25:37.859668 UTC with 13,824 independent episode inputs, 1,216,512 controlled outcomes, 131,072 repeated integrated executions, 432 route executions on 36 route inputs, and 528 cards; original denominators and frozen methods are retained. Compilation logs confirm main and supplement PDF generation. These are completion/provenance checks, not a new empirical-performance evaluation or visual inspection.

**Mathematical rigor: 8.8/10.** Equations, units, conditional guarantees and implementation correspondence are now sound within the declared model, with the important selection, timing and lifecycle qualifications explicit. The score is limited by the reliance on an ideal independent seed/hash-stream model for randomized-policy binomial interpretation, and by the hard-budget/state-machine invariants being supported through code-level reservation arguments and executable audits rather than a complete formal derivation for every branch. These are identifiable limits of the proof package, not newly discovered contradictions. Novelty and empirical superiority are separate dimensions and are not scored here. No target score was used. There is no remaining mathematical blocker under the stated assumptions; final visual QA remains outside this recheck.


\newpage

# 附录2：独立审查原件

# A20–AEI R8：第二轮最终独立领域审查

审查日期：2026-10-11。本报告是作者修订过程中的独立助手审查，不是受期刊委托的正式同行评审。评分依据本次实际文件，不以 9 分或其他目标为锚。本轮只生成本报告，不修改主文、数据、方法、卡片或图件。

## 1. 审查对象与结论

已完整阅读 `main.tex` 引入的 R8 abstract/introduction/related/formulation/knowledge/method/theory/design/results/discussion/conclusion、其 generated results/discussion，以及 `supplement.tex` 的 R8 prefix（`r8_supplement_protocol.tex` 和全部 758 行 `r8_supplement_results.tex`）。核对了 18 个分析 CSV 的结构和主要结果、真实 F1 卡、96 个选择计划、432 行完整路由结果、`real_card_fault_cases.csv` 的全部 18 个案例、preflight 的依赖撤销记录、AI 和作者声明。已确认新编译 PDF 的题名和 28 页正文；本报告不替代逐页排版审查。保留历史研究用于核对定义和证据分隔，没有将其合并到 R8 推断。

**综合评价：8.0/10。建议 Major revision；主要风险是 AEI 创新和知识价值的定位，不是当前发现了数值造假或样本分母错误。**

R8 已由原来的元数据示例提升为实际执行的任务–来源–证据接口：有预感知承诺、统一预算的数值执行、来源版本替换、实际安装事件、直接 union 校准、可用声明及历史撤销。新确认、绑定约束、路由和软件机制数据足够支持一个有边界的工程信息学原型研究。Full 与完整程序式实现等价也被诚实保留，不能因为一个正确实现可用程序重写就否定知识表示本身。

目前仍未充分建立更强的表示层研究优势。数值改善来自既有 CART 策略，profile 谓词无增量；图结构没有独占的选择、风险或拒绝能力，维护/使用成本优势也未测量。主张应是可复查的语义接口及其执行性质。若编辑要求显著的一般知识推理、表示特有的新增效力或物理检查系统验证，当前证据仍可能被认为增量有限。进一步堆积相同输入的运行次数不会解决此项风险。

## 2. 独立复核的主要证据

本轮使用 Python CSV/JSON 读取和 SciPy 精确 Beta 分位数重算，不仅接受 `final_evidence_verification.json` 的 PASS 标记。没有重新执行全部 1,216,512 控制结果，也未声称在新主机复现原生 CPU 的相同值。

| 证据 | 本轮核对结果 | 能支持的结论 |
| --- | --- | --- |
| 独立输入 | 8,192 calibration + 4,096 confirmation + 1,536 stress = 13,824；48 pilot 单列 | 新的独立几何输入，不能把重复策略运行增加到 n |
| 卡片 | 528 个唯一 profile/service/policy/event 组合；每卡 n=4,096；按 β/K=0.05/528 重算 U 的最大绝对差为 0 | 当前表中的 CP 值与公式一致；不是物理总体自动匹配的证据 |
| union | 每个 k_union 均满足 max(k_tr,k_obs) ≤ k_union ≤ min(n,k_tr+k_obs)；原始 OR 构造在主文清楚给出 | 主文没有把两项边际界误称为联合界 |
| KG1–Fixed2，standard | 名义 loss −15.6784%，work +16.0864%；unfitted loss −12.6111%，work +16.0749% | CART 的精度–工作权衡；不是知识图层独占收益 |
| KG1–FlatCART，standard | loss、work、三项事件、readiness、success、stop/publication/installation 汇总相同；主区间为精确零差 | 该场景的数值收益由相同预测/动作策略共享 |
| Profile 模块 | 48 行 Profile/CART 或 Profile/RF 的 stop/publication/event/loss/work 变化全部为 0；guard rate 可为 1 | 触发不等于产生决策增量；当前实验未证明 profile 模块的数值功效 |
| Time/CART，contended | 两个 confirmation profile 均 2,048/2,048 改变终止点；名义 ΔL=+0.00509367 m²s、ΔW=−3.60007 ms、ΔO=−1.66016 pp；unfitted +0.00417946、−3.58264 ms、−1.90430 pp | 真实动作和代价交换，不是均匀变好或截止时刻保证 |
| 请求 | 96/96 与 validated Flat 相同；δ=0.10/0.15/0.20 分别 10/18/20 个 SELECTED，32 个请求/allowance | 有限构造目录的任务可行性；不是现场请求成功率 |
| 集成执行 | 64 个 profile/service/task/variant 汇总 × 2,048 = 131,072 重复执行；32 个 Full–Flat 上下文 numeric/event/claim 差均为 0 | 完整程序式实现复现同一语义；重复执行不提供额外独立样本 |
| 实际卡片故障 | 16 invalid + 2 normal；incorrect attachments 为 none 16、matching 4、current-version 2、history 0、validated procedural 0；两正常案例含 legal rollback 均通过 | 分层协议合规检查；不是随机故障率、风险改善或图实现独占能力 |
| 路由 | 36 独立输入、12 方法、432 原始执行；Full–validated Flat 的 17 个非 CPU 数值/事件/工作字段全部相同；所有 episode cards authorized=0 | 实际连续定位执行和明确 provisional 服务；没有路线/任务期证书 |
| 不利路线 | C172 ordinary 的四个 KG1–Fixed2 配对 RMSE 差均为正；平均 +0.04547 cm、CPU +0.29215 s、success −1.08696 pp | Fixed2 的竞争力是稳定可见的结果，不应隐藏 |
| 影响诊断 | 名义两最大贡献占净收益 27.9944%；unfitted 10.0172%；删两项后均值诊断仍正，原 2,048 个样本保留 | 改善集中程度可评估；删除诊断不替换主推断 |

全部分析 CSV 未发现文本形式的 NaN/Inf 数值字段。该检查不是对所有统计假设或代码的完整证明。

## 3. AEI 范围与增量判断

今日已读的官方范围来源为 [Elsevier AEI description](https://shop.elsevier.com/journals/advanced-engineering-informatics/1474-0346)。期刊要求显式表示并使用知识，以新研究支持知识密集工程任务，并作严格评价。它不强制 RDF/OWL；也不要求一个图实现必须在相同语义程序之上提高定位精度。

| 范围维度 | 当前判断 |
| --- | --- |
| 工程对象 | 几何空气框架上的相对定位、观测期限和持续轨迹，是明确的工程任务。0.10 m 和期限被正确声明为研究代理，而非航空标准。 |
| 显式表示 | K=(V,τ,R,σ,Γ)、八类实体、依赖图、指纹和源事务状态，比旧版“参数改名为知识”更实质。 |
| 知识使用 | 预感知选择/拒绝、动作候选约束、版本替换、事件声明匹配和选择性失效均有执行后果。 |
| 新科学问题 | 最具体对象是“相关数值修订与完整策略/安装模型的统计证据如何保持对应”。这比泛称 contract-anytime 或 risk-aware localization 更有区分力。 |
| 严格评价 | 匹配模型/价格/预算、完整程序式基线、精确卡、独立确认、绑定负载、软件生命周期和直接路由执行，均有实质价值。 |
| 一般性 | 当前仍局限于两项校准混合、四个人工服务、单活动源、可信生产者和固定例程；没有证明维护收益或跨工程任务的通用性。 |

Pant et al. 已经使用误差–延迟合同作 anytime 估计/控制共同决策，并有鲁棒 MPC 和物理航空平台验证（IEEE TCST 29(2), 768–779, 2021；DOI `10.1109/TCST.2020.2979388`；[正式页](https://ieeexplore.ieee.org/abstract/document/9051687)、[作者全文](https://yashpant.github.io/assets/pdf/TCST20.pdf)）。R8 已正面承认这个最近邻，这是本轮的重要改善。Benveniste 的合同组合、已有 anytime/metareasoning、LTT/CRC/CPC 的校准，以及来源/延迟状态处理的既有思想不能计为新基础理论。

R8 可成立的增量是一个明确的数值/证据服务对象及其可执行生命周期：同一扫描与不可变先验的版本序列，预感知政策承诺，完整事件/总体/安装身份，当前声明和源级历史状态分别管理，以及声明撤销不干扰规范数值轨迹。它既没有 Pant 的闭环控制保证，也没有新的通用合同代数或统计风险界。与 semantically complete Flat 的等价表明增量在服务语义，而不在图的排他性。

## 4. 需修改事项：缺陷—证据—建议—复核标准

### M1. 新颖性对象仍应写成可比较的具体对象（Major，优先级 P0）

**缺陷。** Introduction/related/discussion 已诚实承认先例，但新增内容仍主要由数个既有机制的串联描述。只说“task–source–evidence interface”不足以让领域读者判断科学增量来自何处。

**证据。** R8 related 第二段认可 Pant；theory 的 replacement/exposure 是明晰的执行性质，CP 是标准方法，history latch 本身是标准单调状态构造。标准服务 graph/Flat 的选择、数值和授权全部相同。这些事实排除了“首次合同分配计算”“更强风险定理”“图存储带来精度增益”的故事。

**修改建议。** 增加一张小机制比较表，至少列 Pant、合同理论、LTT、运行时保证和本稿；明确研究对象、执行决定、统计/控制条件及评价端点。对已有来源/延迟状态处理也引用已有依据。表中不要将只读到摘要的文献标为“不支持”。贡献第一项应明确“表示/执行什么此前未被这项任务接口连接的关系”，贡献第二项保持服务实现定位。

**复核标准。** 不依赖形容词即可找出新增对象、条件和可观察行为；每项新意有对应实验或执行性质；与 Pant 的区别不依靠其未被证明缺失的功能。不能用本稿更多运行次数压过 Pant 的物理/闭环验证。

### M2. 独立知识价值的最佳现有证据未进入正文展示（Major，P0）

**缺陷。** 完整 Flat 等价不是缺陷，但表示层的 inspectability/selective invalidation 是主要剩余贡献，却主要以文字陈述。当前主体图和结果篇幅更突出精度与工作；读者仍可能将本文当成一般定位软件集成。

**证据。** `preflight.json` 已有五个实际依赖变更：forecast:rf 撤销 168/528，artifacts:nominal 264/528，event:union 176/528，service:standard 132/528，clock 528/528。请求表也有一个很具体的任务实例：unfitted/standard/δ=0.10，observation 选择 OldRAVC（10 个合格策略，U=0.09994596），trajectory/both/union 均拒绝。这个观察界只比允差低 0.00005404，必须同时展示其脆弱性。

**修改建议。** 用现有记录给出一条完整执行链：同一声明总体/服务输入，任务事件变化如何改变资格；依赖变化如何使相应卡撤销且不扩大到无关卡；源版更新后哪些数值内容保持、哪些声明变 provisional。将上述撤销集合和实际状态放入正文小表或 SI 可见交叉引用。把其价值描述为显式、可检查的一致性语义，不推断维护努力、人工错误或开发成本优势。

**复核标准。** 读者可以从类型/关系追到具体动作或证据状态，且能复核受影响与未受影响集合。Full 和完整 Flat 同样正确这一事实保留；若声称维护收益，则必须另有相应研究，当前不需要虚构此类收益。

### M3. 实际被选的 OldRAVC 规则未在当前论文自足定义（Major，P0）

**缺陷。** 关键比较器不能仅靠名字和代码归档定义。OldRAVC 是所有 unfitted relaxed/standard 请求及 contended trajectory 请求的实际选择，但新 Methods 只将它列入 catalogue。

**证据。** `r8_method.tex` 第 25 行列名；R8 SI prefix 没有规则定义；保留 `supplement_r4.tex` 仅称“earlier frozen policy”。关键标准任务表和真实选择计划依赖 OldRAVC。

**修改建议。** 为 OldRAVC 补一段或 catalogue 表行：所用旧预测模型/输出、停止和发布逻辑、固定阈值/价格，以及统一预算、安装和 rollback 包装。Residual 和 Random2or4 也简述，Random2or4 给出 coin 概率及 seed-hash 机制，不仅说 seeded。表述应来自冻结代码，而非为了本轮结果重新设计策略。

**复核标准。** 不打开历史开发目录即可判断三种策略如何执行，规则与 F0 导出一致；新文字不能改选出的策略、卡或事件映射。OldRAVC 不是未经说明的“oracle”或新拟合模型。

### M4. 历史拒绝的判错依据需与统计风险分清（Minor，但影响主要贡献措辞，P1）

**缺陷。** “incorrect attachment”容易被读成已经观测到风险超界。两个 history 案例中，后来有效数值版本可正常安装，而界撤销是研究定义的执行合规要求；本实验没有证明该后续 pose 的风险必然变大。

**证据。** `invalid_history_then_valid` 和 `reconstructed_fault_scope` 是 current-version 层仍通过、history 和 strongFlat 拒绝的仅有两项。16/4/2/0/0 来自构造的软件标签；normal/legal_rollback 都正常通过。Projection theorem 保持规范数值/event 映射，不是对任意 fault population 的风险界。

**修改建议。** 在故障表/图附近明确：这里的 incorrect 是违反声明的可信规范执行/来源历史协议；source-history 拒绝是保守的适用性策略。解释为什么 detected invalid attempt 使这次源执行退出既有证据范围，以及 successor source 为何可以重新承诺。保持数值有效与证据状态分离，避免“history improves risk”或“zero false applicability in general”的语言。

**复核标准。** 条件良好的规范输入与构造历史故障的分母不混合；当前两项应拒绝、legal rollback 应通过；强 Flat 也零错附加。没有将 fault 后仍发放 receipt 的子集暗示为条件校准总体。

### M5. 模块可辨识性和任务选择作用需精确归因（Minor，P1）

**缺陷。** 将这些负结果清楚保留是正确做法，但还可更直接说明为什么 profile 完全冗余、为什么 contended 的 time 看起来是统一截断而非精细适应，以及当前 task 类型的变化主要改变资格/拒绝而非在每种服务内换策略。

**证据。** 48 行 profile 无变化；两个 confirmation profile 的 time 在 contended 每个样本都改变端点，relaxed/standard/tight 均为零。δ=0.15 的 relaxed/standard 四 task 选择同一 profile 内的同一策略；contended 仅 trajectory 通过；time screening 反而使 KG1 轨迹界超过 0.15，selector 选择 Flat/Old 策略。

**修改建议。** 用已有 stop/budget/guard 数据补一句因果解释：更早终止或共同预算怎样先行限制了 profile cap 的可选动作。保留 profile 作为被测试但当前没有额外数值功效的模块。把 task 的已测作用写为事件可行集合及声明/拒绝，不能回到 R5 的旧目录增益或暗示本轮四任务各选更优策略。

**复核标准。** rule firing、改变候选集/终止点、改变数值结果和附加状态分别报告；profile 零效应不被改造成“成功保护”的证据；time 的损失代价和观测收益同时可见。

### M6. 工程一般性与闭环边界是仍存在的研究限制（Minor 的措辞；Major 风险的根源，P1）

**缺陷。** 多几何/路由结果增加适用性，但仍是固定虚拟资产和人为服务模型上的一个任务接口。其工程一般性不能仅由 13,824 个输入或 72 模拟路线小时推出。

**证据。** 卡条件为两个离散混合、四服务、单活动源、固定地图/模型和可信记录； route population 被正确拒绝。路径是 imposed，不根据估计误差作控制。0.10 m、负载和截止时刻均是研究设定，照片不补足现场误差或嵌入式时序。

**修改建议。** 保持当前边界，增强 discussion 中“可迁移的是哪些接口关系、必须重新验证的是哪些数值/总体/时序条件”的具体说明。避免 digital twin、物理安全、WCET、隐性 OOD 检测或闭环控制暗示。若后续要作更广任务论断，需要另一类工程任务或现场测量；本轮不应伪造，也不要求为已有有界主张临时补现场试验。

**复核标准。** 架构反馈箭头解释为任务/声明服务；route 无 episode/mission 证书；native CPU、operation clock 与物理延迟分开；没有从概念可扩展直接宣称实证 generality。

## 5. 行政与投稿格式事项：不作为研究分母或学术造假问题

1. `AUTHOR_DECLARATIONS.md` 中通讯作者/email、真实 COI、CRediT、全体作者审核/同意及资金措辞确认尚缺。它们是实际投稿前事项。不得由助手补造，也不因未提供这些事实给研究方法扣分。现稿没有假称所有作者已批准。
2. 当前新 Methods 没有显式写研究代码/数据图的 AI 辅助工具、版本和开发者；总声明及独立记录已有 OpenAI ChatGPT/Codex (GPT-6)，但 [今日官方 Elsevier GenAI policy](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals) 要求研究过程使用在 Methods 说明。建议在 Methods 加真实简短记录。
3. `r8_introduction.tex` 的 architecture caption 没有逐图 AI 辅助记录；contract_mechanism caption 有 GPT-6 与 Python code 记录。当前政策允许 AI 辅助解释图，但每张解释图 caption 应说明工具、版本、用途，并有总声明。数据图通过可复现分析生成，不需要把每张数据图当生成式示意图。保持原始照片，模拟图明确模拟。
4. 未使用通用 imagegen 来制作这些精确图件。准备 graphical abstract 时仍应采用合规科学制图；不要把“解释图允许”扩张成通用生成图像工具允许 graphical abstract。
5. AEI 官方 Guide 的正文在本次仍是 403/Disabled/防护访问问题。graphical abstract 是否必须、摘要长度、期刊级图像规格和当前匿名提交格式未完整核验。不能写“全部 Guide 检查通过”；此项与已读的官方 Scope/Elsevier GenAI 要求分开。它是提交核对项，不能替代本报告的领域结论。

## 6. 评分与审稿风险

分数用于修订判断，不是期刊录用概率。权重用于显示判断结构；当前加权 8.015，四舍五入为 8.0。

| 维度 | 权重 | 分数 /10 | 理由 |
| --- | ---: | ---: | --- |
| AEI 范围匹配 | 15% | 8.5 | 明确知识实体、依赖和执行后果；仍应更突出知识生命周期结果 |
| 新颖性与最近邻增量 | 25% | 7.2 | 服务语义有具体增量；合同、校准、调度和单调 history 构造均非新基础理论 |
| 实证严谨性与可复查性 | 20% | 8.8 | 新确认、完整基线、统一预算、卡/route/故障分母分离；本轮未重跑全研究 |
| 工程决策与证据价值 | 15% | 8.0 | 拒绝、承诺、版本/卡生命周期实际执行；故障效果需保持合规定位 |
| 一般性与应用覆盖 | 10% | 6.8 | 固定模拟混合、人工服务、单任务接口；没有现场或维护/usability 验证 |
| 主张与证据一致性 | 10% | 9.0 | 明确等价、零效应、失败、脆弱边界；避免把既有研究与新数据混合 |
| 方法自足性与表达 | 5% | 8.0 | 大体清楚，但 OldRAVC 定义缺失、机制结果与已有研究对照可更集中 |

**Major revision 风险：高。** 最可能的评论是“有完整工程实现，但新的知识表示/推理研究贡献还需证明和定位”，以及关键实际选择策略描述不足。前者可用已有执行/依赖结果和明确最近邻比较改善，不能靠夸大精度或软件案例。

**Minor revision 风险：高。** AI Methods/逐图披露、故障标签语义、模块冗余解释、术语/前后证据范围和投稿行政事项均需完善。这些多数不需要再生成研究数据。

**Reject 风险：中等。** 若编辑认为语义接口仍属于一般软件封装，或要求更强的一般知识增量，当前有限总体/模态可能不足。没有在本轮主要表发现足以单独建议因数值失实、错误独立样本数或不公平弱基线而拒稿的问题。不能从这句话推出研究代码不存在尚未发现的问题。

建议先完成 M1–M3 的实质修订，再做一次对应最终稿的独立复核。只补行政信息和英语润色不足以把本轮合理提高到 9；同样，正确保留 strongFlat 等价和 profile 零效应不应被“修成”积极效果。

## 7. 本轮文件定位

审查读取时的核心源指纹如下，避免随后修订与本报告混淆：

| 文件 | SHA-256 |
| --- | --- |
| `main.tex` | `62c586ebfc6cd52746416a93a9e5529fec7e26fa089fc1779e94dbb132bf2671` |
| `sections/r8_knowledge.tex` | `fbb57be8f2f2cfc6f48df8144b54ca3ce96949a76dfe7e46276aa02007504e06` |
| `sections/r8_method.tex` | `3c252c4cad430328aec1c5d1bfe08bce87fa8e0665c69ebb13bf4580afd1b2ed` |
| `sections/r8_theory.tex` | `0b17f8aa09e180d33b01d41eecf44530f0d72e4e550347daf49702a60d07a38a` |
| `sections/r8_results_generated.tex` | `b4ec894d19f0d0e98a691b4cfdbae4a099cc41e171c8dd71fda7ae2954df1861` |
| `sections/r8_discussion_generated.tex` | `bdc9ed905dd28c2c0e775d2c8f2c12b6ce511f50ea24c9f26cd9bb87c6d90334` |
| `data/r8_final/analysis/request_feasibility.csv` | `a2a0b3e6901027e2cafaca6a97237ddbd647913bc12ab6373a4b8822347b3216` |
| `qa/r8/real_card_fault_cases.csv` | `7db224484ed44a39957d4d45d414febdbc5c550e519eb07b069c2615220c66f2` |

阅读范围和独立复核程度均以本报告为准；其他审查者的 PASS 或评分没有作为本轮结论的替代。

## 8. 文字修复后的最终复核（追加，2026-10-11 20:46 UTC）

本节保留上述第二轮初审及 8.0 分原结论，追加对指定修复的复核。没有重做研究或要求改变冻结策略；本次只检查新增相关工作表、方法定义、依赖/请求实例、故障含义和 AI/反馈披露。18 个分析 CSV 的 SHA-256 均仍与完成证据的 `analysis_manifest.json` 一致；`source/r8_policy.py` 的指纹仍为运行绑定中的 `55bdbc0fd285bdd62f16a9561af16e1b02738c97df3001b75dcca8aa3a34a8ea`。最终 PDF 正在编译，本节不宣称其排版已再次全部验证。

| 原事项 | 现在的实际修复与复核 | 状态 |
| --- | --- | --- |
| M1 最近邻增量 | `tab:mechanism-precedents` 正面比较合同理论、Pant、LTT、runtime assurance 和本稿的研究对象/决定条件/评价边界；明确 Pant 的物理及闭环验证。加入 Bar-Shalom 延迟测量先例，并把本稿对象限制为同一次 solve 的相关修订。表没有给未核验能力作负面标记。 | 本轮文字要求闭合；真实创新强度仍属有限接口增量 |
| M2 知识价值可见性 | `tab:r8-dependencies` 使用原五个实际 fixture，撤销 168/264/176/132/528，未受影响 360/264/352/396/0，均与 528 总数和 preflight 对应。新增 unfitted/standard/δ=0.10 的真实请求链：observation 有10策略、选OldRAVC；其他3要求拒绝；U和极小margin保留。明确无维护成本优势、程序实现可共享语义。 | 闭合；没有把既有数据包装成新观测 |
| M3 关键策略定义 | OldRAVC 的480/120开发划分、depth6、六输出、legacy C172特征、发布/停止/终止及统一预算被写出。已对照 `r8_policy.decide`、旧 `checkpoint.decision` 和冻结概率。复核中发现停止句首次遗漏eligible/风险阈值，作者随后修为“From iteration two, an eligible candidate ... frequency ≤0.30 AND gain ≤remaining-work cost”，与代码的 iteration≥2 及条件合取一致。Residual 与 SHA-256 seed coin、cap4概率0.4654427646也清楚给出。 | 闭合；方法和旧模型没有修改 |
| M4 fault 判错语义 | 新 fault 段明确 incorrect=协议适用性违规；数值不干扰可使风险不变，但协议仍暂停声明。16/4/2/0/0、两个有效控制及强程序式零错仍保留。 | 闭合；没有宣称测到风险实际超界 |
| AI Methods 与架构 | Methods 说明 OpenAI ChatGPT/Codex、GPT-6、开发者OpenAI、实际科研/分析/绘图用途；architecture caption 说明GPT-6辅助Python示意代码。反馈箭头被写为未来请求/校准接口，未测试自主反馈重规划或物理控制。 | 本轮指定科学文本/解释图披露闭合；作者实际审核仍待事实确认 |

M5 的 profile 零效应、time 的服务依赖代价和强 Flat 等价仍完整保留；未为了消除负结果而更改数据或新造有效模块。M6 的有限混合、人工服务、单活动源、可信代码、无闭环/物理验证/通用维护效益仍是研究边界，不能靠文字修复消失。当前文稿对这些边界的说法与证据相符。

**追加后的实际综合评分：8.2/10（相同权重的加权值8.15）。针对本轮识别的稿件科学文本缺陷，建议由 Major revision 降为 Minor revision；这一判断不等于预测 AEI 会给 Minor 或录用。**

| 维度 | 初审 | 最终复核 | 改分依据 |
| --- | ---: | ---: | --- |
| AEI 范围匹配 | 8.5 | 8.7 | 依赖结果和请求实例现在直接展示显式知识的使用 |
| 新颖性与最近邻增量 | 7.2 | 7.2 | 定位更清楚，但没有新增算法、证明或外部工程效益证据 |
| 实证严谨性与可复查性 | 8.8 | 8.8 | 原证据不变；文字修复不增加独立样本或研究功效 |
| 工程决策与证据价值 | 8.0 | 8.3 | 已有选择性失效和事件实例可直接追查，含强Flat等价和脆弱界 |
| 一般性与应用覆盖 | 6.8 | 6.8 | 固定模拟总体/服务和物理、维护边界没有改变 |
| 主张与证据一致性 | 9.0 | 9.2 | fault语义和未来反馈明确，不再容易被误读为实测超风险或自主闭环 |
| 方法自足性与表达 | 8.0 | 8.8 | 实际被选的旧策略、随机策略和具体先例均有自足定义 |

最终领域建议是按“可执行工程任务–来源–证据接口及其有界验证”提交，保留负结果。原本可通过现有记录完成的 M1–M3 已实际完成，不应继续用同一文字缺口阻止推进。AEI 外审提出更强知识增量/一般性要求的 **Major 风险仍为中至高，Reject 风险仍为中等**；这些风险源于研究范围，而不是可通过再次润色获得的分数。通讯作者、COI、CRediT、真实作者审核/责任确认、官方Guide及最终图/PDF检查仍由相应事实与行政流程闭合。

本次变化支持小幅提高表达与可复查知识价值的评价，**不支持9分**。它既未产生图表示独占能力，也未增加物理、跨任务或维护效益验证。

最终复核读取的关键新增源 SHA-256：

| 文件 | SHA-256 |
| --- | --- |
| `sections/r8_related.tex` | `bee4eb74a23dfb66acfb40950cc5f148d7810dc8aa10f03c541ef27cedb0ab7b` |
| `sections/r8_method.tex` | `fcc19546061a671bc5eb0e5dea13302a3fa5c0ce83689b00daea8cd6e21c19c5` |
| `sections/r8_results_generated.tex` | `d301a4eb3e139bc4fec7374d8d2ddd20bd22f0d31a5b7bad4df3e86f2e1ebb24` |
| `sections/r8_introduction.tex` | `511fcc84fadb9a926559da9c93e173b9f1cabab27a16e6e077196a943c38ab5d` |
| `sections/r8_supplement_protocol.tex` | `6349534525f9298f4bae1bfac7062df1e7e3c53e96e50a0e0c92a7a2475758c7` |


\newpage

# 附录3：独立审查原件

# A20-AEI R8 第三轮最终独立统计审查

审查日期：2026-10-11。审查人：独立统计 reviewer agent。范围：新 R8 的 A–G 证据、原始结果、实际冻结/恢复记录和主文/SI；不将 retained R4/R5 复用分析计入新确认。本轮只写本报告，未改源码、输入、结果、卡片、选择、冻结记录或计时测量。

## 审稿判断与评分

**统计审稿建议：Minor Revision。评分：8.5/10。未发现需要 Reject、重采样或重做卡片的统计阻断项。** 评分针对统计设计、结果正确性、公平归因与证据边界；不替代 AEI 对工程创新价值的判断，也不预设 9 分。主结论通过独立原始复算，三处报告措辞问题已由作者修正并复核。

可信的结论是：标准服务下冻结 CART 计算策略相对 Fixed2 的平均 loss/observation 改善，在两项新 confirmation populations 中得到支持；同资源的 FlatCART 获得相同结果；Full 与 task-aware fully validated procedural control 的数值、事件和公开 receipt 完全相同。现有结果支持明确可审计的 task/source/evidence 接口与服务条件下的计算取舍。Representation 独占精度/风险/拒绝优势、物理安全、跨分布或 mission 风险，以及维护成本收益均没有新增量化证据；当前讨论已保留这些边界。

评分未达 9 的主要原因是：CP 有效性以声明的 iid complete-input/ideal-stream 模型和固定 mean operation clock 为条件；主比较区间是 approximate percentile bootstrap；native CPU 不是随机化硬件性能研究；36 routes 为少量异质预设 realizations；工程生命周期收益尚未测量。这些限制已经披露，不能将它们包装成更强的结果。

## 独立核验方法及完整性

没有调用项目的主分析/写稿程序来代替复核，也没有为获得期望分数调整方法。使用独立只读 Python：直接读全部 216 个 controlled CSV chunks，重算计数、OR、均值、card inversion/seal、校准目标、feasible catalogue 和 96 个选择；按 seed 从原始确认配对差值重采样，独立重算 32,000 次 bootstrap（以 128 次分块，与作者 256 次分块不同），核对全部 16 个区间。区间端点/均值差小于 2×10^-15。

另外直接验证全部 13,824 raw archives 的 hash 与记录/manifest，对 8,192 calibration records 的完整 JSON digest 复核，核对 64 个 integrated chunks 的结果/F1/V3/binding/driver hashes，并重算逐 context denominator、receipt coverage 和 Full/Flat equality。对 432 route 原始 trace/capture archives 重算 numeric metrics，验证 36 个 route inputs 的 manifest/hash；host CPU 只核验归档记录与分解口径，不假装在新执行中重现同一个 CPU 数字。

| 检查对象 | 独立复核结果 |
|---|---|
| F0 / V3 / F1 | 48 个 F0 components、4 个 V3 components、8 个 F1 files、256 个 calibration-result file hashes 一致 |
| Development sources | 原 1120-source dataset hash 一致；926 train / 194 validation 按 source 分组，集合无交集；CART/RF export hashes 一致 |
| Excluded pilot / final draws | 48 pilot 与 development、calibration、confirmation、stress seeds 分离 |
| Final input index | 恰好 13,824 个 unique seeds，全部 block 范围及 NPZ inventory 匹配 |
| Controlled results | 1,216,512 行完整，720,896 cal / 360,448 confirm / 135,168 stress；每 seed 恰好 22×4=88 行 |
| 同源联合事件 | 每一行 union_failure = trajectory_failure OR observation_failure；observation_failure = 1−capture_success |
| Stage cap | 全部 controlled rows 的 sender_work 不超所属冻结 budget |
| Actual cards / plans | 528 张卡各 n=4096；k、U、score、seal 一致；全部 96 个 Full/strong-Flat plans 与独立选择一致 |
| Integrated confirmation | 131,072 重复执行、4096 unique inputs；全部 profile/service/task/variant contexts 各 n=2048 |
| Route data | 36 inputs、12 methods、432 executions；每 geometry/condition/method 为 4 matched realizations，299 scan opportunities/route |
| Derived analysis | 528 summary、528 tails、72 influence、144 ablation rows 对上 raw；17 个 analysis-table hashes 及当前 analysis script hash 一致 |

数量明确区分：13,824 是 source inputs；1,216,512 是共享输入上的 paired outcomes。Integrated task/validator executions 及 provider 的四次审核重跑均不增加输入 n。Route 的 6000 ticks、299 opportunities 或十二个 methods 不成为 independent iid episode samples。

## 冻结、分离和异常恢复

实际 chronology 为：F0 `19:07:18.664676`；首 calibration collector `19:07:53.248261`；最终 V3 `19:46:40.196132`；F1 `19:59:17.439444`；preconfirmation inventory `19:59:32.211933`；F1–V3 binding `19:59:32.903035`；首 confirmation collector `19:59:32.959195`（全部 UTC）。Six non-cal collectors 顺序结束后，route inputs 在 `20:05:33.164004` 开始生成。所有 F0、V3、F1、binding hashes 保持一致。

预指定 phases 的实际独立 seed 数为 4096/4096 cal、2048/2048 confirm、4×384 stress。训练/验证 source 的划分代码先分完整 source，再展开 checkpoint labels。冻结 predictor、price、clock、lambda_sel=1 m²、catalogue、risk allowances 与 primary family 没有因确认结果重拟合或改选。

V1 同 scope 重建可清除 procedural latch 的缺陷、V2 中间 driver/provenance 闭合以及最终 V3 timer/binder 修复均保留历史。V3 改变附件语义，不改变 numerical/operation-clock/event projection；它是 post-F0、pre-F1 amendment。主文/SI 正确披露此 chronology，没有将其伪写为初始 F0 功能。

原 preconfirmation gate 的 `*/input.npz` 单数 glob 没有覆盖实际 `inputs.npz` 文件名。本人验证原源代码 hash/原 inventory 均保留，未来 glob 已改正；实际 ledger 显示 route inputs 发生在 F1/binding 与六个 collectors 之后。本次研究的 chronology 有独立记录支持。不能把错误 gate 的“PASS”本身当成正确 route-absence 检验。

两条缺失的 unfitted confirmation index records 为 **8602046、8602047**。逐一验证保留原 NPZ 与最终 NPZ 的完整 SHA 相同；15 个数组均同 dtype、shape、逐元素 bitwise 相同。它们是恢复原预定输入，没有新增/删去/换 seed。原 JSONL 的 prefix/front/stream CPU 元数据没有字节恢复，最终 CPU metadata 来自 recovery-time measurement。SI 与 discussion 已明确这一点。该恢复保留全部 outcome denominator，不构成挑选较有利 seed。

## CP family、实际请求和适用总体

独立重算 one-sided upper bound：k<n 时 U=Beta^{-1}(1−0.05/528;k+1,n−k)，k=n 时 U=1。每张卡是 4096 独立 complete inputs 上的一项二元事件。跨 policies/services/events 的同 source 相关性由 union bound 容许；不能将 88 个重复执行乘进 n。

22×2×4×3=528 维族保持冻结。四 task、三个 allowance 是查询这批卡，不另拟合，故没有新增 family factor。Both-marginals 分别查询两张边际卡；union 的 k 是同 episode OR 的实际计数。全族 confidence、episode allowance、individual scan error 和 mission 风险区分正确。28512-row prefix/confidence/allowance sensitivity 是描述性，未据此更改 F1 或重认证。

| Primary selected / fragile card | k / 4096 | 独立核验 U | 相关 margin |
|---|---:|---:|---:|
| Nominal / standard / FlatCART3 / union | 286 | 0.085836 | .15−U = 0.064164 |
| Unfitted / standard / OldRAVC / union | 397 | 0.115254 | .15−U = 0.034746 |
| Unfitted / contended / OldRAVC / trajectory | 516 | 0.146330 | .15−U = 0.003670 |
| Unfitted / standard / OldRAVC / observation | 339 | 0.099946 | .10−U ≈ 0.00005404 |

.15 的 32 configured requests 中 18 selected、14 refused；全部 96 requests 中 48 selected。这是固定配置的 catalogue feasibility，不能当作随机 field-request success rate。标准选中 nominal FlatCART3 / unfitted OldRAVC 与固定 calibration loss+work 目标一致；其有限 confirmation sample loss 不必最优。

**Random2or4 的模型条件必须保留。** 冻结 cap-4 probability 为 0.4654427645788337，实际 rule 为 SHA-256(seed) threshold。`r8_theory.tex` 第25–30行已明确：binomial 解释假设 seed-derived coin 为 complete-input 模型中独立随机化；若条件于固定异质 cap assignment，应使用不同 bound。独立列举 hashes/频数不证明具体 SHA output 的独立性，本审查也没有证明它。现有 24 Random2or4 cards 的 exact CP 解释以该已披露模型假设为条件。其数值匹配，不影响预指定 primary comparisons；不能在最终稿中删除这条假设。

所有 CP 结论均条件于固定 artifacts/predictors、冻结 mean operation clock 和声明的 ideal simulator streams。它们覆盖 declared complete mixtures，没有导出具体 aircraft subgroup、receipt-selected subset、faulty histories、unknown physical populations 或 route/mission 风险。当前 theory/discussion 维持此边界。

## 16 项固定 primary intervals

两 confirmation profiles ×四 contrasts ×loss/observation =16。Service 固定 standard；Full/Flat task 固定 union，allowance=.15。每项按 shared seed 的 paired difference 重采样 n=2048；family-adjusted tails 为 0.05/(2×16) 及其补数。下面合并显示同一 contrast 的两项区间；loss 单位为 10^-3 m²s，observation 为 percentage points，符号为前者减后者。

| Profile | Contrast | Δloss [family interval] | Δobservation [family interval] |
|---|---|---|---|
| Nominal | Full−ValidatedFlat | 0 [0,0] | 0 [0,0] |
| Nominal | KG1−FlatCART | 0 [0,0] | 0 [0,0] |
| Nominal | KG1−FlatRF | −2.180348 [−4.398294,−0.957409] | −1.660156 [−3.125000,−0.195313] |
| Nominal | KG1−Fixed2 | −2.168772 [−4.383710,−0.943986] | −1.660156 [−3.125000,−0.195313] |
| Unfitted | Full−ValidatedFlat | 0 [0,0] | 0 [0,0] |
| Unfitted | KG1−FlatCART | 0 [0,0] | 0 [0,0] |
| Unfitted | KG1−FlatRF | −2.512160 [−3.771350,−1.368251] | −1.171875 [−2.294922,−0.097656] |
| Unfitted | KG1−Fixed2 | −2.514379 [−3.773458,−1.371696] | −1.171875 [−2.294922,−0.097656] |

全部 mean、pointwise 与 family endpoints 独立复算一致。它们是 approximate percentile intervals；Bonferroni 调整不会使每个 approximate bootstrap interval 自动成为有限样本 exact theorem。32000 resamples 在每个 family tail 约对应 50 个 replicate，有 Monte Carlo 与 lattice resolution；当前稿没有把它们混同 exact CP。零区间表示此次 empirical differences 为零，不能从退化 bootstrap 单独推出对任意新实现/总体的全等价或 noninferiority 定理。当前文字说 all reported canonical outcomes identical，符合实证与非干扰结构。

## 公平资源、拒绝和不利结果

Full 与 TaskAwareFlatValidated 使用相同 22-catalogue、真实 cards、固定 objective、request、allowance、service load、budget、input、price 与数值服务；selector/validator/history latch 独立实现。不是拿 trajectory-only 或 stripped checker 作为完整同任务主对照。全部 65536 shared contexts 的两端数字、events、admission、chosen policy、source_claims 精确相同；36 route Full/Flat raw trace/capture pairs 也精确相同。

实际 integrated refusal executions 为 **57344**（包括两 validators）。它们始终在各 context 的 n=2048 中，保留 prior，observation/union failure=1、capture_success=0、installed=0、没有 receipt。其误差与 costs 没有通过 conditional admission filtering 消失。

独立重算 any-receipt 与 all-requested-event coverage。两者在当前 64 variant contexts 中恰好数值相同，但定义确实分离；不能因此删除后者。标准 union 的 nominal 覆盖 2048/2048，unfitted 为 2047/2048；coverage 表示执行期间每个 requested event 至少有一个有效 issued receipt，不代表期末持续有效、receipt-conditioned risk 或该 scan 必然精确。一个无 attachable version 的 unfitted source 已保留。

KG1 对 Fixed2 的 nominal loss 从 0.0138329002 降到 0.0116641278 m²s：15.6784% reduction，work 增加16.0864%；unfitted 从0.0199378194到0.0174234407：12.6111%，work 增加16.0749%。FlatCART 精确得到这些同样的数值/事件结果。

不利 evidence 完整：profile predicate 虽触发但 numerical ablation 为零；contended time screen 可增加 loss；tight cap 使额外 predicate 冗余；Fixed4/Final 有更低 mean loss 的行；ordinary routes 有 Fixed2 占优；四 unsupported stresses 均保留，map-shift 高 union failure 可见。72 influence rows 与全部原始 n 一致：nominal KG1−Fixed2 为442 improved /374 worsened /1232 tied，top-two 占净 gain 27.9944%；unfitted 458/366/1224、10.0172%。Top-two deletion 仅描述性，没有删除 primary observations 或据此重算确认主结论。

Actual-F1-card fault table 含16 invalid+2 normal constructed cases。Incorrect attachments 为16/4/2/0/0（stripped/matching/current/history/validated procedural），两 normal controls 均通过。V3 强 control 亦为零。这里没有随机 fault sampling，不给“0%真实故障风险”、CP rate、额外 independent n 或 graph 独有能力。

## Route、provider 和计时边界

432 route rows 均从 archived 6000-tick trace 与299-opportunity capture arrays 复算，RMSE/p95/p99/max/loss/failure/capture counts 与 CSV/JSON 一致；全部 route authorized_episode_cards=0。相同 source 后续依赖版本与 route ticks 相关，不能转用 episode CP 或把72 simulated execution-hours当成72独立 mission observations。

四 realizations/geometry/condition 的 noise/shape settings 由 rep 预设，并非同分布 replicate mixture。它们具有独立 stochastic perturbations；报告均值、各配对差值是描述性的。SI 明确异质性，不进行基于4同分布route samples的正式推广推断；预定 unfitted/contention/rep0 diagnostic 没有按结果择优。

Provider 审核两项 route input×lazy/hydrated 各一次。输入整文件、全部 trace/capture arrays、非CPU jobs/work/events 相同。原 lazy archive 访问可大幅污染 timer（fixture18.399s vs2.401s，另一fixture13.849s vs2.033s）；这些是边界修正证据，不是算法加速。36 input hashes、4 worker manifests/executor/provider/F1 hashes一致，432 archived numeric results完整。当前 route online CPU 范围1.752–3.534s/600-s模拟route，startup与archive hydration另记。

三个 CPU ledgers 保持分离：controlled 共用已执行 native retained prefix 与逐方法 components；V3 inclusive replay 包含 offline truth assertion/scoring；route direct_online_cpu 是整段在线循环，包含实际数组取用/拷贝、前端、ICP/features、forecast、dispatch、checks、replay和coordinator，排除 raycasting/archive/truth scoring。Operation clock 是另一个固定平均操作成本 service convention，不是这些 measured process-CPU 的新拟合，也不是 embedded/WCET budget。新增 observer CPU 未进入 availability/event map。

Integrated driver 固定先 Full 后 Flat。因此小的 native CPU 差值可能受缓存/执行顺序影响，不能声称严格硬件 superiority 或将几十微秒变成 causal performance finding。当前正文只报告 measured costs，并未将这一差值纳入16项 efficacy family。继续维持此处理即可。

## 缺陷—证据—修改—最终复核

| 本轮发现/复核 | 证据 | 修改或处理 | 最终状态 |
|---|---|---|---|
| 32“primary contexts”易与16 primary intervals 混淆 | 原 main/SI request wording | 改为32 primary-allowance (0.15) contexts | 已读到 main 与 SI 更新；16CI/32requests 不混用 |
| Stress/full-tail 完整结果位置指向过宽 | 原 prose 声称全部在 supplement，完整每method/service字段在release CSV | 明确 complete all-method/service / full tail 在 release CSVs | 已读到 generated main 更新；原始结果无变化 |
| Coverage 仅“authorized receipt”易误读持续有效 | 原概括及 any vs all 字段 | 明确 during execution、每requested event至少一次有效issued receipt；analyze保留any与all | 字段和 main task-table定义已独立复核；本数据两指标相同 |
| 同 scope latch/reset、V2 driver/timer过渡 | 保留v1/v2与上一轮独立软件实证 | 最终V3 persistent scope、分别计CPU、binder/resume gates | 最终四components与audit hashes一致；canonical receipt equality通过 |
| 原 route-absence gate glob错误 | 保留原source/inventory及actual generation ledger | 保留错误记录、修正未来glob、用真实chronology验证本轮 | 已复核；不依靠错误PASS认定absence |
| 两条index缺失与CPU metadata来源 | 8602046/47 originals、recovery audit | unchangedcollector原seed恢复，公开CPU为新测 | 15数组/整文件hash相同；全部denominators恢复 |
| Random2or4 iid条件 | deterministic seed coin与heterogeneous-cap条件化 | theory已显式声明ideal independent coin模型和另一解释需不同bound | 已复读第25–30行；属于条件假设，未证明具体SHA独立性 |
| Provider lazy timing混入归档解压 | 两paired fixtures及完整trace/非CPU相等 | versioned prehydration、分开startup/archive/online CPU | 独立array/JSON复核通过；numerical F0未改 |

剩余 Minor 建议：SI integrated-table caption 也可重复一句“执行期间每事件至少一次有效 issued receipt”，使单独阅读SI时定义完整；`preconfirmation_gate_correction.json` 的26个route files是当时修正快照，宜在最终说明中明确其观察时点，避免把字段 `currently_present` 解读为最终 inventory（本轮实际为36）。这些不改变方法、计数、风险卡或选择，不要求重做试验。

**最终：本轮统计审查通过，建议 Minor Revision；真实评分8.5/10。所有核心数值独立复核一致，未发现删失失败、虚增独立样本、按确认结果改选或失配主对照。** 有效性限定于已披露的固定模拟总体、随机化假设和service-clock模型；最终出版文字应持续保留这些条件与null/adverse结果。

## 末次文字闭合复核（2026-10-11）

仅复核上列两项剩余 Minor 文字建议，没有重复全量数值复算，也未修改评分锚、源码、数据或冻结记录。

- `source/r8_results_author.py` 第194行及生成的 `sections/r8_supplement_results.tex` 第530行均已明确：Coverage requires at least one valid issued receipt during execution for each requested event. 该定义完整保留执行期间、至少一次有效签发和每个请求事件三个条件；SI单独阅读时也与已复核的 all-requested coverage 指标一致。
- `sections/r8_supplement_protocol.tex` 第27行已明确，gate-correction note 的26个route files是 later correction made 时的进度快照，不是 preconfirmation 或 final inventory，并明示 final release contains all 36。原 correction JSON 作为历史观察记录保留，最终说明不会再把 `currently_present` 误读为最终数量。

**两项文字建议均闭合。统计严谨性评分仍为8.5/10，第三轮建议仍为 Minor Revision；本报告没有待完成的具体修订项。** 前述方法条件、描述性证据边界与未量化的工程收益仍是评分依据，不能因文字闭合而提升为 Strong Accept。

