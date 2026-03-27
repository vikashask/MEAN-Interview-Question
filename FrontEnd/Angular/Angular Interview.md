# Angular Interview Questions and Answers

## Core Concepts

### 1. What is Angular?
Angular is a TypeScript-based open-source web application framework led by the Angular Team at Google. It offers a complete rewrite from AngularJS (Angular 1.x).

Key features:
- Component-based architecture
- TypeScript support
- Dependency Injection
- CLI tooling
- RxJS integration

### 2. What are Components?
Components are the building blocks of Angular applications. They consist of:

```typescript
@Component({
    selector: 'app-example',
    template: `
        <h1>{{ title }}</h1>
        <p>{{ description }}</p>
    `,
    styles: [`h1 { color: blue; }`]
})
export class ExampleComponent {
    title = 'Example Component';
    description = 'This is an example component';
}
```

### 3. What is Dependency Injection?
DI is a design pattern where classes receive their dependencies from external sources rather than creating them.

Example:
```typescript
@Injectable({
    providedIn: 'root'
})
export class UserService {
    getUsers() { /* ... */ }
}

@Component({
    selector: 'app-users'
})
export class UsersComponent {
    constructor(private userService: UserService) {}
}
```

## Data Binding

### 1. What are the different types of data binding?

#### One-way Data Binding
- Interpolation: `{{ value }}`
- Property Binding: `[property]="value"`
- Event Binding: `(event)="handler()"`

#### Two-way Data Binding
```typescript
[(ngModel)]="value"
```

Example:
```html
<!-- Interpolation -->
<h1>{{ title }}</h1>

<!-- Property Binding -->
<img [src]="imageUrl">

<!-- Event Binding -->
<button (click)="onClick()">Click me</button>

<!-- Two-way Binding -->
<input [(ngModel)]="name">
```

## Directives

### 1. What are the types of directives?

#### Component Directives
- Regular Angular components with template

#### Structural Directives
- `*ngIf`
- `*ngFor`
- `*ngSwitch`

```html
<div *ngIf="condition">Shown if true</div>

<ul>
    <li *ngFor="let item of items">{{ item }}</li>
</ul>
```

#### Attribute Directives
- `ngClass`
- `ngStyle`

```html
<div [ngClass]="{'active': isActive}">
<div [ngStyle]="{'color': textColor}">
```

## Services

### 1. What is a Service?
Services are singleton objects used for:
- Sharing data between components
- Implementing application logic
- External interactions (e.g., API calls)

```typescript
@Injectable({
    providedIn: 'root'
})
export class DataService {
    private data: any[] = [];

    getData() {
        return this.data;
    }

    addData(item: any) {
        this.data.push(item);
    }
}
```

## Routing

### 1. How do you implement routing?

```typescript
// app-routing.module.ts
const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'users', component: UsersComponent },
    { path: 'users/:id', component: UserDetailComponent },
    { path: '**', component: NotFoundComponent }
];

// Template usage
<router-outlet></router-outlet>
<a routerLink="/users">Users</a>
```

## Forms

### 1. What are the two types of forms?

#### Template-Driven Forms
```html
<form #userForm="ngForm" (ngSubmit)="onSubmit(userForm.value)">
    <input name="username" [(ngModel)]="user.name">
    <button type="submit">Submit</button>
</form>
```

#### Reactive Forms
```typescript
// Component
form = new FormGroup({
    username: new FormControl(''),
    password: new FormControl('')
});

// Template
<form [formGroup]="form" (ngSubmit)="onSubmit()">
    <input formControlName="username">
    <input formControlName="password">
</form>
```

## Lifecycle Hooks

### 1. What are the main lifecycle hooks?

```typescript
export class LifecycleComponent implements OnInit, OnDestroy {
    ngOnInit() {
        // Called after component is initialized
    }

    ngOnDestroy() {
        // Called just before component is destroyed
    }

    ngOnChanges(changes: SimpleChanges) {
        // Called when input property changes
    }

    ngDoCheck() {
        // Called during every change detection run
    }
}
```

## RxJS and Observables

### 1. What is RxJS used for in Angular?

```typescript
import { Observable } from 'rxjs';

@Component({
    // ...
})
export class ExampleComponent {
    data$: Observable<any>;

    constructor(private http: HttpClient) {
        this.data$ = this.http.get('/api/data').pipe(
            map(response => response.data),
            catchError(error => {
                console.error(error);
                return of([]);
            })
        );
    }
}
```

## Testing

### 1. How do you test Angular applications?

```typescript
describe('ExampleComponent', () => {
    let component: ExampleComponent;
    let fixture: ComponentFixture<ExampleComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ ExampleComponent ]
        }).compileComponents();

        fixture = TestBed.createComponent(ExampleComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
```

## Best Practices

1. Follow Angular Style Guide
2. Use proper component organization
3. Implement lazy loading for modules
4. Use TypeScript features effectively
5. Handle subscriptions properly
6. Write comprehensive tests
7. Use Angular CLI for development
8. Implement proper error handling
9. Follow proper naming conventions
10. Use Angular's built-in security features

## Performance Tips

1. Use OnPush change detection strategy
2. Implement trackBy function with ngFor
3. Lazy load modules
4. Use pure pipes
5. Optimize change detection
6. Minimize DOM manipulation
7. Use web workers for CPU-intensive tasks
8. Implement proper caching strategies
9. Use AOT compilation
10. Bundle size optimization
