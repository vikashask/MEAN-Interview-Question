# Angular CLI Commands Reference

## Project Creation and Setup

### New Project
```bash
# Create new Angular project
ng new project-name

# Create with specific options
ng new project-name --routing --style=scss

# Create without installing dependencies
ng new project-name --skip-install
```

### Development Server
```bash
# Start development server
ng serve

# Start with specific port
ng serve --port 4201

# Open browser automatically
ng serve --open

# Use production configuration
ng serve --configuration=production
```

## Generating Components

### Components and Modules
```bash
# Generate component
ng generate component my-component
ng g c my-component

# Generate module
ng generate module my-module
ng g m my-module

# Generate component in specific module
ng g c my-module/my-component

# Generate with specific options
ng g c my-component --skip-tests --flat
```

### Services and Guards
```bash
# Generate service
ng generate service my-service
ng g s my-service

# Generate guard
ng generate guard my-guard
ng g g my-guard

# Generate resolver
ng generate resolver my-resolver
ng g r my-resolver
```

### Other Generators
```bash
# Generate directive
ng g directive my-directive

# Generate pipe
ng g pipe my-pipe

# Generate interface
ng g interface my-interface

# Generate enum
ng g enum my-enum
```

## Building and Testing

### Build Commands
```bash
# Production build
ng build --configuration=production

# Development build
ng build

# Build with specific configuration
ng build --configuration=staging

# Build with stats
ng build --stats-json
```

### Testing Commands
```bash
# Run unit tests
ng test

# Run e2e tests
ng e2e

# Run tests with code coverage
ng test --code-coverage

# Run specific test file
ng test --include=**/my.component.spec.ts
```

## Project Analysis

### Linting
```bash
# Run linting
ng lint

# Fix linting issues
ng lint --fix

# Lint specific files
ng lint my-project --files="src/**/*.ts"
```

### Dependency Analysis
```bash
# Show dependency graph
ng dep-graph

# Check for circular dependencies
ng lint --rules-dir=circular-deps
```

## Configuration

### Adding Dependencies
```bash
# Add Angular Material
ng add @angular/material

# Add PWA support
ng add @angular/pwa

# Add third-party library
ng add @ng-bootstrap/ng-bootstrap
```

### Update Commands
```bash
# Check for updates
ng update

# Update specific packages
ng update @angular/core @angular/cli

# Update with force
ng update --force
```

## Workspace Commands

### Multiple Projects
```bash
# Generate library
ng generate library my-lib

# Build library
ng build my-lib

# Generate application
ng generate application my-app
```

### Project Configuration
```bash
# Configure project
ng config projects.my-app.architect.build.options.outputPath dist/my-app

# Get configuration value
ng config projects.my-app.prefix

# Set global configuration
ng config -g cli.warnings.versionMismatch false
```

## Best Practices

1. Project Structure
   ```bash
   # Generate feature module
   ng g m features/my-feature --routing
   
   # Generate component in feature
   ng g c features/my-feature/components/my-component
   ```

2. Lazy Loading
   ```bash
   # Generate lazy-loaded module
   ng g m features/my-feature --route my-feature --module app.module
   ```

3. Testing Setup
   ```bash
   # Generate component with tests
   ng g c my-component --spec
   
   # Generate service with tests
   ng g s my-service --spec
   ```

## Common Options

### Global Options
- `--dry-run`: Show what would be generated
- `--skip-tests`: Skip creating spec files
- `--skip-import`: Skip importing component in module
- `--project`: Specify project for generation

### Component Options
- `--prefix`: Specify selector prefix
- `--style`: Specify style file extension
- `--change-detection`: Specify change detection strategy
- `--view-encapsulation`: Specify view encapsulation strategy

### Build Options
- `--aot`: Ahead of Time compilation
- `--optimization`: Enable optimization
- `--source-map`: Generate source maps
- `--watch`: Watch for changes

