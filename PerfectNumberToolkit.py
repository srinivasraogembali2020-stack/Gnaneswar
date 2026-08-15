#!/usr/bin/env python3
"""
=============================================================================
  PERFECT NUMBER TOOLKIT (Python 3.8+) - Extended Edition
  A comprehensive mathematical toolkit for:
  1. Perfect, Abundant & Deficient Classification
  2. Euclid-Euler Theorem & Catalog Generator
  3. Lucas-Lehmer Primality Test for Mersenne Numbers
  4. Aliquot Trajectories & Amicable Pair Sieve
  5. Semiperfect (Pseudoperfect) Verification
  6. Weird Number Engine (Abundant but not Semiperfect)
  7. Untouchable Number Detector (Non-Aliquot Sums)
  8. Sociable Cycles & Multi-Period Orbit Sieve
  9. k-Hyperperfect Number Solver & Verifier
  10. Superperfect Number Evaluator (sigma(sigma(n)) = 2n)
  11. Multiperfect (k-fold Divisor Harmonizers, sigma(n)=k*n)
  12. Odd Perfect Number Theorem & Touchard Sieve
=============================================================================
"""

import math
import sys
import time
from typing import Dict, List, Optional, Set, Tuple, Union


# =============================================================================
# 1. CORE NUMBER THEORY & DIVISOR FUNCTIONS
# =============================================================================

def proper_divisors(n: int) -> List[int]:
    """Returns all proper positive divisors of n strictly less than n."""
    if n <= 1:
        return []
    small, large = [], []
    limit = int(math.isqrt(n))
    for i in range(1, limit + 1):
        if n % i == 0:
            small.append(i)
            pair = n // i
            if pair != i and pair != n:
                large.append(pair)
    return small + large[::-1]


def all_divisors(n: int) -> List[int]:
    """Returns all positive divisors of n including n itself."""
    if n <= 0:
        return []
    divs = proper_divisors(n)
    divs.append(n)
    return divs


def aliquot_sum(n: int) -> int:
    """Computes s(n) = sum of proper divisors of n."""
    return sum(proper_divisors(n))


def divisor_sum(n: int) -> int:
    """Computes sigma_1(n) = sum of all positive divisors of n."""
    return aliquot_sum(n) + n


def prime_factors(n: int) -> Dict[int, int]:
    """Returns prime factorization as {prime: power}."""
    if n <= 1:
        return {}
    factors = {}
    temp = n
    while temp % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        temp //= 2
    d = 3
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 2
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    return factors


def is_prime(n: int) -> bool:
    """Fast deterministic Miller-Rabin test for integer primality."""
    if n < 2:
        return False
    if n in (2, 3, 5, 7):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n <= a:
            break
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# =============================================================================
# 2. CLASSICAL CLASSIFICATION & SEMIPERFECT TOOLS
# =============================================================================

def is_perfect(n: int) -> bool:
    """Returns True if n is perfect (s(n) == n)."""
    return n > 1 and aliquot_sum(n) == n


def classify(n: int) -> Dict[str, Union[int, str, List[int], Dict[int, int]]]:
    """Full divisor profile and abundance classification."""
    divs = proper_divisors(n)
    s = sum(divs)
    sigma = s + n
    abundance = s - n
    status = "PERFECT" if s == n else ("ABUNDANT" if s > n else "DEFICIENT")
    return {
        "number": n,
        "classification": status,
        "proper_divisors": divs,
        "divisor_count": len(divs),
        "aliquot_sum_s": s,
        "divisor_sum_sigma": sigma,
        "abundance": abundance,
        "abundance_index": round(sigma / n, 6),
        "prime_factors": prime_factors(n),
        "binary": bin(n)[2:]
    }


def is_semiperfect(n: int) -> Tuple[bool, List[int]]:
    """Checks if a subset of proper divisors sums to n using subset-sum DP."""
    divs = proper_divisors(n)
    if sum(divs) < n:
        return False, []
    dp = {0: []}
    for d in divs:
        new_dp = {}
        for cur_sum, subset in dp.items():
            nxt_sum = cur_sum + d
            if nxt_sum <= n and nxt_sum not in dp:
                new_dp[nxt_sum] = subset + [d]
        dp.update(new_dp)
        if n in dp:
            return True, dp[n]
    return (n in dp), dp.get(n, [])


