# React Query (TanStack Query) – Revision Sheet

A practical, interview‑ready summary of React Query/TanStack Query for React apps (focus on v4/v5 concepts).

## Why use it?
- Declarative data fetching/caching layer for client state (server state) that handles lifecycle, retries, background refetch, and cache invalidation.
- Eliminates manual `useEffect` + `useState` boilerplate and keeps UI in sync with server.
- Works with any data source (REST/GraphQL/SDK); transport agnostic.

## Install & setup
- Core: `npm i @tanstack/react-query` (or `yarn add ...`).
- Devtools (optional, but highly recommended in dev only): `npm i @tanstack/react-query-devtools`.
- Create a client once and provide it:
  ```tsx
  // main.tsx / index.tsx
  import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { staleTime: 0, refetchOnWindowFocus: true, retry: 3 },
    },
  });

  root.render(
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  );
  ```
- Devtools:
  ```tsx
  import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
  <ReactQueryDevtools initialIsOpen={false} />;
  ```

## Core concepts
- **Query**: Cached read operation; identified by a **query key** (array, e.g. `['todos', userId]`). Keys must be stable & serializable.
- **Mutation**: Write/side‑effect operation (`POST/PUT/PATCH/DELETE`). Not cached; can trigger invalidation.
- **Query Cache**: Stores data + metadata per key. Managed by `QueryClient`.
- **Stale vs cache time**
  - `staleTime` (ms): how long data is considered fresh. Fresh data skips auto-refetch on mount/focus/network reconnect. Default: 0 (immediately stale).
  - `gcTime`/`cacheTime` (ms): how long unused data stays in cache after last subscriber unmounts (default 5 min). After GC, data refetches on next mount.
- **Statuses**: `isLoading`, `isFetching`, `isError`, `isSuccess`; plus `error`, `data`, `status`.
- **Transport agnostic**: You provide fetcher (fetch/axios/graphql-request, etc.).

## `useQuery` essentials
```tsx
const { data, isLoading, isFetching, error } = useQuery({
  queryKey: ['todos', userId],
  queryFn: () => api.getTodos(userId),
  enabled: !!userId,          // dependent query
  staleTime: 5 * 60_000,      // 5 minutes fresh
  refetchOnWindowFocus: false,
  select: todos => todos.filter(t => !t.done), // client projection
  placeholderData: keepPreviousData,           // keeps old page during pagination
});
```
- `enabled`: gate execution (dependent queries, feature flags).
- `select`: project/shape data without extra renders.
- `initialData`: seed cache (e.g., SSR/hydration or state passed via router loader).
- `placeholderData`: temporary data until fetch resolves (often `keepPreviousData` for pagination).
- `refetchInterval`: polling; set `refetchIntervalInBackground` to keep polling while tab hidden.
- `retry`: number | boolean | (failureCount, error) => boolean. Default 3, exponential backoff.
- `suspense`: integrate with React Suspense (v18).
- `networkMode`: `online` (default), `always`, or `offlineFirst` (v5) to control behavior with navigator.onLine.

## Mutations (`useMutation`)
```tsx
const mutation = useMutation({
  mutationFn: (todo) => api.updateTodo(todo),
  onSuccess: (data, variables) => {
    queryClient.invalidateQueries({ queryKey: ['todos', variables.userId] });
  },
});
```
- `mutate` (sync) and `mutateAsync` (promise).
- **Optimistic updates** pattern:
  ```tsx
  const mutation = useMutation({
    mutationFn: api.updateTodo,
    onMutate: async (variables) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      const previous = queryClient.getQueryData(['todos']);
      queryClient.setQueryData(['todos'], old =>
        old.map(t => t.id === variables.id ? { ...t, ...variables } : t)
      );
      return { previous };
    },
    onError: (_err, _vars, ctx) => queryClient.setQueryData(['todos'], ctx?.previous),
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
  });
  ```
- Prefer invalidation over manual refetch unless you have specialized cache update logic.

## Invalidation & refetching
- Invalidate by key (broad/narrow):
  ```ts
  queryClient.invalidateQueries({ queryKey: ['todos'] });           // all todos
  queryClient.invalidateQueries({ queryKey: ['todos', userId] });   // scoped
  ```
- `refetchQueries` triggers immediate refetch of active queries.
- `setQueryData` to update cache directly (fast UI), but remember to keep server truth accurate eventually.

## Data prefetching
- Use on navigation hover or SSR loaders:
  ```ts
  await queryClient.prefetchQuery({
    queryKey: ['todo', id],
    queryFn: () => api.getTodo(id),
    staleTime: 10_000,
  });
  ```
- Works with `dehydrate`/`Hydrate` for SSR/SSG (Next.js/Remix).

