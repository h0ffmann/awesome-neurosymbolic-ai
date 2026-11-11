<!--
  GENERATED FILE - do not edit directly.
  Source of truth: README.base.md (edit that file in pull requests).
  Built by scripts/build_readme.py via .github/workflows/stats.yml.
-->
<div align="center">

<picture>
	<source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.png">
	<img alt="A neural network flowing into the universal quantifier, drawn from Desmos equations, by @h0ffmann" src="assets/banner-light.png" width="820">
</picture>

# Awesome Neurosymbolic AI [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

<sub>∀ · <i>for all</i> · <a href="assets/README.md">the drawing</a> · <a href="assets/banner.desmos.json">its Desmos equations</a> · <a href="scripts/draw_banner.py">the pen</a> · <a href="#contents">contents</a> · <a href="contributing.md">contribute</a></sub>

[![lint](https://github.com/h0ffmann/awesome-neurosymbolic-ai/actions/workflows/lint.yml/badge.svg)](https://github.com/h0ffmann/awesome-neurosymbolic-ai/actions/workflows/lint.yml)
[![links](https://github.com/h0ffmann/awesome-neurosymbolic-ai/actions/workflows/links.yml/badge.svg)](https://github.com/h0ffmann/awesome-neurosymbolic-ai/actions/workflows/links.yml)
[![metrics](https://github.com/h0ffmann/awesome-neurosymbolic-ai/actions/workflows/stats.yml/badge.svg)](https://github.com/h0ffmann/awesome-neurosymbolic-ai/actions/workflows/stats.yml)
[![license: CC0-1.0](https://img.shields.io/badge/license-CC0--1.0-6e40c9?style=flat-square)](license)
[![stars](https://img.shields.io/github/stars/h0ffmann/awesome-neurosymbolic-ai?style=flat-square&color=6e40c9)](https://github.com/h0ffmann/awesome-neurosymbolic-ai/stargazers)

</div>

> Frameworks, reasoners, papers, courses, and benchmarks for neurosymbolic AI — systems that combine neural learning with symbolic reasoning.

Neurosymbolic AI pairs the perception, flexibility, and scale of neural networks with the compositionality, data efficiency, interpretability, and formal guarantees of symbolic methods such as logic programming, constraint solving, theorem proving, and knowledge representation. This list covers both the integration layer (neurosymbolic frameworks proper) and the mature symbolic foundations those systems build on.

Entries are curated: each one is maintained, documented, and useful in practice or foundational in the literature. Read the contribution guidelines (linked at the bottom) before suggesting an addition.

## Contents

- [Rankings](#rankings)
- [Neurosymbolic Frameworks](#neurosymbolic-frameworks)
- [Symbolic Foundations](#symbolic-foundations)
	- [Solvers and Provers](#solvers-and-provers)
	- [Logic Programming](#logic-programming)
	- [Knowledge Representation](#knowledge-representation)
	- [Planning](#planning)
- [LLMs and Symbolic Reasoning](#llms-and-symbolic-reasoning)
- [Papers](#papers)
	- [Surveys](#surveys)
	- [Landmark Papers](#landmark-papers)
- [Books](#books)
- [Courses and Tutorials](#courses-and-tutorials)
- [Benchmarks and Datasets](#benchmarks-and-datasets)
- [Community](#community)
- [Contributing](#contributing)

## Rankings

Generated from the list's own entries and their live metrics: the ten most starred repositories on each side of the neural–symbolic bridge, refreshed weekly.

### Top 10 neurosymbolic AI repositories

| # | Repository | ⭐ Stars | Created | Last commit |
|---:|---|---:|---|---|
| 1 | [GraphRAG](https://github.com/microsoft/graphrag) | 36,627 | 2024-03 | 2026-11-02 |
| 2 | [cognee](https://github.com/topoteretes/cognee) | 33,237 | 2023-08 | 2026-11-06 |
| 3 | [Graphiti](https://github.com/getzep/graphiti) | 32,741 | 2024-08 | 2026-11-11 |
| 4 | [Guidance](https://github.com/guidance-ai/guidance) | 21,820 | 2022-11 | 2026-05-21 |
| 5 | [XERJ](https://github.com/xerj-org/xerj) | 18,815 | 2026-06 | 2026-11-09 |
| 6 | [Outlines](https://github.com/dottxt-ai/outlines) | 16,007 | 2023-03 | 2026-08-24 |
| 7 | [AlphaGeometry](https://github.com/google-deepmind/alphageometry) | 4,903 | 2023-10 | 2026-01-05 |
| 8 | [SymbolicAI](https://github.com/ExtensityAI/symbolicai) | 1,781 | 2022-11 | 2026-10-22 |
| 9 | [LeanDojo](https://github.com/lean-dojo/LeanDojo) | 852 | 2023-06 | 2026-01-18 |
| 10 | [Nucleoid](https://github.com/NucleoidAI/Nucleoid) | 770 | 2021-07 | 2026-11-11 |

### Top 10 symbolic AI repositories

| # | Repository | ⭐ Stars | Created | Last commit |
|---:|---|---:|---|---|
| 1 | [OR-Tools](https://github.com/google/or-tools) | 14,362 | 2015-02 | 2026-09-17 |
| 2 | [Z3](https://github.com/Z3Prover/z3) | 12,914 | 2015-03 | 2026-11-10 |
| 3 | [Lean 4](https://github.com/leanprover/lean4) | 9,958 | 2018-04 | 2026-11-11 |
| 4 | [RDFLib](https://github.com/RDFLib/rdflib) | 2,551 | 2012-02 | 2026-11-02 |
| 5 | [Scryer Prolog](https://github.com/mthom/scryer-prolog) | 2,470 | 2016-10 | 2026-10-22 |
| 6 | [Protégé](https://github.com/protegeproject/protege) | 1,643 | 2013-08 | 2026-09-23 |
| 7 | [cvc5](https://github.com/cvc5/cvc5) | 1,389 | 2012-12 | 2026-11-10 |
| 8 | [Soufflé](https://github.com/souffle-lang/souffle) | 1,194 | 2016-03 | 2026-10-31 |
| 9 | [OWL API](https://github.com/owlcs/owlapi) | 945 | 2013-02 | 2026-11-02 |
| 10 | [Clingo](https://github.com/potassco/clingo) | 861 | 2016-05 | 2026-11-03 |

## Neurosymbolic Frameworks

Languages and libraries whose core purpose is integrating neural networks with symbolic reasoning.

| Project | Description | ⭐ Stars | Created | Contributors | Last commit | Commits in 2026 |
|---|---|---:|---|---:|---|---:|
| [Scallop](https://github.com/scallop-lang/scallop) | Neurosymbolic programming language based on Datalog, with differentiable reasoning built on provenance semirings and tunable reasoning granularity. | 526 | 2022-07 | 6 | 2026-06-26 | 3 |
| [DeepProbLog](https://github.com/ML-KULeuven/deepproblog) | Neural probabilistic logic programming that extends ProbLog with neural predicates, from KU Leuven. | 362 | 2021-06 | 4 | 2026-09-29 | 9 |
| [ABLkit](https://github.com/AbductiveLearning/ABLkit) | Toolkit for Abductive Learning, which bridges machine learning and logical abduction, from Nanjing University's LAMDA group. | 102 | 2022-02 | 6 | 2026-10-25 | 40 |
| [DomiKnowS](https://github.com/HLR/DomiKnowS) | Declarative Python/PyTorch framework for integrating logical domain knowledge as constraints into deep learning, with ILP-based inference. | 55 | 2019-03 | 16 | 2026-09-04 | 406 |
| [LTNtorch](https://github.com/tommasocarraro/LTNtorch) | PyTorch implementation of Logic Tensor Networks, which ground first-order fuzzy logic into tensor computations for learning with logical constraints. | 164 | 2021-11 | 1 | 2024-10-02 | 0 |
| [Logic Tensor Networks](https://github.com/logictensornetworks/logictensornetworks) | Original TensorFlow implementation of Logic Tensor Networks (Real Logic). | 376 | 2018-07 | 5 | 2026-11-07 | 16 |
| [LNN](https://github.com/IBM/LNN) | IBM's Logical Neural Networks, where every neuron represents a component of a weighted real-valued logic formula, supporting omnidirectional inference. | 337 | 2021-11 | 14 | 2026-09-09 | 15 |
| [NeurASP](https://github.com/azreasoners/NeurASP) | Embraces neural network outputs as probabilistic atom facts in Answer Set Programming. | 58 | 2020-02 | 3 | 2026-11-08 | 8 |
| [PSL](https://github.com/linqs/psl) | Probabilistic Soft Logic, a mature framework for probabilistic reasoning over relational domains using hinge-loss Markov random fields; basis of the NeuPSL neurosymbolic extension. | 315 | 2011-07 | 20 | 2024-05-08 | 0 |
| [PyNeuraLogic](https://github.com/LukasZahradnik/PyNeuraLogic) | Differentiable relational logic templates that generalize and extend graph neural networks. | 315 | 2020-12 | 3 | 2026-10-22 | 101 |
| [PyReason](https://github.com/lab-v2/pyreason) | Explainable reasoning over graphs with open-world annotated logic, supporting temporal reasoning. | 355 | 2022-10 | 14 | 2026-10-26 | 220 |
| [dPASP](https://github.com/kamel-usp/dpasp) | Differentiable probabilistic answer set programming framework for neurosymbolic inference and learning. | 32 | 2022-06 | 2 | 2026-09-17 | 2 |
| [Vehicle](https://github.com/vehicle-lang/vehicle) | Specification language for neural networks that compiles one logical spec into a differentiable training loss, verifier queries, and Agda, Rocq, or Isabelle proofs. | 137 | 2021-02 | 27 | 2026-11-05 | 204 |

## Symbolic Foundations

Mature, production-grade symbolic engines. These are the reasoning backbones that neurosymbolic systems (and LLM + solver pipelines) call into.

### Solvers and Provers

| Project | Description | ⭐ Stars | Created | Contributors | Last commit | Commits in 2026 |
|---|---|---:|---|---:|---|---:|
| [Z3](https://github.com/Z3Prover/z3) | Microsoft Research's SMT solver, the workhorse of program verification, symbolic execution, and constraint solving. | 12,914 | 2015-03 | 351 | 2026-11-10 | 3,095 |
| [cvc5](https://github.com/cvc5/cvc5) | Industrial-strength open-source SMT solver with strong theory support and proof production. | 1,389 | 2012-12 | 103 | 2026-11-10 | 588 |
| [Kissat](https://github.com/arminbiere/kissat) | State-of-the-art SAT solver by Armin Biere, a reference implementation in modern CDCL solving. | 685 | 2020-05 | 3 | 2025-10-16 | 0 |
| [Vampire](https://github.com/vprover/vampire) | Award-winning automated theorem prover for first-order logic. | 449 | 2014-03 | 35 | 2026-11-10 | 905 |
| [E Prover](https://github.com/eprover/eprover) | High-performance theorem prover for full first-order logic with equality. | 174 | 2016-11 | 10 | 2026-11-11 | 208 |
| [Lean 4](https://github.com/leanprover/lean4) | Interactive theorem prover and dependently-typed programming language, with the community-maintained [Mathlib](https://github.com/leanprover-community/mathlib4) mathematical library. | 9,958 | 2018-04 | 295 | 2026-11-11 | 2,931 |
| [Isabelle](https://isabelle.in.tum.de) | Generic proof assistant with the large Archive of Formal Proofs ecosystem. | — | — | — | — | — |
| [Rocq](https://rocq-prover.org) | Interactive theorem prover based on the calculus of inductive constructions, formerly known as Coq. | — | — | — | — | — |
| [OR-Tools](https://github.com/google/or-tools) | Google's operations research suite, including the award-winning CP-SAT constraint programming solver. | 14,362 | 2015-02 | 149 | 2026-09-17 | 41 |
| [MiniZinc](https://www.minizinc.org) | Solver-independent constraint modeling language, the lingua franca of constraint programming. | — | — | — | — | — |

### Logic Programming

| Project | Description | ⭐ Stars | Created | Contributors | Last commit | Commits in 2026 |
|---|---|---:|---|---:|---|---:|
| [SWI-Prolog](https://www.swi-prolog.org) | The most widely used open-source Prolog system, actively maintained for decades. | — | — | — | — | — |
| [Scryer Prolog](https://github.com/mthom/scryer-prolog) | Modern ISO-conforming Prolog implemented in Rust. | 2,470 | 2016-10 | 56 | 2026-10-22 | 287 |
| [Clingo](https://github.com/potassco/clingo) | The standard Answer Set Programming system from the Potassco project. | 861 | 2016-05 | 22 | 2026-11-03 | 44 |
| [ProbLog](https://github.com/ML-KULeuven/problog) | Probabilistic logic programming language and engine, the symbolic substrate of DeepProbLog. | 430 | 2019-05 | 17 | 2026-09-14 | 52 |
| [Soufflé](https://github.com/souffle-lang/souffle) | High-performance Datalog engine that compiles to parallel C++, used in static analysis at scale. | 1,194 | 2016-03 | 99 | 2026-10-31 | 21 |
| [miniKanren](https://minikanren.org) | Family of embeddable relational programming languages with implementations in dozens of host languages. | — | — | — | — | — |

### Knowledge Representation

| Project | Description | ⭐ Stars | Created | Contributors | Last commit | Commits in 2026 |
|---|---|---:|---|---:|---|---:|
| [Protégé](https://github.com/protegeproject/protege) | The standard open-source ontology editor for OWL, from Stanford. | 1,643 | 2013-08 | 38 | 2026-09-23 | 30 |
| [ELK](https://github.com/liveontologies/elk-reasoner) | Very fast OWL EL reasoner used with large biomedical ontologies such as SNOMED CT. | 129 | 2015-10 | 9 | 2024-07-11 | 0 |
| [Apache Jena](https://jena.apache.org) | Java framework for building Semantic Web and linked data applications with RDF, SPARQL, and OWL. | — | — | — | — | — |
| [RDFLib](https://github.com/RDFLib/rdflib) | Pure-Python library for working with RDF, SPARQL, and serialization formats. | 2,551 | 2012-02 | 203 | 2026-11-02 | 128 |
| [OWL API](https://github.com/owlcs/owlapi) | Reference Java API for creating and manipulating OWL ontologies. | 945 | 2013-02 | 34 | 2026-11-02 | 8 |
| [mOWL](https://github.com/bio-ontology-research-group/mowl) | Python library for machine learning with ontologies, embedding OWL knowledge into vector spaces. | 97 | 2020-03 | 11 | 2026-09-10 | 100 |

### Planning

- [Fast Downward](https://github.com/aibasel/downward) - The reference classical planning system built on heuristic search. ⭐ 410 · created 2019-06 · 26 contributors · last commit 2026-11-09 · 58 commits in 2026.
- [Unified Planning](https://github.com/aiplan4eu/unified-planning) - Python API providing a single interface to many planning engines, from the AIPlan4EU project. ⭐ 330 · created 2021-03 · 39 contributors · last commit 2026-11-10 · 765 commits in 2026.
- [Planning.wiki](https://planning.wiki) - Community guide to PDDL and automated planning tools.

## LLMs and Symbolic Reasoning

Where most practical adoption is happening today: pairing large language models with symbolic engines that check, constrain, or execute their outputs — and grounding them in structured, curated knowledge.

| Project | Description | ⭐ Stars | Created | Contributors | Last commit | Commits in 2026 |
|---|---|---:|---|---:|---|---:|
| [SynaLinks](https://github.com/SynaLinks/synalinks) | Keras-inspired framework for building neurosymbolic language-model applications with knowledge graphs and constrained structured output. | 465 | 2025-02 | 10 | 2026-11-09 | 426 |
| [SymbolicAI](https://github.com/ExtensityAI/symbolicai) | Compositional differentiable programming library that treats LLMs as semantic parsers embedded in a symbolic framework. | 1,781 | 2022-11 | 14 | 2026-10-22 | 251 |
| [LeanDojo](https://github.com/lean-dojo/LeanDojo) | Open toolkit for interacting with Lean, including retrieval-augmented LLM-based theorem proving. | 852 | 2023-06 | 18 | 2026-01-18 | 1 |
| [AlphaGeometry](https://github.com/google-deepmind/alphageometry) | DeepMind's neurosymbolic system combining a language model with a symbolic deduction engine, reaching olympiad-level geometry. | 4,903 | 2023-10 | 1 | 2026-01-05 | 1 |
| [Outlines](https://github.com/dottxt-ai/outlines) | Constrained text generation that guarantees LLM outputs conform to regular expressions, grammars, or JSON schemas via finite-state machines. | 16,007 | 2023-03 | 179 | 2026-08-24 | 164 |
| [Guidance](https://github.com/guidance-ai/guidance) | Programming paradigm for steering LLMs with grammars, regular expressions, and control flow, with guaranteed output structure. | 21,820 | 2022-11 | 79 | 2026-05-21 | 25 |
| [Nucleoid](https://github.com/NucleoidAI/Nucleoid) | Declarative logic runtime that accumulates statements into an adaptive logic graph, positioned as neurosymbolic infrastructure for world models. | 770 | 2021-07 | 5 | 2026-11-11 | 496 |
| [XERJ](https://github.com/xerj-org/xerj) | Local-first AI search engine and MCP server in one Rust binary: BM25, vector, and hybrid search for agent memory and RAG, with Corpus Hub serving pinned reference corpora as ground truth. | 18,815 | 2026-06 | 120 | 2026-11-09 | 4,176 |
| [GraphRAG](https://github.com/microsoft/graphrag) | Microsoft's modular graph-based RAG: an LLM extracts a knowledge graph from documents, and queries reason over its structure rather than raw chunks. | 36,627 | 2024-03 | 51 | 2026-11-02 | 84 |
| [Graphiti](https://github.com/getzep/graphiti) | Builds real-time, temporally aware knowledge graphs that serve as queryable memory for AI agents, from Zep. | 32,741 | 2024-08 | 64 | 2026-11-11 | 346 |
| [cognee](https://github.com/topoteretes/cognee) | Open-source memory platform for agents that turns data into a knowledge graph combined with vector search. | 33,237 | 2023-08 | 302 | 2026-11-06 | 7,566 |

## Papers

> [!TIP]
> **📌 Curated pick:** [Neuro-Symbolic Frameworks: Conceptual Characterization and Empirical Comparative Analysis](https://neurosymbolic-ai-journal.com/system/files/nai-paper-924_0.pdf) (Sinha, Premsri, Kamali and Kordjamshidi — Neurosymbolic Artificial Intelligence journal, 2026).
> A conceptual characterization and head-to-head empirical comparison of NeSy frameworks, including DomiKnowS, DeepProbLog, and Scallop — the best single read before choosing a framework from this list.

### Surveys

- [Neurosymbolic AI: The 3rd Wave](https://arxiv.org/abs/2012.05876) - Garcez and Lamb's influential position paper framing the modern neurosymbolic agenda (2020).
- [The Next Decade in AI: Four Steps Towards Robust Artificial Intelligence](https://arxiv.org/abs/2002.06177) - Gary Marcus's hybrid-AI manifesto: robust AI needs hybrid neurosymbolic architectures, large-scale knowledge, explicit reasoning, and cognitive models (2020).
- [Neurosymbolic AI — Why, What, and How](https://arxiv.org/abs/2305.00813) - Concise introduction by Sheth, Roy, and Gaur (2023).
- [From Statistical Relational to Neurosymbolic Artificial Intelligence: A Survey](https://arxiv.org/abs/2108.11451) - Marra et al. connect neurosymbolic AI to its statistical relational learning roots (2021).
- [Neuro-Symbolic AI and Its Taxonomy: A Survey](https://arxiv.org/abs/2305.08876) - Systematic taxonomy of integration patterns (2023).
- [Survey on Applications of Neurosymbolic Artificial Intelligence](https://arxiv.org/abs/2209.12618) - Application-focused view of the field (2022).
- [Neurosymbolic AI for Reasoning Over Knowledge Graphs: A Survey](https://doi.org/10.1109/TNNLS.2024.3420218) - DeLong, Mir, and Fleuriot's IEEE TNNLS survey of neurosymbolic reasoning on graphs (2024).
- [Neurosymbolic Programming](https://www.nowpublishers.com/article/Details/PGL-049) - Chaudhuri et al.'s Foundations and Trends monograph treating neurosymbolic systems as a programming languages problem (2021).

### Landmark Papers

- [Harnessing Deep Neural Networks with Logic Rules](https://arxiv.org/abs/1603.06318) - Hu et al. distill logic rules into network weights via posterior regularization (2016).
- [End-to-End Differentiable Proving](https://arxiv.org/abs/1705.11040) - Rocktäschel and Riedel's Neural Theorem Provers over knowledge bases (2017).
- [A Semantic Loss Function for Deep Learning with Symbolic Knowledge](https://arxiv.org/abs/1711.11157) - Xu et al. turn logical constraints into a differentiable loss via knowledge compilation (2018).
- [DeepProbLog: Neural Probabilistic Logic Programming](https://arxiv.org/abs/1805.10872) - Manhaeve et al. introduce neural predicates in probabilistic logic programs (2018).
- [The Neuro-Symbolic Concept Learner](https://arxiv.org/abs/1904.12584) - Mao et al. learn visual concepts, words, and semantic parsing without explicit supervision (2019).
- [SATNet: Bridging Deep Learning and Logical Reasoning](https://arxiv.org/abs/1905.12149) - Wang et al. embed a differentiable MAXSAT solver in neural networks (2019).
- [Logic-LM: Empowering Large Language Models with Symbolic Solvers](https://arxiv.org/abs/2305.12295) - Pan et al. parse problems with an LLM and offload the reasoning to Prolog, Z3, and Pyke (2023).

## Books

- [Neuro-Symbolic Artificial Intelligence: The State of the Art](https://ebooks.iospress.nl/volume/neuro-symbolic-artificial-intelligence-the-state-of-the-art) - Edited volume by Hitzler and Sarker surveying the field's main threads (IOS Press, 2021).
- [Compendium of Neurosymbolic Artificial Intelligence](https://ebooks.iospress.nl/volume/compendium-of-neurosymbolic-artificial-intelligence) - Follow-up edited volume collecting extended versions of recent key papers (IOS Press, 2023).

## Courses and Tutorials

- [Summer School on Neurosymbolic Programming](https://www.neurosymbolic.org) - Annual summer school with recorded lectures from leading researchers.
- [IBM Neuro-Symbolic AI Toolkit](https://ibm.github.io/neuro-symbolic-ai) - Entry point to IBM's neurosymbolic projects, papers, and demos.

## Benchmarks and Datasets

- [CLEVR](https://github.com/facebookresearch/clevr-dataset-gen) - Diagnostic dataset for compositional visual reasoning, the classic testbed for neurosymbolic VQA. ⭐ 653 · created 2017-07 · 1 contributors · last commit 2019-03-22 · 0 commits in 2026.
- [FOLIO](https://github.com/Yale-LILY/FOLIO) - First-order logic reasoning benchmark with natural language annotated by logicians. ⭐ 148 · created 2022-09 · 1 contributors · last commit 2023-12-22 · 0 commits in 2026.
- [ProofWriter](https://allenai.org/data/proofwriter) - Datasets of entailment trees for rule-based reasoning over natural language from AI2.
- [ARC-AGI](https://github.com/fchollet/ARC-AGI) - Chollet's Abstraction and Reasoning Corpus, a benchmark of core-knowledge program induction tasks. ⭐ 4,855 · created 2019-11 · 21 contributors · last commit 2025-04-04 · 0 commits in 2026.
- [rsbench](https://unitn-sml.github.io/rsbench) - Suite for systematically evaluating reasoning shortcuts in neurosymbolic models.

## Community

- [Neurosymbolic Artificial Intelligence Journal](https://neurosymbolic-ai-journal.com) - Open-access journal dedicated to the field, with an open and transparent review process.
- [Neural-Symbolic Learning and Reasoning Association](https://neural-symbolic.org) - Home of the long-running NeSy conference series, held since 2005.

## Related Lists

- [Awesome LLM Reasoning with NeSy](https://github.com/LAMDA-NeSy/Awesome-LLM-Reasoning-with-NeSy) - Paper-centric list on neurosymbolic learning in the LLM era, from the LAMDA NeSy group. ⭐ 334 · created 2024-10 · 1 contributors · last commit 2025-06-19 · 0 commits in 2026.
- [Awesome Neurosymbolic AI (benchmarks)](https://github.com/sciknoworg/awesome-neurosymbolic-ai) - Catalog of benchmarks, datasets, and evaluation resources. ⭐ 8 · created 2026-06 · 0 contributors · last commit 2026-06-17 · 9 commits in 2026.
- [Awesome Neurosymbolic Computer Vision](https://github.com/marcionicolau/awesome-neurosymbolic-cv) - Companion list to a neurosymbolic computer vision survey. ⭐ 0 · created 2024-01 · 1 contributors · last commit 2024-01-10 · 0 commits in 2026.
- [NeSymGraphs](https://github.com/NeSymGraphs) - GitHub organization collecting implementations from a survey on neurosymbolic reasoning over knowledge graphs.

## Contributing

Contributions are welcome! Please read the [contribution guidelines](contributing.md) first, then open a pull request. One entry per pull request keeps reviews fast.
