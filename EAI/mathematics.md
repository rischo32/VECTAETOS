# Mathematical Foundation

## Encode V3

encode(a) = (I, S, V, T)

## Distance

d(aᵢ,aⱼ) = Σ |encode_k(aᵢ) - encode_k(aⱼ)|

## Curvature

Δ(i,j,k) =
d(i,j) + d(j,k) + d(k,i)

* ||(i→j→k→i)||

## Reconstruction

Rᵢⱼ = Σₖ orientation(i,j,k) · Δ(i,j,k)

R ∈ so(n)

## Spectral

λ = eigenvalues(R)

## κ

κ = distribúcia:

|| τ₁(τ₂(a)) - τ₂(τ₁(a)) ||

## Fingerprint

h = H(μ, A, QE, κ_signature, LTL)
