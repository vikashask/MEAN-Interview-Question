# JavaScript DOM (Document Object Model)

## DOM Selection Methods

### Basic Selectors
```javascript
// Get element by ID
const element = document.getElementById('myId');

// Get elements by class name
const elements = document.getElementsByClassName('myClass');

// Get elements by tag name
const divs = document.getElementsByTagName('div');

// Query selector (returns first match)
const firstMatch = document.querySelector('.myClass');

// Query selector all (returns all matches)
const allMatches = document.querySelectorAll('.myClass');
```

### Element Navigation
```javascript
// Parent node
const parent = element.parentNode;
const parentElement = element.parentElement;

// Child nodes
const children = element.childNodes;
const childElements = element.children;
const firstChild = element.firstChild;
const lastChild = element.lastChild;

// Siblings
const nextSibling = element.nextSibling;
const previousSibling = element.previousSibling;
const nextElement = element.nextElementSibling;
const previousElement = element.previousElementSibling;
```

## DOM Manipulation

### Creating Elements
```javascript
// Create new element
const div = document.createElement('div');

// Create text node
const text = document.createTextNode('Hello World');

// Create document fragment
const fragment = document.createDocumentFragment();
```

### Modifying Elements
```javascript
// Set inner HTML
element.innerHTML = '<span>New content</span>';

// Set text content
element.textContent = 'New text';

// Set attributes
element.setAttribute('class', 'newClass');
element.id = 'newId';
element.className = 'class1 class2';

// Add/Remove Classes
element.classList.add('newClass');
element.classList.remove('oldClass');
element.classList.toggle('active');
element.classList.contains('active');
```

### DOM Tree Modification
```javascript
// Append child
parent.appendChild(child);

// Insert before
parent.insertBefore(newChild, referenceChild);

// Replace child
parent.replaceChild(newChild, oldChild);

// Remove child
parent.removeChild(child);

// Remove self
element.remove();
```

## Events

### Event Handling
```javascript
// Add event listener
element.addEventListener('click', function(event) {
    console.log('Clicked!');
});

// Remove event listener
element.removeEventListener('click', handler);

// Prevent default behavior
element.addEventListener('submit', function(event) {
    event.preventDefault();
});

// Stop propagation
element.addEventListener('click', function(event) {
    event.stopPropagation();
});
```

### Common Events
```javascript
// Mouse events
element.addEventListener('click', handler);
element.addEventListener('dblclick', handler);
element.addEventListener('mouseenter', handler);
element.addEventListener('mouseleave', handler);
element.addEventListener('mousemove', handler);

// Keyboard events
element.addEventListener('keydown', handler);
element.addEventListener('keyup', handler);
element.addEventListener('keypress', handler);

// Form events
element.addEventListener('submit', handler);
element.addEventListener('change', handler);
element.addEventListener('input', handler);
element.addEventListener('focus', handler);
element.addEventListener('blur', handler);
```

## Styles and CSS

### Manipulating Styles
```javascript
// Inline styles
element.style.backgroundColor = 'red';
element.style.marginTop = '10px';
element.style.display = 'none';

// Get computed style
const style = window.getComputedStyle(element);
const bgColor = style.backgroundColor;

// CSS custom properties (variables)
element.style.setProperty('--my-var', 'blue');
const value = element.style.getPropertyValue('--my-var');
```

### Dimensions and Position
```javascript
// Element dimensions
const height = element.offsetHeight;
const width = element.offsetWidth;
const clientHeight = element.clientHeight;
const clientWidth = element.clientWidth;
const scrollHeight = element.scrollHeight;

// Position
const rect = element.getBoundingClientRect();
const top = rect.top;
const left = rect.left;

// Scroll position
const scrollTop = element.scrollTop;
const scrollLeft = element.scrollLeft;
```

## Forms

### Form Elements
```javascript
// Get form elements
const form = document.forms['myForm'];
const elements = form.elements;

// Access form fields
const username = form.elements['username'];
const email = form.elements['email'];

// Get/Set values
const value = username.value;
username.value = 'John';

// Check radio/checkbox
const isChecked = checkbox.checked;
checkbox.checked = true;
```

### Form Validation
```javascript
// Built-in validation
input.required = true;
input.pattern = '[A-Za-z]{3}';
input.minLength = 3;
input.maxLength = 10;

// Custom validation
input.setCustomValidity('Invalid input');
const isValid = input.checkValidity();
const validationMessage = input.validationMessage;
```

## Best Practices

1. Performance
   ```javascript
   // Use document fragments
   const fragment = document.createDocumentFragment();
   for (let i = 0; i < 1000; i++) {
       const div = document.createElement('div');
       fragment.appendChild(div);
   }
   document.body.appendChild(fragment);
   
   // Cache DOM queries
   const container = document.getElementById('container');
   ```

2. Event Delegation
   ```javascript
   // Instead of multiple listeners
   document.getElementById('list').addEventListener('click', function(e) {
       if (e.target.matches('li')) {
           // Handle list item click
       }
   });
   ```

3. Cross-Browser Compatibility
   ```javascript
   // Check for feature support
   if ('querySelector' in document) {
       // Use querySelector
   } else {
       // Fallback
   }
   ```

4. Memory Management
   ```javascript
   // Remove event listeners
   function cleanup() {
       element.removeEventListener('click', handler);
   }
   
   // Remove elements
   while (element.firstChild) {
       element.removeChild(element.firstChild);
   }
   ```

## Common Use Cases

### Dynamic Content Loading
```javascript
async function loadContent() {
    const response = await fetch('api/data');
    const data = await response.json();
    
    const container = document.getElementById('content');
    data.forEach(item => {
        const div = document.createElement('div');
        div.textContent = item.name;
        container.appendChild(div);
    });
}
```

### Form Handling
```javascript
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    try {
        const response = await fetch('/api/submit', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        showSuccess('Form submitted successfully');
    } catch (error) {
        showError('Error submitting form');
    }
});
```

### Dynamic Styling
```javascript
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', 
        document.body.classList.contains('dark-theme') ? 'dark' : 'light'
    );
}
```