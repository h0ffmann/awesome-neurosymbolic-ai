# Neurosymbolic frameworks in Agda

[`NeSy.agda`](NeSy.agda) is a small, type-checked sketch of how to model a neurosymbolic framework in a dependently typed proof assistant:

| layer | in Agda |
|---|---|
| symbolic syntax | well-scoped first-order formulas as an inductive family `Fml Γ` (de Bruijn indices) |
| truth values | a `TruthAlg` record: Boolean logic and Logic Tensor Networks' product real logic are two instances |
| neural components | postulated networks (`mlp : Params → P → Vec Float 8 → Float`) used as atom groundings |
| semantics | a structural fold `⟦_⟧`, where `1 - ⟦ axioms ⟧` is the training loss |
| soundness | `sound`: if the truth algebras are related by a homomorphism and the groundings agree through it, the two semantics agree on every formula |

Some limits of this approach:

- Agda's `Float` has no usable equational theory, so proofs go over abstract algebras (or `ℚ`), and `Float` is used only to compute.
- Training happens outside Agda. To prove things about a *specific* trained network, postulate it and get those facts from an external verifier, as [Vehicle](https://github.com/vehicle-lang/vehicle)'s Agda backend does.
- Probabilistic systems in the DeepProbLog style fit the same pattern if you make `⟦_⟧` monadic over a distribution monad.

Check it with:

```sh
agda -i /path/to/agda-stdlib -i . NeSy.agda   # Agda 2.6.3, agda-stdlib 1.7.3
```

## Sources

- Badreddine, d'Avila Garcez, Serafini, Spranger. [Logic Tensor Networks](https://arxiv.org/abs/2012.13635). *Artificial Intelligence* 303, 2022. Source of the fuzzy operators and the p-mean-error aggregator.
- Ślusarz, Komendantskaya, Daggitt, Stewart, Stark. [Logic of Differentiable Logics: Towards a Uniform Semantics of DL](https://arxiv.org/abs/2303.10650). LPAR 2023. Source of the idea of one syntax with a parametric semantics for differentiable logics.
- Daggitt et al. [Vehicle](https://github.com/vehicle-lang/vehicle). Source of the approach of postulating networks and verifying them externally.
- van Krieken, Acar, van Harmelen. [Analyzing Differentiable Fuzzy Logic Operators](https://arxiv.org/abs/2002.06100). *Artificial Intelligence* 302, 2022.
- Manhaeve et al. [DeepProbLog: Neural Probabilistic Logic Programming](https://arxiv.org/abs/1805.10872). NeurIPS 2018.
