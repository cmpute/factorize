# Factorization in pure Rust
A natively cross-platform and fast factorization utility written in pure Rust.

## Goals
- Support output in Math format (e.g. `2^3 * 3^2`), core-utils format (e.g. `2 2 2 3 3`), json format (`{factors: {2:3, 3:2}, complete: true, residue: nil }`).
- Support output diagnosis information to stderr (such as total time, expected time)
- Support parallel factorization (enable by default)
- Support set timeout (for large target), and report the partial result (unfactorized part will be marked)
- Main benchmark: coreutils/factor (C), uutils/factor (`uu_factor` crate), primefac (Python), Pari/GP, SageMath, [YAFU](https://github.com/bbuhrow/yafu), Cado-NFS