# =============================================================================
# 3. WEIRD NUMBERS (Abundant but not Semiperfect)
# =============================================================================

def is_weird_number(n: int) -> Tuple[bool, str]:
    """
    A number is WEIRD if it is abundant (s(n) > n) but NOT semiperfect
    (no subset of proper divisors sums to n). Smallest weird number is 70.
    """
    divs = proper_divisors(n)
    s = sum(divs)
    if s <= n:
        return False, f"{n} is not abundant (s(n)={s} <= {n})"
    semi, _ = is_semiperfect(n)
    if not semi:
        return True, f"⭐ {n} IS A WEIRD NUMBER! (Abundant with s(n)={s}, but no subset of divisors sums to {n})"
    return False, f"{n} is abundant and semiperfect (pseudoperfect)."


def find_weird_numbers(limit: int) -> List[int]:
    """Finds all weird numbers up to limit (e.g. 70, 836, 4030, 5830...)."""
    weird_list = []
    for n in range(70, limit + 1):
        if is_weird_number(n)[0]:
            weird_list.append(n)
    return weird_list


# =============================================================================
# 4. UNTOUCHABLE NUMBERS (Non-Aliquot Sums)
# =============================================================================

def is_untouchable(n: int, search_upper_bound: Optional[int] = None) -> Tuple[bool, Optional[int]]:
    """
    Checks if n is an UNTOUCHABLE number (cannot be expressed as the sum of
    proper divisors s(x) of any integer x). Known examples: 2, 5, 52, 88, 96, 120...
    """
    if n == 5:
        return True, None
    bound = search_upper_bound or max((n + 1) ** 2, 2000)
    bound = min(bound, 200000)  # Safe search ceiling for CLI responsiveness
    for x in range(2, bound + 1):
        if aliquot_sum(x) == n:
            return False, x
    return True, None


# =============================================================================
# 5. SOCIABLE NUMBER CYCLES (Period >= 3)
# =============================================================================

def find_sociable_cycle(start_n: int, max_steps: int = 50) -> Dict[str, Union[int, List[int], str, bool]]:
    """
    Traces an aliquot trajectory to find closed sociable cycles of length k >= 3.
    e.g. The smallest known 5-cycle starts at 12496.
    """
    seen = []
    current = start_n
    for _ in range(max_steps):
        seen.append(current)
        nxt = aliquot_sum(current) if current > 0 else 0
        if nxt in seen:
            cycle_start = seen.index(nxt)
            cycle = seen[cycle_start:]
            period = len(cycle)
            desc = "Perfect Number (1-cycle)" if period == 1 else ("Amicable Pair (2-cycle)" if period == 2 else f"Sociable {period}-Cycle")
            return {
                "start": start_n,
                "is_sociable": period >= 3,
                "period": period,
                "cycle": cycle,
                "classification": desc
            }
        if nxt == 0 or nxt > 10**10:
            break
        current = nxt
    return {"start": start_n, "is_sociable": False, "period": 0, "cycle": [], "classification": "No cycle detected in range"}


# =============================================================================
# 6. k-HYPERPERFECT NUMBERS
# =============================================================================

def is_hyperperfect(n: int, k: int = 1) -> Tuple[bool, int]:
    """
    Checks if n is k-hyperperfect: n = 1 + k * (s(n) - 1).
    k = 1 is the classical perfect number (s(n) = n).
    k = 2 examples: 21, 2133, 19521, 176661, 1292277.
    """
    if n <= 1 or k <= 0:
        return False, 0
    s = aliquot_sum(n)
    target = 1 + k * (s - 1)
    return (target == n), s


def find_hyperperfect(limit: int, k: int = 2) -> List[int]:
    """Finds all k-hyperperfect numbers up to limit."""
    return [n for n in range(2, limit + 1) if is_hyperperfect(n, k)[0]]


# =============================================================================
# 7. SUPERPERFECT NUMBERS
# =============================================================================

