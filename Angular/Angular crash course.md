# Angular Crash Course (2025 Edition)

> A concise, modern guide to Angular **v17+** (standalone-first, signals, new control flow, functional providers). Works great for interviews and real projects.

---

## 1) Quick Start

### Prerequisites
- Node.js LTS (recommend ≥ 18)
- Angular CLI
```bash
npm install -g @angular/cli
```

### Create & run a new app (standalone by default)
```bash
ng new my-app
cd my-app
ng serve -o
```

> Tip: For SSR/SEO, enable during `ng new` or later:
```bash
ng add @angular/ssr
```

---

## 2) Standalone Components (no NgModules needed)
```ts
// src/app/app.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  template: `<h1>Hello {{ name }}</h1>`
})
export class AppComponent {
  name = 'Angular';
}
```

### Bootstrapping
```ts
// src/main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { routes } from './app/app.routes';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
  ],
});
```

### Routing (standalone)
```ts
// src/app/app.routes.ts
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home.component').then(m => m.HomeComponent)
  },
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.routes').then(m => m.ADMIN_ROUTES)
  },
  { path: '**', redirectTo: '' }
];
```

Create a lazy standalone component:
```bash
ng g c home --standalone --inline-template --inline-style
```

---

## 3) New Template Control Flow (`@if`, `@for`, `@switch`, `@defer`)

```html
<!-- @if / @else -->
@if (user(); as u) {
  <p>Hi, {{ u.name }}</p>
} @else {
  <button (click)="login()">Login</button>
}

<!-- @for with tracking -->
@for (item of items(); track item.id) {
  <li>{{ item.name }}</li>
} @empty {
  <em>No items</em>
}

<!-- @switch -->
@switch (status()) {
  @case ('loading') { <p>Loading…</p> }
  @case ('error') { <p class="error">Failed</p> }
  @default { <p>Ready</p> }
}

<!-- @defer for performance (lazy render) -->
@defer (on viewport) {
  <heavy-chart />
} @placeholder {
  <p>Preparing chart…</p>
} @loading {
  <p>Loading…</p>
}
```

---

## 4) Signals (fine‑grained reactivity)

```ts
import { signal, computed, effect } from '@angular/core';

export class Counter {
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  constructor() {
    effect(() => console.log('count:', this.count()));
  }

  inc() { this.count.update(v => v + 1); }
  reset() { this.count.set(0); }
}
```

**Patterns**
- Keep `computed` pure (no writes).
- Use `effect` for side-effects (DOM, logging, service calls).
- With RxJS interop: `toSignal` / `toObservable` from `@angular/core/rxjs-interop`.

```ts
import { toSignal } from '@angular/core/rxjs-interop';
import { startWith, map } from 'rxjs';

itemsSig = toSignal(this.http.get<Item[]>('/api/items').pipe(
  map(list => list.filter(x => x.active)),
  startWith([])
), { initialValue: [] });
```

---

## 5) Dependency Injection & Services (functional providers)

```ts
// src/app/data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class DataService {
  constructor(private http: HttpClient) {}
  getUsers() { return this.http.get<User[]>('/api/users'); }
}
```

Functional interceptor (concise):
```ts
// src/app/auth.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('token');
  const authReq = token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req;
  return next(authReq);
};
```

Register with the new providers API:
```ts
import { provideHttpClient, withInterceptors } from '@angular/common/http';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor])),
  ],
});
```

Functional guard:
```ts
// src/app/auth.guard.ts
import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

export const authGuard: CanActivateFn = () => {
  const router = inject(Router);
  const isLoggedIn = !!localStorage.getItem('token');
  return isLoggedIn || router.createUrlTree(['/login']);
};
```

Use guard:
```ts
{ path: 'dashboard', canActivate: [authGuard], loadComponent: () => import('./dashboard.component').then(m => m.DashboardComponent) }
```

---

## 6) Forms (Typed Reactive Forms preferred)

```ts
import { Component } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';

type LoginForm = FormGroup<{
  username: FormControl<string>;
  password: FormControl<string>;
}>;

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <input formControlName="username" placeholder="Username">
      <input type="password" formControlName="password" placeholder="Password">
      <button type="submit" [disabled]="form.invalid">Login</button>
    </form>
    <pre>{{ form.value | json }}</pre>
  `
})
export class LoginComponent {
  form: LoginForm = new FormGroup({
    username: new FormControl('', { nonNullable: true, validators: [Validators.required] }),
    password: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.minLength(8)] }),
  });

  submit() { if (this.form.valid) {/* call API */} }
}
```

Template-driven still works (smaller forms):
```html
<input name="username" [(ngModel)]="user.name">
```

---

## 7) HTTP Client (modern setup)

```ts
import { HttpClient } from '@angular/common/http';
import { inject } from '@angular/core';

