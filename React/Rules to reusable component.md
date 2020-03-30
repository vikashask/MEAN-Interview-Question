#  Rules to reusable component

## 1. Components should be small and easy to read.
## 2. Use prop-types package to structure and validate the props of your components.
## 3. For styled components, do not include any functional details, instead pass ## them as props.
## 4. For container components, do not include UI details, instead let the children ## styled components take care of them
## 5. Prefer functional components vs class-based components.
## 6. Prefer CSS in JS strategy for styled components for better maintainability.
## 7. UI variations should be coming in as configurable props whereas data should ## be coming up as part of global state like Redux or React Context.
## 8. Don’t repeat sections wherever it can be avoided, instead use arrays to store ## those section details and loop over them.
## 9. For components, add comments only wherever absolutely necessary (to indicate ## a hack or workaround for a bug).
## 10. For library utilities (pure functions), write JS-Doc comments.
## 11. Avoid using anonymous component wherever possible.
## 12. All files for a component should be part of the same folder.
## 13. Always use eslint and prettier for keeping your code clean and formatted.
## 14. Use ES6 features.