def is_superperfect(n: int) -> Tuple[bool, int, int]:
    """
    A number n is SUPERPERFECT if sigma(sigma(n)) = 2n.
    Suryanarayana (1969): Even superperfect numbers are 2^k where 2^(k+1)-1 is prime.
    """
    if n <= 1:
        return False, 0, 0
    sig1 = divisor_sum(n)
    sig2 = divisor_sum(sig1)
    return (sig2 == 2 * n), sig1, sig2


# =============================================================================
# 8. MULTIPERFECT (k-ABUNDANT) NUMBERS
# =============================================================================

def multiperfect_analysis(n: int) -> Dict[str, Union[int, float, bool]]:
    """
    Analyzes harmonic multiperfect numbers where sigma(n) = k * n for integer k >= 2.
    k = 2: Classical perfect numbers (6, 28, 496, 8128)
    k = 3: Triperfect numbers (120, 672, 523776)
    k = 4: Quadraperfect numbers (30240, 32760, 2178540)
    """
    sigma = divisor_sum(n)
    is_multi = (sigma % n == 0)
    k = sigma // n if is_multi else None
    return {
        "number": n,
        "sigma": sigma,
        "is_multiperfect": is_multi,
        "k_index": k,
        "abundance_ratio": round(sigma / n, 6)
    }


# =============================================================================
# 9. ODD PERFECT NUMBER CONSTRAINT & TOUCHARD SIEVE
# =============================================================================

def odd_perfect_constraints(n: int) -> Dict[str, Union[bool, str, List[str]]]:
    """
    Applies major theoretical constraints established for Odd Perfect Numbers:
    1. Touchard's Theorem: n ≡ 1 (mod 12) OR n ≡ 9 (mod 36)
    2. Euler's Form: n = q^a * m^2 where q is prime with q ≡ a ≡ 1 (mod 4)
    3. Minimum Bound: Proven that odd perfect numbers must exceed 10^1500
    4. Divisor Count: Must have at least 101 distinct prime factors (Hare, 2012)
    """
    if n % 2 == 0:
        return {"is_odd": False, "passed_all_tests": False, "notes": ["Number is even."]}
    
    passed_touchard = (n % 12 == 1) or (n % 36 == 9)
    factors = prime_factors(n)
    
    # Check Euler's form q^a * m^2
    euler_prime_candidates = []
    for p, a in factors.items():
        if a % 2 == 1 and p % 4 == 1 and a % 4 == 1:
            euler_prime_candidates.append((p, a))
    
    euler_valid = (len(euler_prime_candidates) == 1)
    is_actual_perfect = is_perfect(n)
    
    notes = [
        f"Touchard Form (mod 12/36): {'PASS' if passed_touchard else 'FAIL'}",
        f"Euler Structure (q^a * m^2): {'PASS' if euler_valid else 'FAIL'} ({euler_prime_candidates})",
        f"Distinct Prime Factors: {len(factors)} (Theoretical min for OPN: 101)",
        f"Actual Perfect Check: {is_actual_perfect}"
    ]
    
    return {
        "number": n,
        "is_odd": True,
        "touchard_passed": passed_touchard,
        "euler_form_passed": euler_valid,
        "prime_factor_count": len(factors),
        "is_perfect": is_actual_perfect,
        "notes": notes
    }


# =============================================================================
# 10. LUCAS-LEHMER & EUCLID-EULER CATALOG
# =============================================================================

KNOWN_MERSENNE_EXPONENTS = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281,
    3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243
]

def euclid_euler_perfect(p: int) -> int:
    """Calculates 2^(p-1) * (2^p - 1)."""
    return (1 << (p - 1)) * ((1 << p) - 1)


