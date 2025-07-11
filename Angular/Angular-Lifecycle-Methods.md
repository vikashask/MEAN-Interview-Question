# Angular Component Lifecycle Methods

## Overview

Angular components go through different lifecycle phases from initialization to destruction. Each phase has an associated hook method that you can implement to tap into these phases.

## Lifecycle Hooks in Order

### 1. ngOnChanges
```typescript
interface OnChanges {
    ngOnChanges(changes: SimpleChanges): void;
}

// Implementation
ngOnChanges(changes: SimpleChanges) {
    // Called before ngOnInit and when data-bound property changes
    for (let property in changes) {
        let change = changes[property];
        let current  = JSON.stringify(change.currentValue);
        let previous = JSON.stringify(change.previousValue);
        console.log(`${property}: currentValue = ${current}, previousValue = ${previous}`);
    }
}
```

### 2. ngOnInit
```typescript
interface OnInit {
    ngOnInit(): void;
}

// Implementation
ngOnInit() {
    // Called once after the first ngOnChanges
    // Perfect for initialization logic
    this.loadUserData();
    this.setupSubscriptions();
}
```

### 3. ngDoCheck
```typescript
interface DoCheck {
    ngDoCheck(): void;
}

// Implementation
ngDoCheck() {
    // Called during every change detection run
    // Use for custom change detection
    if (this.hero.name !== this.oldHeroName) {
        this.changeDetected = true;
        this.oldHeroName = this.hero.name;
    }
}
```

### 4. ngAfterContentInit
```typescript
interface AfterContentInit {
    ngAfterContentInit(): void;
}

// Implementation
ngAfterContentInit() {
    // Called once after the first ngDoCheck
    // Component content has been initialized
    console.log('Content projection complete');
    this.contentInitialized = true;
}
```

### 5. ngAfterContentChecked
```typescript
interface AfterContentChecked {
    ngAfterContentChecked(): void;
}

// Implementation
ngAfterContentChecked() {
    // Called after ngAfterContentInit and every subsequent ngDoCheck
    // Check content projection changes
    if (this.projected !== this.oldProjected) {
        this.contentChanged = true;
        this.oldProjected = this.projected;
    }
}
```

### 6. ngAfterViewInit
```typescript
interface AfterViewInit {
    ngAfterViewInit(): void;
}

// Implementation
ngAfterViewInit() {
    // Called once after ngAfterContentChecked
    // Component views are initialized
    this.setupViewElements();
    this.initializeCharts();
}
```

### 7. ngAfterViewChecked
```typescript
interface AfterViewChecked {
    ngAfterViewChecked(): void;
}

// Implementation
ngAfterViewChecked() {
    // Called after ngAfterViewInit and every subsequent ngAfterContentChecked
    // Check for view updates
    if (this.viewElement.offsetHeight !== this.oldHeight) {
        this.oldHeight = this.viewElement.offsetHeight;
        this.updateLayout();
    }
}
```

### 8. ngOnDestroy
```typescript
interface OnDestroy {
    ngOnDestroy(): void;
}

// Implementation
ngOnDestroy() {
    // Called before component is destroyed
    // Clean up subscriptions, event handlers, etc.
    this.subscription.unsubscribe();
    this.eventEmitter.complete();
    clearInterval(this.timerInterval);
}
```

## Common Use Cases

### 1. Data Initialization
```typescript
export class UserProfileComponent implements OnInit {
    user: User;
    
    constructor(private userService: UserService) {}
    
    ngOnInit() {
        this.userService.getUser()
            .subscribe(user => this.user = user);
    }
}
```

### 2. Watching Input Changes
```typescript
export class ChildComponent implements OnChanges {
    @Input() data: any;
    
    ngOnChanges(changes: SimpleChanges) {
        if (changes.data) {
            if (changes.data.firstChange) {
                this.initialSetup(changes.data.currentValue);
            } else {
                this.handleDataUpdate(
                    changes.data.previousValue,
                    changes.data.currentValue
                );
            }
        }
    }
}
```

### 3. Clean Up Resources
```typescript
export class DataComponent implements OnInit, OnDestroy {
    private subscription: Subscription;
    private intervalId: number;
    
    ngOnInit() {
        this.subscription = this.dataService
            .getData()
            .subscribe(data => this.handleData(data));
            
        this.intervalId = setInterval(() => {
            this.checkUpdates();
        }, 1000);
    }
    
    ngOnDestroy() {
        if (this.subscription) {
            this.subscription.unsubscribe();
        }
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    }
}
```

## Best Practices

### 1. Implement Interfaces
```typescript
// Good Practice
export class MyComponent implements OnInit, OnDestroy {
    ngOnInit() { /* ... */ }
    ngOnDestroy() { /* ... */ }
}

// Avoid
export class MyComponent {
    ngOnInit() { /* ... */ }  // No interface implementation
}
```

### 2. Order of Operations
```typescript
export class OrderedComponent implements OnInit, AfterViewInit, OnDestroy {
    constructor() {
        // Only basic initializations
        // Avoid HTTP calls or complex logic
    }
    
    ngOnInit() {
        // Data initialization
        // HTTP calls
        // Complex computations
    }
    
    ngAfterViewInit() {
        // DOM manipulations
        // Third-party library initializations
    }
    
    ngOnDestroy() {
        // Cleanup
    }
}
```

### 3. Performance Considerations
```typescript
export class PerformantComponent implements DoCheck {
    @Input() items: any[];
    private previousLength: number;
    
    ngDoCheck() {
        // Efficient checking
        if (this.items.length !== this.previousLength) {
            this.previousLength = this.items.length;
            this.handleItemsChange();
        }
    }
}
```

### 4. Error Handling
```typescript
export class RobustComponent implements OnInit {
    ngOnInit() {
        try {
            this.initializeData();
        } catch (error) {
            console.error('Initialization failed:', error);
            this.handleError(error);
        }
    }
    
    private async initializeData() {
        try {
            const data = await this.dataService.getData();
            this.processData(data);
        } catch (error) {
            throw new Error(`Data initialization failed: ${error.message}`);
        }
    }
}
```

### 5. Content Projection Checks
```typescript
export class ContentComponent implements AfterContentChecked {
    @ContentChild(ChildComponent) child: ChildComponent;
    private previousChildState: string;
    
    ngAfterContentChecked() {
        // Efficient content checking
        if (this.child && this.child.state !== this.previousChildState) {
            this.previousChildState = this.child.state;
            this.handleChildStateChange();
        }
    }
}
```
