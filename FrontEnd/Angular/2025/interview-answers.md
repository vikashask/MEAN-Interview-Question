# Angular Interview Questions and Answers 2025

## 1. What is SPA?
**Answer:**
A Single Page Application (SPA) is a web application that loads a single HTML page and dynamically updates the content as the user interacts with it, without refreshing the entire page.

**Key characteristics:**
- Loads all necessary HTML, CSS, and JavaScript in the initial load
- Dynamic updates without full page reloads
- Smooth user experience with faster transitions
- Better performance after initial load
- Works offline with proper PWA implementation

**Examples of SPAs:**
- Gmail
- Facebook
- Twitter
- Google Maps

## 2. What are pros and cons of Angular compared to React?

**Pros of Angular:**
1. Complete Framework
   - Full-featured framework with everything built-in
   - Official CLI for project generation
   - Built-in form validation
   - Dependency Injection system
   - RxJS integration

2. Strong Structure
   - Enforced architectural patterns
   - Consistent code organization
   - TypeScript by default
   - Better for large enterprise applications

3. Two-way Data Binding
   - Automatic sync between model and view
   - Reduced boilerplate code
   - Easier to implement forms

**Cons of Angular:**
1. Steeper Learning Curve
   - More concepts to learn
   - Complex syntax
   - TypeScript requirement

2. Heavier Bundle Size
   - Larger initial download
   - Slower first page load

3. Less Flexible
   - Opinionated framework
   - More rigid structure
   - Less freedom in implementation choices

## 3. How does Angular work?

**Core Components:**
1. **Modules (NgModules)**
   - Container for related components, directives, pipes, and services
   - Root module (AppModule) bootstraps the application

2. **Components**
```typescript
@Component({
    selector: 'app-root',
    template: '<h1>{{title}}</h1>'
})
export class AppComponent {
    title = 'My App';
}
```

3. **Templates**
   - HTML with Angular-specific syntax
   - Bindings and directives

4. **Data Binding**
   - Interpolation: {{value}}
   - Property binding: [property]="value"
   - Event binding: (event)="handler()"
   - Two-way binding: [(ngModel)]="value"

**Working Process:**
1. Bootstrap process starts with main.ts
2. Angular creates component tree
3. Change detection monitors data changes
4. View updates automatically when data changes

## 4. Sharing data between components in Angular

There are several ways to share data between components:

1. **Parent to Child: @Input()**
```typescript
// Parent Component
<app-child [data]="parentData"></app-child>

// Child Component
export class ChildComponent {
    @Input() data: any;
}
```

2. **Child to Parent: @Output() and EventEmitter**
```typescript
// Child Component
export class ChildComponent {
    @Output() dataEvent = new EventEmitter<string>();
    
    sendData() {
        this.dataEvent.emit('Hello from child');
    }
}

// Parent Component
<app-child (dataEvent)="handleData($event)"></app-child>
```

3. **Using Services**
```typescript
@Injectable({
    providedIn: 'root'
})
export class DataService {
    private data = new BehaviorSubject<string>('');
    currentData = this.data.asObservable();

    updateData(newData: string) {
        this.data.next(newData);
    }
}
```

4. **Using @ViewChild**
```typescript
export class ParentComponent {
    @ViewChild(ChildComponent) child: ChildComponent;
    
    ngAfterViewInit() {
        console.log(this.child.someProperty);
    }
}
```

## 5. What ways of binding in Angular do you know?

1. **Interpolation (One-way)**
```html
<h1>{{title}}</h1>
```

2. **Property Binding (One-way)**
```html
<img [src]="imageUrl">
<button [disabled]="isDisabled">Click me</button>
```

3. **Event Binding**
```html
<button (click)="onClick()">Click me</button>
<input (input)="onInput($event)">
```

4. **Two-way Binding**
```html
<input [(ngModel)]="name">
```

5. **Attribute Binding**
```html
<div [attr.aria-label]="labelText">Content</div>
```

