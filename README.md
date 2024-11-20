## Schwartz Zippel Lemma

**References:** PAZK Ch. 3

Given:

1.  a field F
2.  a set S ⊆ F
3.  p an `m`-variate non-zero polynomial of degree at most `d` over `F`

Then `Pr_{x∈S^m}[p(x)=0] <= d/|S|`.

Corollary 1: Given two `m`-variate polynomials `q` and `r` of degree at most `d` over `F` where `q != r`, `q` and `r` agree on at most `d` points.

To show this, assume `q` and `r` agree on `k > d` points towards a contradiction.
Then the polynomial `p(x)=q(x)-r(x)` will be a polynomial of degree at most `d` with `k` roots.
Thus, the `Pr_{x∈F^m}[p(x)=0] = k/|F|` where `k/|F| > d/|F|`, contradicting Schwartz Zippel.

## Reed-Solomon Encoding

**References:** PAZK Ch. 2

Given:

1.  an alphabet `Σ` of size `q`,
2.  a `Σ`-message `m=(m_1,...,m_k)` of length `k`,
3.  a finite field `F` of size `|F|`,
4.  a vector of distinct F-elements `a=[a_1,...,a_n]` where `k < n <= |F|`

The Reed-Solomon encoding process then:

1.  computes a polynomial `p_m : F -> F`
2.  encodes `m` as length `n` vector `RS(m)=[p_m(a_1),...,p_m(a_n)]`

The polynomial `p_m` is defined in one of the following ways:

1.  Simple encoding
    
    Let symbols `m_1,...,m_k` be the coefficients of a degree `k-1` univariate polynomial `p_m(x) = Σ_{i=0}^{k-1} m_i*x^i`.

2.  Systematic encoding
    
    Let `p_m` be the univariate polynomial of maximum degree `k-1` defined via Lagrange interpolation such that for `1<=i<=k`, `p_m(a_i)=m_i`.

Note: Very commonly, the choice of points `a` is equal to `[0,...,|F|-1]`, i.e., an ordered vector of _all_ points in `F`.

## Univariate Low-Degree Extension (LDE)

Given a vector `a=(a_1,...,a_n)` in some field `F`, the  low-degree extension of `a` is a polynomial `f : F -> F` defined as follows:

Let `f` be the univariate Langrange interpolation of points `(0,a_1),...,(n-1,a_n)`.

By definition, `f` has max degree `n-1`.

**Note:** This is an instance of the systematic Reed-Solomon encoding, and the terms Reed-Solomon and LDE are conflated by some authors.

## Univariate Lagrange Interpolation

**References:** PAZK Ch. 2

Given points `(x_1,y_1),...,(x_n,y_k)` where `k>2` with distinct x-values, Langrange interpolation defines polynomial `p` of max degree `k-1` such that:

For each `1<=i<k`, let `p_m(a_i)=m_i`.

Then `p` is defined as the scaled sum of `k` Langrange basis polynomials as follows:

1.  Let the `j`-th Langrange basis polynomial be defined as:
    
    `l_j(x) = Π_{0<m<=k, m!=j} (x - x_m)/(x_j - x_m)`
    
    Note that the subscripted `x_j` and `x_m` refer to x-values of selected points while `x` is the independent variable of `l_j(x)`.

2.  Then let `p(x) = Σ_{j=0}^k y_j * l_j(x)`
    
    The above definition follows from the fact that `l_j(x_j) = 1` and for `0<m<=k` with `m!=j`, `l_j(x_m)=0`.

## Multi-linear Extension

**References:** PAZK Ch. 3

Given a function `f : {0,1}^k -> F`, we can consider its multilinear extension `f^ : F^k -> F` as follows:

`f^(x_1,...,x_k) = \sum_{ w∈{0,1}^k } f(w)*χ_w(x_1,...,x_k)`

where given `w = (b_1,...,b_k)`

`χ_w(x_1,...,x_k) = Π_{i=1}^k x_i*b_i + (1-x_i)*(1-b_i)`

Observe that each `χ_w()` function multiplies the ith variable logical-and'ed with the ith bit of `w`

Finally, observe that `f^(x_1,...,x_k)` is multi-linear with max degree `k`.
By multi-linear, we mean that `f^` has degree 1 when viewed a polynomial of a single independent variable `x_j` for some `1<=j<=k`.

## ZK Proof Techniques

gkr         fixed
circom r1cs arbitrary
air         algebraic intermediate representation - uses iops
iop         lower-level

## PAZK Exercises

### Ex 3.1

Original Freivald's algorithm:

1.  | r^0 r^1 ... r^{n-1} | --- this is a point that is input to a basis polynomial
2.  | a_0 a_1 ... a_{n-1} | --- these are the coefficients of the polynomial

Alternate view of (1),(2) --- as n field points and as n coefficients for each point
In this view, the n-variate polynomial has degree 1

### Ex 3.2

Bob and Alice want to verify their messages a and b of length n and with an alphabet size of m are identical.
Original Protocol:

Fix a prime field F of size p where |F| >> n, choose random r ∈ F, compute p_a(r) and p_b(r) and check they are equal

We want to show that the probability that of `p_a(r) = p_b(r)` when `p_a != p_b` is less than `1/n`.
To do so, we note that:

1.  `g(x) = p_a(x) - p_b(x)` is a polynomial of degree n-1
2.  `g(x) = 0` iff `p_a(x) = p_b(x)` for any x
3.  By Schwartz-Zippel, the probability of `Pr_{x∈F}[g(x) = 0] <= (n-1)/|F| = (n-1)/p`

If we enforce that `p > max{n^2,m}`, then we have that (2) holds with probability less than `(n-1)/n^2` or less than `1/n`

New Protocol:

For an alphabet size of m, we will need `ceil(log(m)) = floor(log(m-1))+1 = index_of_MSB(m-1)+1` bits to encode each symbol.
To simplify and without loss of generality, pick the least k such that m <= 2^k and increase m to 2^k (our alphabet will have extra unused symbols).
Thus, we will need `n*log(m)=n*k=log(m^n)=log(2^(n*k))` bits to encode the entire message.
So, we naturally have two functions:

`f_a,f_b : {0,1}^{n*k} -> {0,1}`

which correspond to the binary encoding of their messages.
Now, we compute the multilinear extension in a field F of the form:

`f^_a,f^_b : F^{n*k} -> F`

This polynomial will have degree `n*k`.
To ensure that possible error is less than `1/n*k`, we set our field size to `|F|=(n*k)^2`.
By Schwartz-Zippel, the polynomials will have equal values for an input when they are different with probability <= `n*k/|F|`.
Expanding that out, we have: `n*k/(n*k)^2` or `1/n*k`.

The communication cost in bits is equal to the bit cost of two field elements.
Since the field has size `(n*k)^2` and we need to send two elements, the total cost is `2*ceil(log((n*k)^2))=2*ceil(2*log(n*k))`.

### Ex 3.4

See the python file [mle.py](./mle.py).
