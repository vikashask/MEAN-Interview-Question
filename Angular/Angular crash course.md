# Angular Crash Course

## Core Concepts

### Components
Components are the building blocks of Angular applications. They contain:
* Template (HTML)
* Class (TypeScript/JavaScript)
* Metadata (Decorators)

```typescript
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'My App';
}
```

### Modules
Modules are containers for a cohesive block of code:
* Root module (`AppModule`)
* Feature modules
* Shared modules

```typescript
@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

### Data Binding

#### One-way Data Binding
* Interpolation: `{{ value }}`
* Property Binding: `[property]="value"`
* Event Binding: `(event)="handler()"`

#### Two-way Data Binding
```html
<input [(ngModel)]="name">
```

### Directives

#### Structural Directives
* `*ngIf="condition"`
* `*ngFor="let item of items"`
* `*ngSwitch`

#### Attribute Directives
* `ngClass`
* `ngStyle`
* `ngModel`

### Services & Dependency Injection
Services are used for sharing data and functionality:

```typescript
@Injectable({
  providedIn: 'root'
})
export class DataService {
  getData() {
    return ['item1', 'item2'];
  }
}
```

### Routing
Configure routes in your application:

```typescript
const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'about', component: AboutComponent },
  { path: '**', component: NotFoundComponent }
];
```

### Forms

#### Template-driven Forms
```html
<form #myForm="ngForm" (ngSubmit)="onSubmit(myForm)">
  <input name="username" [(ngModel)]="user.name">
  <button type="submit">Submit</button>
</form>
```

#### Reactive Forms
```typescript
form = new FormGroup({
  username: new FormControl(''),
  password: new FormControl('')
});
```

### HTTP Client
Making HTTP requests:

```typescript
@Injectable()
export class UserService {
  constructor(private http: HttpClient) { }

  getUsers() {
    return this.http.get('/api/users');
  }
}
```

## Best Practices

### Performance Optimization
* Use OnPush change detection
* Lazy loading modules
* Pure pipes
* Track by function in ngFor

### Code Organization
* Feature modules
* Shared modules
* Core module
* Lazy loading
* Proper file naming

### Testing
* Unit tests with Jasmine
* End-to-end tests with Protractor
* Component testing
* Service testing

## Step 1: Install the Angular CLI
    npm install -g @angular/cli

## Step 2: Create a workspace and initial application
    ng new my-app

## Step 3: Serve the application
    cd my-app
    ng serve --open
    ng serve --o

## Create the heroes component
   ng generate component heroes

## Two-way binding
    [(ngModel)]="hero.name"

## Display hero list
    <li *ngFor="let hero of heroes">

## click event binding
    <li *ngFor="let hero of heroes" (click)="onSelect(hero)">

## Hide empty details with *ngIf
    <div *ngIf="selectedHero">

## @Input() hero property
    <app-hero-detail [hero]="selectedHero"></app-hero-detail>

## Create the HeroService
    ng generate service hero
    @Injectable() services
## Add the AppRoutingModule
    ng generate module app-routing --flat --module=app
    --flat puts the file in src/app instead of its own folder.
    --module=app tells the CLI to register it in the imports array of the AppModule