6. **Class Binding**
```html
<div [class.active]="isActive">Content</div>
```

7. **Style Binding**
```html
<div [style.color]="textColor">Colored text</div>
```

## 6. What is HTML in Angular?

Angular HTML is an extended version of regular HTML with additional features:

1. **Template Syntax**
   - Interpolation: {{expression}}
   - Property binding: [property]
   - Event binding: (event)
   - Two-way binding: [(ngModel)]

2. **Directives**
   - Structural directives: *ngIf, *ngFor
   - Attribute directives: ngClass, ngStyle
   - Custom directives

3. **Pipes**
```html
<p>{{date | date:'short'}}</p>
<p>{{price | currency:'USD'}}</p>
```

4. **Template Reference Variables**
```html
<input #myInput>
<button (click)="logValue(myInput.value)">Log</button>
```

## 7. What are services in Angular?

Services are classes that handle data and logic that should be shared across components:

**Key Points:**
1. Singleton instances (by default when provided in root)
2. Used for:
   - Data sharing
   - Business logic
   - External interactions (HTTP calls)
   - Reusable functionality

**Example:**
```typescript
@Injectable({
    providedIn: 'root'
})
export class UserService {
    private apiUrl = 'api/users';

    constructor(private http: HttpClient) { }

    getUsers() {
        return this.http.get<User[]>(this.apiUrl);
    }

    addUser(user: User) {
        return this.http.post<User>(this.apiUrl, user);
    }
}
```

## 8. How to make HTTP Request in Angular?

Steps to make HTTP requests:

1. **Import HttpClientModule**
```typescript
import { HttpClientModule } from '@angular/common/http';

@NgModule({
    imports: [HttpClientModule]
})
export class AppModule { }
```

2. **Create a Service**
```typescript
@Injectable({
    providedIn: 'root'
})
export class ApiService {
    constructor(private http: HttpClient) { }

    getData() {
        return this.http.get('api/data');
    }

    postData(data: any) {
        return this.http.post('api/data', data);
    }

    updateData(id: number, data: any) {
        return this.http.put(`api/data/${id}`, data);
    }

    deleteData(id: number) {
        return this.http.delete(`api/data/${id}`);
    }
}
```

3. **Use in Component**
```typescript
export class MyComponent implements OnInit {
    constructor(private apiService: ApiService) { }

    ngOnInit() {
        this.apiService.getData()
            .pipe(
                catchError(error => {
                    console.error('Error:', error);
                    return EMPTY;
                })
            )
            .subscribe(data => {
                console.log('Data:', data);
            });
    }
}
```

## 9. How does dependency injection work?

Dependency Injection (DI) is a design pattern where dependencies are "injected" into components rather than created within them.

**Key Concepts:**
1. **Injector Hierarchy**
   - Root injector
   - Module injectors
   - Component injectors

2. **Provider Configuration**
```typescript
@Injectable({
    providedIn: 'root' // Application-wide singleton
})

// OR in module
@NgModule({
    providers: [MyService]
})

// OR in component
@Component({
    providers: [MyService] // Component-level instance
})
```

3. **Injection Tokens**
```typescript
const CONFIG = new InjectionToken<AppConfig>('app.config');

// Providing value
providers: [
    { provide: CONFIG, useValue: defaultConfig }
]

// Injecting
constructor(@Inject(CONFIG) private config: AppConfig) { }
```

## 10. How to use a router in Angular?

1. **Configure Routes**
```typescript
const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'about', component: AboutComponent },
    { path: 'users/:id', component: UserComponent },
    { path: '**', component: NotFoundComponent }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
```

2. **Router Outlet**
```html
<router-outlet></router-outlet>
```

3. **Navigation**
```html
<!-- Template -->
<a [routerLink]="['/about']">About</a>
<a [routerLink]="['/users', userId]">User Details</a>
```

