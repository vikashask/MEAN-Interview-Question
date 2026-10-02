# Array interview patterns — derive, don't memorize

> For each problem: say the input contract, name the invariant, trace an edge case, then state time and **auxiliary** space (exclude output unless stated). Review [array fundamentals](./array/array.md) first.

| Problem                  | Pattern / invariant                               | Complexity                                                                       | Trap                                      |
| ------------------------ | ------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------- |
| Pair sum                 | seen complements in `Set`                         | expected `O(n)` time, `O(n)` space                                               | distinct indices / duplicate pairs        |
| Kth smallest             | quickselect partitions around pivot               | expected `O(n)`, worst `O(n²)`; in-place partition + iterative loop `O(1)` extra | `k` 1-based, mutates input                |
| Product except self      | prefix products × suffix products                 | `O(n)` time, `O(1)` extra **excluding `O(n)` output**                            | zeros, empty array                        |
| Longest consecutive      | only expand from set elements without predecessor | expected `O(n)` time/space                                                       | duplicate input                           |
| Majority > n/2           | Boyer–Moore cancels unequal pairs                 | `O(n)` time, `O(1)` space                                                        | verify candidate if majority not promised |
| Search rotated sorted    | one half sorted each step                         | `O(log n)` if distinct, `O(1)` space                                             | duplicates may force `O(n)`               |
| Trapping rain water      | process lower boundary; maintain max seen         | `O(n)` time, `O(1)` space                                                        | empty/flat                                |
| Median two sorted arrays | left partition has all smaller values             | `O(log min(m,n))`, `O(1)`                                                        | both empty; partition edges               |
| Maximum product subarray | track max **and min** ending at index             | `O(n)` time, `O(1)`                                                              | negatives swap roles                      |

## Minimal worked solutions (JavaScript)

### 1. Pair sum — unique value pairs

```js
function pairs(nums, target) {
  const seen = new Set(),
    emitted = new Set(),
    result = [];
  for (const x of nums) {
    const y = target - x;
    const key = `${Math.min(x, y)},${Math.max(x, y)}`;
    if (seen.has(y) && !emitted.has(key)) {
      emitted.add(key);
      result.push([y, x]);
    }
    seen.add(x);
  }
  return result;
}
```

For arbitrary non-integer values, do not stringify the pair as a collision-free identity; use a nested `Map`/`Set` or specify integer inputs. A 2-sum _indices_ problem instead stores value → first index.

### 2. Kth smallest — in-place quickselect (1-based k)

```js
function kthSmallest(a, k) {
  if (k < 1 || k > a.length) throw new RangeError("k out of range");
  let lo = 0,
    hi = a.length - 1;
  while (lo <= hi) {
    const pivot = a[hi];
    let p = lo;
    for (let i = lo; i < hi; i++) {
      if (a[i] < pivot) {
        [a[p], a[i]] = [a[i], a[p]];
        p++;
      }
    }
    [a[p], a[hi]] = [a[hi], a[p]];
    if (p === k - 1) return a[p];
    if (p > k - 1) hi = p - 1;
    else lo = p + 1;
  }
}
```

Repeated last-pivot selection degrades on sorted/duplicate-heavy inputs. Random pivots improve expected behavior; median-of-medians gives worst-case linear selection at more complexity.

### 3. Product except self — output is not free

```js
function productExceptSelf(a) {
  const out = Array(a.length).fill(1);
  let product = 1;
  for (let i = 0; i < a.length; i++) {
    out[i] = product;
    product *= a[i];
  }
  product = 1;
  for (let i = a.length - 1; i >= 0; i--) {
    out[i] *= product;
    product *= a[i];
  }
  return out;
}
```

### 4. Longest consecutive — expand only at a start

```js
function longestConsecutive(a) {
  const s = new Set(a);
  let best = 0;
  for (const x of s) {
    if (s.has(x - 1)) continue;
    let y = x;
    while (s.has(y)) y++;
    best = Math.max(best, y - x);
  }
  return best;
}
```

### 5. Majority — verify if not guaranteed

```js
function majority(a) {
  let candidate,
    count = 0;
  for (const x of a) {
    if (count === 0) candidate = x;
    count += x === candidate ? 1 : -1;
  }
  return a.filter((x) => x === candidate).length > a.length / 2
    ? candidate
    : undefined;
}
```

### 6. Rotated sorted search — distinct values

```js
function rotatedSearch(a, target) {
  let l = 0,
    r = a.length - 1;
  while (l <= r) {
    const m = l + Math.floor((r - l) / 2);
    if (a[m] === target) return m;
    if (a[l] <= a[m]) {
      if (a[l] <= target && target < a[m]) r = m - 1;
      else l = m + 1;
    } else if (a[m] < target && target <= a[r]) l = m + 1;
    else r = m - 1;
  }
  return -1;
}
```

### 7. Trapping rain water — lower side is settled

```js
function trappedWater(h) {
  let l = 0,
    r = h.length - 1,
    leftMax = 0,
    rightMax = 0,
    water = 0;
  while (l < r) {
    if (h[l] <= h[r]) {
      leftMax = Math.max(leftMax, h[l]);
      water += leftMax - h[l++];
    } else {
      rightMax = Math.max(rightMax, h[r]);
      water += rightMax - h[r--];
    }
  }
  return water;
}
```

### 8. Median of two sorted arrays — binary partition of shorter input

```js
function medianSorted(a, b) {
  if (a.length > b.length) return medianSorted(b, a);
  if (!a.length && !b.length) throw new RangeError("both inputs empty");
  let lo = 0,
    hi = a.length,
    leftCount = Math.floor((a.length + b.length + 1) / 2);
  while (lo <= hi) {
    const i = Math.floor((lo + hi) / 2),
      j = leftCount - i;
    const al = i ? a[i - 1] : -Infinity,
      ar = i < a.length ? a[i] : Infinity;
    const bl = j ? b[j - 1] : -Infinity,
      br = j < b.length ? b[j] : Infinity;
    if (al <= br && bl <= ar)
      return (a.length + b.length) % 2
        ? Math.max(al, bl)
        : (Math.max(al, bl) + Math.min(ar, br)) / 2;
    if (al > br) hi = i - 1;
    else lo = i + 1;
  }
  throw new Error("inputs must be sorted");
}
```

### 9. Maximum product subarray — keep both extremes

```js
function maxProduct(a) {
  if (!a.length) return undefined;
  let max = a[0],
    min = a[0],
    best = a[0];
  for (let i = 1; i < a.length; i++) {
    const x = a[i],
      prevMax = max,
      prevMin = min;
    max = Math.max(x, x * prevMax, x * prevMin);
    min = Math.min(x, x * prevMax, x * prevMin);
    best = Math.max(best, max);
  }
  return best;
}
```

**Recall:** Which solution requires sorted input? Which one mutates? Which complexity excludes output? Can you explain why negatives make the _minimum_ product valuable?