export class UserService {
  private http = inject(HttpClient);
  getUsers() { return this.http.get<User[]>('/api/users'); }
  getUser(id: string) { return this.http.get<User>(`/api/users/${id}`); }
}
```

Error handling patterns:
- Interceptor for common errors
- `catchError` in feature services
- Display user-friendly messages via a toast/snackbar

---

## 8) Performance Playbook

- **Signals + new control flow** → fewer checks, granular updates
- **Lazy load** routes/components (`loadChildren`, `loadComponent`)
- **@defer** heavy UI
- **track** in `@for` for stable list identity
- **CD**: OnPush still valid; signals also work great in zoneless setups
- Split bundles, preconnect critical origins, cache aggressively
- Avoid large work on main thread (use Web Workers where needed)

---

## 9) Testing (Unit & E2E)

**Unit tests** (Jasmine or Jest). Example service test:
```ts
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { DataService } from './data.service';

describe('DataService', () => {
  let httpMock: HttpTestingController;
  let service: DataService;

  beforeEach(() => {
    TestBed.configureTestingModule({ imports: [HttpClientTestingModule] });
    httpMock = TestBed.inject(HttpTestingController);
    service = TestBed.inject(DataService);
  });

  it('GET /api/users', () => {
    const mock = [{ id: 1, name: 'A' }];
    service.getUsers().subscribe(r => expect(r).toEqual(mock as any));
    httpMock.expectOne('/api/users').flush(mock);
    httpMock.verify();
  });
});
```

**E2E**: Prefer **Cypress** or **Playwright** (Protractor is deprecated).

---

## 10) Code Organization (feature-first)

```
src/
  app/
    home/            // feature
      home.component.ts
    users/           // feature
      users.routes.ts
      list.component.ts
      detail.component.ts
    shared/          // shared ui (pipes, directives, dumb components)
    core/            // singletons (interceptors, guards, services)
    app.component.ts
    app.routes.ts
```

CLI helpers:
```bash
ng g c feature/list --standalone
ng g guard auth --functional
ng g interceptor auth --functional
```

---

## 11) Common Snippets

**Two-way binding (standalone component model())**
```ts
import { Component, model } from '@angular/core';

@Component({
  selector: 'rating',
  standalone: true,
  template: `
    <button (click)="dec()">-</button>
    <span>{{ value() }}</span>
    <button (click)="inc()">+</button>
  `
})
export class RatingComponent {
  value = model(0);
  inc() { this.value.update(v => v + 1); }
  dec() { this.value.update(v => v - 1); }
}
```

**track function in lists**
```html
@for (u of users(); track u.id) {
  <div>{{ u.name }}</div>
}
```

**Functional Resolver (fetch before route enters)**
```ts
import { ResolveFn } from '@angular/router';
import { inject } from '@angular/core';
import { UserService } from './user.service';

export const userResolver: ResolveFn<any> = (route) => {
  return inject(UserService).getUser(route.paramMap.get('id')!);
};
```

---

## 12) Migration Notes (for older content in this repo)

- Prefer **standalone components** over NgModules for new code.
- Use new **template control flow** (`@if/@for/@switch/@defer`) over `*ngIf/*ngFor` when possible.
- Replace Protractor with **Cypress/Playwright** for E2E.
- Favor **Reactive Forms with types** for maintainability.
- Consider **signals** + zoneless CD for high-perf UIs.

---

## 13) Cheat Sheet (interview‑friendly)

- Standalone-first, `bootstrapApplication`, `provideRouter`, `provideHttpClient`
- New control flow: `@if/@for/@switch/@defer`
- Signals: `signal`, `computed`, `effect`, interop with RxJS
- Functional providers: interceptors/guards as functions
- Lazy routes: `loadChildren`, `loadComponent`
- Typed Reactive Forms; template-driven for simple cases
- Testing: HttpTestingController; E2E with Cypress/Playwright
- Perf: lazy UI, track identity, split bundles, workers

---

Happy building! 🚀
