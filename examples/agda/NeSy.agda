------------------------------------------------------------------------
-- A neurosymbolic framework in Agda, in about 150 lines.
--
--   * symbolic layer : well-scoped first-order syntax (inductive types)
--   * truth values   : a parameter (Bool, fuzzy Float, ...)
--   * neural layer   : postulated networks, used as atom groundings
--   * semantics      : a structural fold; `1 - ⟦ axioms ⟧` is the loss
--   * soundness      : truth-algebra homomorphisms lift to whole formulas
--
-- Fuzzy operators follow Logic Tensor Networks (Badreddine et al., 2022,
-- https://arxiv.org/abs/2012.13635). Treating differentiable logics
-- uniformly, through one syntax and a parametric semantics, follows Ślusarz
-- et al., "Logic of Differentiable Logics" (LPAR 2023,
-- https://arxiv.org/abs/2303.10650). Postulating the network and leaving
-- facts about it to an external verifier is how Vehicle's Agda backend
-- works (https://github.com/vehicle-lang/vehicle).
--
-- Checked with Agda 2.6.3 and agda-stdlib 1.7.3:
--   agda -i /path/to/agda-stdlib -i . NeSy.agda
------------------------------------------------------------------------

module NeSy where

open import Data.Bool    using (Bool; true; false; _∧_; _∨_; not)
open import Data.Fin     using (Fin; zero; suc)
open import Data.Float   using (Float; _+_; _-_; _*_; _÷_; sqrt; fromℕ)
open import Data.List    using (List; []; _∷_; foldr; length; map)
open import Data.Nat     using (ℕ; zero; suc)
open import Data.Vec     using (Vec; []; _∷_; lookup)
  renaming (map to vmap)
open import Relation.Binary.PropositionalEquality
  using (_≡_; refl; cong; cong₂; trans; sym)

------------------------------------------------------------------------
-- 1. symbolic layer: signature and well-scoped formulas (de bruijn)

record Sig : Set₁ where
  field
    Pred  : Set
    arity : Pred → ℕ

module Syntax (S : Sig) where
  open Sig S

  infixr 5 _⇒_
  infixr 6 _∨′_
  infixr 7 _∧′_

  data Fml (Γ : ℕ) : Set where
    atom      : (p : Pred) → Vec (Fin Γ) (arity p) → Fml Γ
    _∧′_ _∨′_ _⇒_ : Fml Γ → Fml Γ → Fml Γ
    ¬′_       : Fml Γ → Fml Γ
    ∀′        : Fml (suc Γ) → Fml Γ

------------------------------------------------------------------------
-- 2. truth values as a parameter

record TruthAlg : Set₁ where
  field
    T           : Set
    _⊗_ _⊕_ _⇛_ : T → T → T      -- t-norm, t-conorm, implication
    ∼_          : T → T           -- negation
    ⨂           : List T → T      -- aggregator for ∀ (min, mean, p-mean, ...)

-- classical logic
𝔹 : TruthAlg
𝔹 = record
  { T   = Bool
  ; _⊗_ = _∧_
  ; _⊕_ = _∨_
  ; _⇛_ = λ a b → not a ∨ b
  ; ∼_  = not
  ; ⨂   = foldr _∧_ true
  }

-- logic tensor networks' "stable product" real logic, on Float
-- (product t-norm, probabilistic sum, reichenbach implication,
--  p-mean-error aggregator with p = 2)
LTN : TruthAlg
LTN = record
  { T   = Float
  ; _⊗_ = _*_
  ; _⊕_ = λ a b → a + b - a * b
  ; _⇛_ = λ a b → 1.0 - a + a * b
  ; ∼_  = λ a → 1.0 - a
  ; ⨂   = pME
  }
  where
  pME : List Float → Float
  pME [] = 1.0
  pME xs = 1.0 - sqrt (foldr (λ x acc → (1.0 - x) * (1.0 - x) + acc) 0.0 xs
                        ÷ fromℕ (length xs))

------------------------------------------------------------------------
-- 3 + 4. groundings and semantics (a structural fold)

module Semantics (S : Sig) (A : TruthAlg) {D : Set}
                 (G : (p : Sig.Pred S) → Vec D (Sig.arity S p) → TruthAlg.T A)
                 (batch : List D) where
  open Sig S
  open Syntax S
  open TruthAlg A

  mutual
    ⟦_⟧ : ∀ {Γ} → Fml Γ → Vec D Γ → T
    ⟦ atom p xs ⟧ ρ = G p (vmap (lookup ρ) xs)
    ⟦ φ ∧′ ψ ⟧    ρ = ⟦ φ ⟧ ρ ⊗ ⟦ ψ ⟧ ρ
    ⟦ φ ∨′ ψ ⟧    ρ = ⟦ φ ⟧ ρ ⊕ ⟦ ψ ⟧ ρ
    ⟦ φ ⇒ ψ ⟧     ρ = ⟦ φ ⟧ ρ ⇛ ⟦ ψ ⟧ ρ
    ⟦ ¬′ φ ⟧      ρ = ∼ ⟦ φ ⟧ ρ
    ⟦ ∀′ φ ⟧      ρ = ⨂ (inst φ ρ batch)

    -- ⟦ φ ⟧ at every element of the batch, written out so the
    -- termination checker sees φ shrink
    inst : ∀ {Γ} → Fml (suc Γ) → Vec D Γ → List D → List T
    inst φ ρ []       = []
    inst φ ρ (d ∷ ds) = ⟦ φ ⟧ (d ∷ ρ) ∷ inst φ ρ ds

------------------------------------------------------------------------
-- 5. soundness: a homomorphism of truth algebras, plus groundings that
--    agree through it, gives semantics that agree on every formula

record Hom (A B : TruthAlg) : Set where
  module A = TruthAlg A
  module B = TruthAlg B
  field
    h   : A.T → B.T
    h-⊗ : ∀ x y → h (x A.⊗ y) ≡ h x B.⊗ h y
    h-⊕ : ∀ x y → h (x A.⊕ y) ≡ h x B.⊕ h y
    h-⇛ : ∀ x y → h (x A.⇛ y) ≡ h x B.⇛ h y
    h-∼ : ∀ x   → h (A.∼ x)   ≡ B.∼ h x
    h-⨂ : ∀ xs  → h (A.⨂ xs)  ≡ B.⨂ (map h xs)

module Soundness (S : Sig) (A B : TruthAlg) (H : Hom A B) {D : Set}
                 (Gᴬ : (p : Sig.Pred S) → Vec D (Sig.arity S p) → TruthAlg.T A)
                 (Gᴮ : (p : Sig.Pred S) → Vec D (Sig.arity S p) → TruthAlg.T B)
                 (G-agree : ∀ p xs → Gᴮ p xs ≡ Hom.h H (Gᴬ p xs))
                 (batch : List D) where
  open Syntax S
  open Hom H
  module SA = Semantics S A Gᴬ batch
  module SB = Semantics S B Gᴮ batch

  mutual
    sound : ∀ {Γ} (φ : Fml Γ) (ρ : Vec D Γ) → SB.⟦ φ ⟧ ρ ≡ h (SA.⟦ φ ⟧ ρ)
    sound (atom p xs) ρ = G-agree p _
    sound (φ ∧′ ψ) ρ = trans (cong₂ B._⊗_ (sound φ ρ) (sound ψ ρ)) (sym (h-⊗ _ _))
    sound (φ ∨′ ψ) ρ = trans (cong₂ B._⊕_ (sound φ ρ) (sound ψ ρ)) (sym (h-⊕ _ _))
    sound (φ ⇒ ψ)  ρ = trans (cong₂ B._⇛_ (sound φ ρ) (sound ψ ρ)) (sym (h-⇛ _ _))
    sound (¬′ φ)   ρ = trans (cong B.∼_ (sound φ ρ)) (sym (h-∼ _))
    sound (∀′ φ)   ρ = trans (cong B.⨂ (sound-inst φ ρ batch)) (sym (h-⨂ _))

    sound-inst : ∀ {Γ} (φ : Fml (suc Γ)) (ρ : Vec D Γ) (ds : List D)
               → SB.inst φ ρ ds ≡ map h (SA.inst φ ρ ds)
    sound-inst φ ρ []       = refl
    sound-inst φ ρ (d ∷ ds) = cong₂ _∷_ (sound φ (d ∷ ρ)) (sound-inst φ ρ ds)

------------------------------------------------------------------------
-- example: "smokers get cancer", with a postulated network per predicate

data P : Set where smokes cancer : P

Smoking : Sig
Smoking = record { Pred = P ; arity = λ _ → 1 }

postulate
  Person : Set
  Params : Set
  θ      : Params
  embed  : Person → Vec Float 8
  mlp    : Params → P → Vec Float 8 → Float  -- trained outside Agda; outputs in [0,1]
  people : List Person                        -- the current batch

open Syntax Smoking

-- ∀x. smokes(x) ⇒ cancer(x)
axiom : Fml 0
axiom = ∀′ (atom smokes (zero ∷ []) ⇒ atom cancer (zero ∷ []))

groundLTN : (p : P) → Vec Person 1 → Float
groundLTN p (x ∷ []) = mlp θ p (embed x)

-- satisfaction of the knowledge base; training minimises 1 - sat
sat : Float
sat = Semantics.⟦_⟧ Smoking LTN groundLTN people axiom []