def lucas_lehmer_test(p: int, max_trace: int = 10) -> Dict[str, Union[int, bool, List[int], float]]:
    """Runs the Lucas-Lehmer test for M_p = 2^p - 1."""
    start = time.perf_counter()
    if p == 2:
        return {"p": 2, "mersenne_number": 3, "is_prime": True, "iterations": [4], "execution_time_sec": time.perf_counter() - start}
    mp = (1 << p) - 1
    s = 4
    trace = [s]
    for i in range(1, p - 1):
        s = (s * s - 2) % mp
        if len(trace) < max_trace or i == p - 2:
            trace.append(s)
    return {
        "p": p,
        "mersenne_number": mp,
        "is_prime": (s == 0),
        "iterations": trace,
        "execution_time_sec": time.perf_counter() - start
    }


def aliquot_trajectory(start_n: int, max_steps: int = 30) -> Dict[str, Union[int, List[dict], str, bool]]:
    """Traces the aliquot sequence from start_n."""
    seen = []
    current = start_n
    history = []
    for step in range(max_steps + 1):
        seen.append(current)
        nxt = aliquot_sum(current) if current > 0 else 0
        status = "Terminated at 0" if current == 0 else ("Fixed Point" if current == nxt else (f"Cycle loop with {nxt}" if nxt in seen else f"s({current}) -> {nxt}"))
        history.append({"step": step, "value": current, "aliquot_sum": nxt, "status": status})
        if current == 0 or current == nxt or nxt in seen:
            return {"start": start_n, "steps": history, "step_count": len(history), "outcome": status, "is_periodic": (nxt in seen)}
        current = nxt
    return {"start": start_n, "steps": history, "step_count": len(history), "outcome": f"Exceeded {max_steps} steps", "is_periodic": False}


def find_amicable_pairs(limit: int) -> List[Tuple[int, int]]:
    """Finds all amicable pairs (a, b) up to limit."""
    sums = [0] * (limit + 1)
    for i in range(1, limit + 1):
        sums[i] = aliquot_sum(i)
    pairs = []
    for a in range(2, limit + 1):
        b = sums[a]
        if a < b <= limit and sums[b] == a:
            pairs.append((a, b))
    return pairs


# =============================================================================
# 11. CLI INTERFACE & COMMAND DISPATCHER
# =============================================================================

def print_banner():
    print("=" * 78)
    print("  🐍 PERFECT NUMBER TOOLKIT — Extended Edition (12 Core Modules)")
    print("=" * 78)
    print("Commands:")
    print("  • perfect <n>           - Full analysis, abundance & proper divisor list")
    print("  • lucas <p>             - Lucas-Lehmer test on Mersenne number 2^p - 1")
    print("  • aliquot <n> [steps]   - Trace aliquot trajectory & detect cycles")
    print("  • amicable <limit>      - Sieve amicable number pairs up to limit")
    print("  • semiperfect <n>       - Subset-sum check for pseudoperfectness")
    print("  • weird <n / limit>     - Test weirdness (abundant but NOT semiperfect)")
    print("  • untouchable <n>       - Check if n is a non-aliquot untouchable sum")
    print("  • sociable <n>          - Trace closed sociable orbits of period >= 3")
    print("  • hyperperfect <n> [k]  - Test k-hyperperfectness: n = 1 + k(s(n)-1)")
    print("  • superperfect <n>      - Evaluate Suryanarayana condition σ(σ(n))=2n")
    print("  • multiperfect <n>      - Test k-fold harmonic divisor sum σ(n) = k*n")
    print("  • odd_check <n>         - Touchard & Euler sieve on odd candidates")
    print("  • catalog [count]       - Euclid-Euler even perfect numbers list")
    print("  • help / exit           - Display manual or exit")
    print("-" * 78)


