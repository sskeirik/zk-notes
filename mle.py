"""
This module:

1.  computes a multi-linear extension (MLE) g of some function f from binary words of length k to some prime field;
2.  takes a vector V of k points and computes g(V).

That is, given a prime field F and a function f : {0,1}^k -> F, this module computes an evaluator for a polynomial g : F^k -> F such that:

∀w∈{0,1}^k, f(w)=g(w)

where {0,1} are also interpreted as the additive and multiplicative identity elements in F.

The evaluator computes g(V) using dynamic programming in 0(n) space and time using the algorithm given by:

Victor Vu, Srinath T. V. Setty, Andrew J. Blumberg, and Michael Walfish.
A hybrid architecture for interactive verifiable computation.
In 2013 IEEE Symposium on Security and Privacy, SP 2013, Berkeley, CA, USA, May 19-22, 2013, pages 223–237.
IEEE Computer Society, 2013. 30, 31, 68

NOTE: This module is designed for educational purposes and is not production ready.
"""

from math import sqrt
import pathlib

def try_int(s):
    try: return int(s)
    except: return None

def read_lines(fpath):
    lines = pathlib.Path(fpath).read_text().split('\n')
    # remove redundant newline added by some text editors
    if lines[-1] == '': lines.pop()
    return lines

def is_prime(a):
    if a < 2: return False
    for x in range(2, int(sqrt(a)) + 1):
        if a % x == 0: return False
    return True

def get_pow2(n):
    if n < 0 or n.bit_count() != 1: raise ValueError(f"get_pow2() did not receive a power of 2: {n}")
    return n.bit_length() - 1

def in_field(point, p):
  if not isinstance(point,int) or point < 0 or p < point:
    raise ValueError(f"point is non-integer or invalid field F_{p} element: {point}")
  return point

def field_neg(point, p):          return ((p-1)*point)     % p
def field_mul(point1, point2, p): return (point1 * point2) % p
def field_add(point1, point2, p): return (point1 + point2) % p

def parse_field_and_eval_table(lines):
    # validate line count
    get_pow2(len(lines)-1)

    # get and validate prime field index
    p = try_int(lines[0])
    if p is None or not is_prime(p):
      raise ValueError("Line 1 had invalid integer literal or non-prime integer: '{lines[0].strip()}'")

    # get prime field values
    eval_table = [0]*(len(lines)-1)
    for idx, line in enumerate(lines[1:]):
      e = try_int(line)
      if e is None or e < -1 or p < e::
        raise ValueError(f"Line {idx+1} had invalid integer literal or field element: '{line.strip()}'")
      eval_table[idx] = e

    return p,eval_table

def eval_chi_funcs(bit_len, p, points):
    # validate points
    if len(points) != bit_len:
      raise ValueError("Points list has invalid size")

    # preallocate tables
    sz = 1 << bit_len
    curr, nxt = [0]*sz, [0]*sz

    # build first table
    in_field(points[0], p)
    curr[0] = field_add(1, field_neg(points[0], p), p)
    curr[1] = points[0]

    # compute chi
    for point_idx,point in enumerate(points[1:]):
      # validate current point
      in_field(point, p)
      # evaluate current bit polynomials
      zero,one = field_add(1, field_neg(point, p), p), point
      # evaluate compound word polynomials
      curr_sz = 1 << (point_idx+1)
      for curr_idx in range(curr_sz):
        nxt_idx = curr_idx << 1
        nxt[nxt_idx  ] = field_mul(curr[curr_idx], zero, p)
        nxt[nxt_idx+1] = field_mul(curr[curr_idx], one,  p)
      # swap tables
      curr,nxt = nxt,curr

    # return evaluated word polynomials
    return curr

def mle(p, eval_table, points):
    bit_len = get_pow2(len(eval_table))
    # build chi funcs
    chi_table = eval_chi_funcs(bit_len, p, points)
    print(f"chi_table: {chi_table}")
    # validate chi_table size
    if len(eval_table) != len(chi_table):
      raise ValueError("eval_chi_funcs produced an incorrectly sized table")
    # accumulate eval table and chi func products
    total = 0
    for point1,point2 in zip(eval_table,chi_table):
      point = field_mul(point1, point2, p)
      total = field_add(total, point, p)
    return total

def run(fpath, points):
  p, eval_table = parse_field_and_eval_table(read_lines(fpath))
  points = [in_field(try_int(x), p) for x in points]
  result = mle(p, eval_table, points)
  return eval_table, points, result

if __name__ == "__main__":
  import sys
  if len(sys.argv[1:]) < 2: raise ValueError("Not enough arguments")

  fpath = sys.argv[1]
  points = sys.argv[2:]
  eval_table, points, res = run(fpath, points)

  print(f"mle({points}) = {res}")
