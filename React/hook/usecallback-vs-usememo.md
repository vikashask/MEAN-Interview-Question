useCallback gives you referential equality between `renders for functions`.
And useMemo gives you referential equality between `renders for values`.
The difference is that useCallback returns its function when the dependencies change while useMemo calls its function and returns the result.

- UseCallback
  Returns a memoized callback.

- UseMemo
  Returns a memoized value.
