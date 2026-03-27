# TypeScript Modules Guide

## Module Basics

### Export Syntax
```typescript
// Named exports
export const PI = 3.14159;
export function calculateArea(radius: number): number {
    return PI * radius * radius;
}

// Default export
export default class Circle {
    constructor(public radius: number) {}
    
    getArea(): number {
        return calculateArea(this.radius);
    }
}
```

### Import Syntax
```typescript
// Named imports
import { PI, calculateArea } from './math';

// Default import
import Circle from './math';

// Rename imports
import { calculateArea as area } from './math';

// Import all as namespace
import * as MathUtils from './math';
```

## Module Organization

### Barrel Files (index.ts)
```typescript
// shapes/circle.ts
export class Circle {}

// shapes/rectangle.ts
export class Rectangle {}

// shapes/index.ts (barrel)
export * from './circle';
export * from './rectangle';

// Usage
import { Circle, Rectangle } from './shapes';
```

### Re-exports
```typescript
// Expose internal module
export { default as Utils } from './internal/utils';

// Re-export with different name
export { SomeClass as BaseClass } from './base';

// Re-export selected items
export { Item1, Item2 } from './items';
```

## Module Resolution

### Path Mapping
```typescript
// tsconfig.json
{
    "compilerOptions": {
        "baseUrl": ".",
        "paths": {
            "@app/*": ["src/app/*"],
            "@shared/*": ["src/shared/*"]
        }
    }
}

// Usage
import { SharedComponent } from '@shared/components';
import { UserService } from '@app/services';
```

### Module Resolution Strategies
```typescript
// tsconfig.json
{
    "compilerOptions": {
        "moduleResolution": "node",
        // or "classic"
    }
}
```

## Dynamic Imports

### Async Module Loading
```typescript
// Dynamic import
async function loadModule() {
    const module = await import('./dynamic-module');
    module.doSomething();
}

// With type checking
type Module = {
    doSomething(): void;
};

async function loadTypedModule() {
    const module = await import<Module>('./module');
    module.doSomething();
}
```

### Lazy Loading in Angular
```typescript
// app-routing.module.ts
const routes: Routes = [
    {
        path: 'feature',
        loadChildren: () => 
            import('./feature/feature.module')
            .then(m => m.FeatureModule)
    }
];
```

## Module Augmentation

### Extending Existing Modules
```typescript
// Original module
declare module "lodash" {
    interface LoDashStatic {
        customFunction(value: string): string;
    }
}

// Implementation
_.customFunction = (value: string) => {
    return value.toUpperCase();
};
```

### Global Augmentation
```typescript
declare global {
    interface String {
        toMyFormat(): string;
    }
}

String.prototype.toMyFormat = function() {
    return this.toLowerCase();
};
```

## Best Practices

### 1. Module Organization
```typescript
// Feature based organization
/src
    /features
        /users
            user.model.ts
            user.service.ts
            user.component.ts
            index.ts
        /products
            product.model.ts
            product.service.ts
            product.component.ts
            index.ts
```

### 2. Import Style
```typescript
// Prefer
import { Something } from './something';

// Instead of
import * as Everything from './everything';
```

### 3. Export Style
```typescript
// Prefer named exports
export class User {}
export interface UserData {}

// Use default export sparingly
export default class MainComponent {}
```

### 4. Type Exports
```typescript
// types.ts
export interface User {
    id: number;
    name: string;
}

export type UserRole = 'admin' | 'user';

// Usage
import type { User, UserRole } from './types';
```

## Common Patterns

### 1. Service Module
```typescript
// service.module.ts
export interface ServiceConfig {
    apiUrl: string;
    timeout: number;
}

export class Service {
    constructor(private config: ServiceConfig) {}
    
    async getData(): Promise<any> {
        // Implementation
    }
}
```

### 2. Feature Module
```typescript
// feature.module.ts
export interface FeatureConfig {
    enabled: boolean;
}

export * from './models';
export * from './services';
export * from './components';

export function initializeFeature(config: FeatureConfig) {
    // Implementation
}
```

### 3. Utility Module
```typescript
// utils.module.ts
export function formatDate(date: Date): string {
    // Implementation
}

export function parseDate(str: string): Date {
    // Implementation
}

export const DateUtils = {
    format: formatDate,
    parse: parseDate
};
```

## Error Handling

### Module Loading Errors
```typescript
async function loadModule() {
    try {
        const module = await import('./dynamic-module');
        return module;
    } catch (error) {
        console.error('Failed to load module:', error);
        throw error;
    }
}
```

### Type Safety
```typescript
// Ensure type safety in dynamic imports
type ModuleType = {
    default: typeof SomeClass;
    namedExport: string;
};

async function loadSafeModule() {
    const module = await import<ModuleType>('./module');
    return new module.default();
}
```