def main():
    print_banner()

    while True:
        try:
            line = input("\n[PyToolkit] >>> ").strip()
            if not line:
                continue
            if line in ("exit", "quit", "q"):
                print("Exiting Perfect Number Toolkit. Happy computing!")
                break
                
            parts = line.split()
            cmd = parts[0].lower()

            if cmd in ("perfect", "classify"):
                n = int(parts[1])
                res = classify(n)
                print(f"\n--- Classification for {n} ---")
                print(f"• Status           : {res['classification']}")
                print(f"• Proper Divisors  : {res['proper_divisors'][:18]}{' ...' if len(res['proper_divisors']) > 18 else ''} (Total {res['divisor_count']})")
                print(f"• Aliquot Sum s(n) : {res['aliquot_sum_s']}")
                print(f"• Divisor Sum σ(n) : {res['divisor_sum_sigma']}")
                print(f"• Abundance Index  : {res['abundance_index']}")
                print(f"• Prime Factors    : {res['prime_factors']}")

            elif cmd in ("lucas", "mersenne"):
                p = int(parts[1])
                res = lucas_lehmer_test(p)
                print(f"\n--- Lucas-Lehmer Test for M_{p} = 2^{p} - 1 ---")
                print(f"• Mersenne Value   : {res['mersenne_number']}")
                print(f"• Primality Result : {'⭐ MERSENNE PRIME' if res['is_prime'] else '❌ COMPOSITE'}")
                if res['is_prime']:
                    print(f"• Perfect Number   : {euclid_euler_perfect(p)}")

            elif cmd == "aliquot":
                n = int(parts[1])
                steps = int(parts[2]) if len(parts) > 2 else 20
                traj = aliquot_trajectory(n, steps)
                print(f"\n--- Aliquot Trajectory for {n} ---")
                for s in traj['steps']:
                    print(f"  Step {s['step']:2d}: {s['value']:<15d} [{s['status']}]")

            elif cmd == "amicable":
                lim = int(parts[1]) if len(parts) > 1 else 3000
                pairs = find_amicable_pairs(lim)
                print(f"\nAmicable pairs up to {lim}: {pairs}")

            elif cmd == "semiperfect":
                n = int(parts[1])
                semi, sub = is_semiperfect(n)
                print(f"Semiperfect for {n}: {semi} (Subset: {sub})")

            elif cmd == "weird":
                arg = int(parts[1])
                if len(parts) > 2 and parts[1] == "find":
                    lim = int(parts[2])
                    print(f"Weird numbers up to {lim}: {find_weird_numbers(lim)}")
                else:
                    is_w, msg = is_weird_number(arg)
                    print(msg)

            elif cmd == "untouchable":
                n = int(parts[1])
                is_untouch, preimage = is_untouchable(n)
                if is_untouch:
                    print(f"⭐ {n} is an UNTOUCHABLE number (no integer x has s(x) = {n}).")
                else:
                    print(f"❌ {n} is touchable: s({preimage}) = {n}.")

            elif cmd == "sociable":
                n = int(parts[1])
                res = find_sociable_cycle(n)
                print(f"Sociable Orbit for {n}: {res['classification']}")
                if res['cycle']:
                    print(f"Cycle (period {res['period']}): {res['cycle']}")

            elif cmd == "hyperperfect":
                n = int(parts[1])
                k = int(parts[2]) if len(parts) > 2 else 1
                is_hyp, s = is_hyperperfect(n, k)
                print(f"Hyperperfect ({k}-hyperperfect) for {n}: {is_hyp} (s(n)={s})")

            elif cmd == "superperfect":
                n = int(parts[1])
                is_sup, s1, s2 = is_superperfect(n)
                print(f"Superperfect for {n}: {is_sup} (σ(n)={s1}, σ(σ(n))={s2}, target 2n={2*n})")

            elif cmd == "multiperfect":
                n = int(parts[1])
                res = multiperfect_analysis(n)
                print(f"Multiperfect for {n}: {res['is_multiperfect']} (k = {res['k_index']}, σ(n) = {res['sigma']})")

            elif cmd in ("odd_check", "odd_constraints"):
                n = int(parts[1])
                res = odd_perfect_constraints(n)
                print(f"\n--- Odd Perfect Sieve for {n} ---")
                for note in res['notes']:
                    print(f"• {note}")

            elif cmd == "catalog":
                count = int(parts[1]) if len(parts) > 1 else 8
                print(f"\n--- Euclid-Euler Catalog (First {count}) ---")
                for idx, p in enumerate(KNOWN_MERSENNE_EXPONENTS[:count], 1):
                    print(f"#{idx} (p={p}): {euclid_euler_perfect(p)}")

            elif cmd == "help":
                print_banner()

            else:
                print(f"Unknown command: '{cmd}'. Type 'help' for available options.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