```typescript
// Component
constructor(private router: Router) { }

navigate() {
    this.router.navigate(['/about']);
    // OR with parameters
    this.router.navigate(['/users', userId]);
}
```

## 11. What are life cycle hooks in Angular?

Angular components go through different lifecycle phases. Here are the main lifecycle hooks in order:

1. **ngOnChanges**
   - Called when input property changes
   - Receives SimpleChanges object

2. **ngOnInit**
   - Called once after first ngOnChanges
   - Used for initialization logic

3. **ngDoCheck**
   - Called during every change detection run
   - Used for custom change detection

4. **ngAfterContentInit**
   - Called after content projection
   - Called once after first ngDoCheck

5. **ngAfterContentChecked**
   - Called after content has been checked
   - Called after ngAfterContentInit and every ngDoCheck

6. **ngAfterViewInit**
   - Called after component's view initialization
   - Safe to work with view children

7. **ngAfterViewChecked**
   - Called after view has been checked
   - Called after ngAfterViewInit and every ngDoCheck

8. **ngOnDestroy**
   - Called before component destruction
   - Used for cleanup (unsubscribing from observables)

## 12. What are ViewChild and ViewChildren in Angular?

**ViewChild** and **ViewChildren** are decorators that allow a parent component to access child elements.

1. **ViewChild**
```typescript
export class ParentComponent {
    @ViewChild(ChildComponent) childComponent: ChildComponent;
    @ViewChild('myTemplate') myTemplate: TemplateRef<any>;

    ngAfterViewInit() {
        // Access child component properties/methods
        this.childComponent.someMethod();
    }
}
```

2. **ViewChildren**
```typescript
export class ParentComponent {
    @ViewChildren(ChildComponent) children: QueryList<ChildComponent>;

    ngAfterViewInit() {
        this.children.forEach(child => {
            child.someMethod();
        });
    }
}
```

## 13. Constructor vs NgOnInit in Angular - what is the difference?

**Constructor:**
- Part of TypeScript/JavaScript class
- Called when class is instantiated
- Used for dependency injection
- Shouldn't contain complex logic
- Runs before all lifecycle hooks

```typescript
constructor(private service: MyService) {
    // Only basic initialization and DI
}
```

**ngOnInit:**
- Angular lifecycle hook
- Called after constructor
- Called after input properties are set
- Used for component initialization
- Access to input properties
- Place for complex initialization logic

```typescript
export class MyComponent implements OnInit {
    @Input() data: any;

    constructor(private service: MyService) { }

    ngOnInit() {
        // Complex initialization logic
        this.service.getData().subscribe(result => {
            this.processData(result);
        });
    }
}
```

## 14. Unsubscribe in Angular - why is it important?

Unsubscribing from observables is crucial to prevent memory leaks in Angular applications.

**Why Important:**
1. Prevents memory leaks
2. Avoids unexpected behavior
3. Improves application performance
4. Prevents multiple subscription executions

**Ways to Unsubscribe:**

1. **Manual Unsubscribe**
```typescript
export class MyComponent implements OnDestroy {
    private subscription: Subscription;

    ngOnInit() {
        this.subscription = this.service.getData()
            .subscribe(data => {
                // Handle data
            });
    }

    ngOnDestroy() {
        if (this.subscription) {
            this.subscription.unsubscribe();
        }
    }
}
```

2. **Using async pipe**
```html
<div *ngIf="data$ | async as data">
    {{data}}
</div>
```

3. **Using takeUntil**
```typescript
export class MyComponent implements OnDestroy {
    private destroy$ = new Subject<void>();

    ngOnInit() {
        this.service.getData()
            .pipe(takeUntil(this.destroy$))
            .subscribe(data => {
                // Handle data
            });
    }

    ngOnDestroy() {
        this.destroy$.next();
        this.destroy$.complete();
    }
}
```

4. **Using take(1) for one-time subscriptions**
```typescript
this.service.getData()
    .pipe(take(1))
    .subscribe(data => {
        // Handle data
    });
```