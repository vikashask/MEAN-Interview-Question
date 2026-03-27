# Modules & npm

## CommonJS vs ES Modules

```javascript
// CommonJS (default in Node.js)
const express = require("express");
const { sum } = require("./utils");

module.exports = { sum, multiply };
module.exports.PI = 3.14;

// ES Modules (with .mjs or "type": "module" in package.json)
import express from "express";
import { sum } from "./utils.js";

export { sum, multiply };
export const PI = 3.14;
export default MyClass;
```

## require() & import

```javascript
// require() - synchronous, can be called anywhere
const config = require("./config");
const utils = require("./utils");

// Dynamic require
const moduleName = process.env.MODULE;
const module = require(`./${moduleName}`);

// import - static, must be at top level
import config from "./config.js";
import { sum } from "./utils.js";

// Dynamic import (async)
const module = await import(`./${moduleName}.js`);
```

## Module Caching

```javascript
// Modules are cached after first require
const utils1 = require("./utils");
const utils2 = require("./utils");
console.log(utils1 === utils2); // true - same instance

// Clear cache (rarely needed)
delete require.cache[require.resolve("./utils")];
const utils3 = require("./utils"); // Fresh instance
```

## package.json

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "My Node.js application",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "tsc"
  },
  "dependencies": {
    "express": "^4.18.0",
    "mongoose": "^7.0.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.0",
    "jest": "^29.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## npm Commands

```bash
# Install dependencies
npm install
npm install --save express          # Add to dependencies
npm install --save-dev jest         # Add to devDependencies
npm install -g nodemon              # Global install

# Update packages
npm update
npm update express                  # Update specific package

# Remove packages
npm uninstall express
npm uninstall -D jest

# Check for vulnerabilities
npm audit
npm audit fix

# List installed packages
npm list
npm list --depth=0                  # Top-level only

# Version management
npm version patch                   # 1.0.0 → 1.0.1
npm version minor                   # 1.0.0 → 1.1.0
npm version major                   # 1.0.0 → 2.0.0
```

## Semantic Versioning

```json
{
  "express": "4.18.0", // Exact version
  "express": "^4.18.0", // Compatible with 4.x (allows 4.18.1, 4.19.0)
  "express": "~4.18.0", // Compatible with 4.18.x (allows 4.18.1, not 4.19.0)
  "express": ">=4.18.0", // Greater than or equal
  "express": "4.18.0 - 5.0.0" // Range
}
```

## Creating & Publishing Modules

```javascript
// my-module/index.js
const sum = (a, b) => a + b;
const multiply = (a, b) => a * b;

module.exports = { sum, multiply };

// my-module/package.json
{
  "name": "my-math-module",
  "version": "1.0.0",
  "main": "index.js",
  "keywords": ["math", "sum", "multiply"],
  "author": "Your Name",
  "license": "MIT"
}

// Publish to npm
npm login
npm publish

// Use in another project
npm install my-math-module
const { sum } = require('my-math-module');
```

## Monorepo with npm Workspaces

```json
{
  "name": "my-monorepo",
  "workspaces": ["packages/api", "packages/cli", "packages/shared"]
}
```

```bash
# Install dependencies for all workspaces
npm install

# Run script in specific workspace
npm run start -w packages/api

# Add dependency to workspace
npm install lodash -w packages/api
```

## .npmrc Configuration

```
# ~/.npmrc
registry=https://registry.npmjs.org/
@myorg:registry=https://registry.mycompany.com/
//registry.mycompany.com/:_authToken=YOUR_TOKEN
always-auth=true
```

## Useful npm Packages

```javascript
// Utilities
const lodash = require("lodash");
const moment = require("moment");
const uuid = require("uuid");

// Environment variables
const dotenv = require("dotenv");
dotenv.config();

// Validation
const joi = require("joi");
const yup = require("yup");

// HTTP client
const axios = require("axios");

// Logging
const winston = require("winston");
const pino = require("pino");
```