## Parallel, dependent, and paginated queries
- **Parallel**: call multiple `useQuery` hooks; they run independently.
- **Dependent**: use `enabled` to wait for parent data (`enabled: !!userId`).
- **Paginated** (`pageParam` with `useInfiniteQuery`):
  ```tsx
  const {
    data, fetchNextPage, hasNextPage, isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['feed'],
    queryFn: ({ pageParam = 0 }) => api.getFeed(pageParam),
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? false,
    staleTime: 30_000,
  });
  ```
- **Keep previous page while loading next**: `placeholderData: keepPreviousData` with standard pagination or use `useInfiniteQuery`.

## Window focus & reconnect behavior
- Defaults: `refetchOnWindowFocus: true`, `refetchOnReconnect: true`.
- Disable for expensive endpoints or set longer `staleTime`.
- Focus events batch to avoid thrash.

## Caching heuristics cheat sheet
- High-read, low-churn lists: set `staleTime` to minutes; disable focus refetch.
- Critical freshness (prices, stocks): small `staleTime`, enable polling.
- Forms editing existing entity: seed with `initialData`, use `setQueryData` on save, then invalidate.
- Slow/rarely used data: larger `cacheTime` to free memory; or `gcTime: Infinity` to pin.

## Error handling
- Query errors surface in `error`; render fallback UI or toast.
- Global handler: `QueryClient` option `queryCache.onError` or `MutationCache.onError`.
- `retry: false` for non-retriable errors (validation/4xx).

## Suspense & streaming (React 18)
- Enable `suspense: true` on queries to let React boundaries show fallback during fetch.
- For mutations + suspense, still handle errors via error boundaries.

## SSR / Next.js / Remix
- Create client per request to avoid shared caches on server.
- Prefetch with `queryClient.prefetchQuery` on server, then `dehydrate` and wrap page with `<Hydrate state={dehydratedState}>`.
- In Next.js App Router, often use server components for fetch + `dehydrate` in a client boundary.

## Devtools usage
- Shows cache keys, status, observers, data snapshots.
- Use only in development; lazy load to keep bundle small.

## Common pitfalls
- Unstable query keys (objects/functions) cause cache misses—always use arrays of serializable values.
- Forgetting `enabled` for dependent queries leads to fetch with `undefined` params.
- Setting `staleTime` too low causes refetch storms; too high can show stale data.
- Not invalidating after mutations → UI shows stale cache.
- Using `mutationFn` to also update cache instead of `onSuccess/onMutate` – separation is clearer.

## Quick patterns
- **List + detail**: list key `['todos']`, detail key `['todo', id]`; invalidate detail on edit and list on create/delete.
- **Toggle feature flag**: `useQuery` with `staleTime: Infinity` (flags rarely change), manual refetch on admin change.
- **File uploads**: use `useMutation`, set `networkMode: 'always'` if navigator.offline matters.
- **Auth token refresh**: keep fetcher centralized (axios interceptor); React Query handles retries but let interceptor refresh token and retry once.

## API surface at a glance
- Hooks: `useQuery`, `useInfiniteQuery`, `useMutation`, `useQueryClient`, `useIsFetching`, `useIsMutating`.
- Client methods: `prefetchQuery`, `fetchQuery`, `invalidateQueries`, `refetchQueries`, `cancelQueries`, `setQueryData`, `getQueryData`, `getQueriesData`.
- Utilities: `keepPreviousData`, `dehydrate`/`Hydrate`, `focusManager`, `onlineManager`.

## Upgrade notes (v4 → v5 highlights)
- Package stayed `@tanstack/react-query`; API largely compatible.
- `cacheTime` renamed to `gcTime` but `cacheTime` alias remains.
- `networkMode` adds `always`/`offlineFirst`.
- `retryOnMount` removed; smarter defaults for focus/mount.
- Infinite queries use `pageParam` unchanged; improved `hasNextPage` inference when `getNextPageParam` returns `undefined`/`null`.

## Interview-ready talking points
- Explain difference between client state vs server state; React Query manages the latter.
- Outline lifecycle: request → cache → stale/fresh → background refetch → GC.
- Describe how to avoid waterfall requests with `enabled` and parallel queries.
- Show optimistic update flow with rollback.
- Mention SSR hydration and `dehydrate` for Next.js/Remix.
- Note defaults (staleTime 0, cacheTime 5m, retry 3, refetch on focus/reconnect).

## Minimal starter snippet (copy/paste)
```tsx
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';

const client = new QueryClient();

function Todos({ userId }) {
  const { data, isLoading } = useQuery({
    queryKey: ['todos', userId],
    queryFn: () => fetch(`/api/todos?user=${userId}`).then(r => r.json()),
    enabled: !!userId,
  });
  if (isLoading) return <p>Loading...</p>;
  return <ul>{data.map(t => <li key={t.id}>{t.title}</li>)}</ul>;
}

export default function App() {
  return (
    <QueryClientProvider client={client}>
      <Todos userId=\"123\" />
    </QueryClientProvider>
  );
}
```

Keep this sheet handy; it covers 90% of React Query questions and day‑to‑day usage.
