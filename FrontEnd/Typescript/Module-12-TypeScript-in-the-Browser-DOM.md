# 📦 Module 12: TypeScript in the Browser (DOM)

🟡 **Intermediate**

## 12.1 DOM Element Types

DOM queries return broad or nullable types by default.

```typescript
const el = document.getElementById("app");   // HTMLElement | null
const inp = document.querySelector(".email"); // Element | null
```

## 12.2 Narrowing and Asserting DOM Elements

```typescript
// Type Assertion
const btn = document.getElementById("submit-btn") as HTMLButtonElement;
btn.disabled = true; // ✅

// Generic querySelector (preferred)
const input = document.querySelector<HTMLInputElement>("#email");
if (input) { console.log(input.value); } // ✅

// instanceof check
const canvas = document.getElementById("canvas");
if (canvas instanceof HTMLCanvasElement) {
  const ctx = canvas.getContext("2d"); // ✅
}
```

## 12.3 Typing Events

```typescript
const form = document.querySelector<HTMLFormElement>("#login-form")!;

form.addEventListener("submit", (e: SubmitEvent) => {
  e.preventDefault();
  const data = new FormData(e.target as HTMLFormElement);
  console.log(data.get("email"));
});

document.addEventListener("click", (e: MouseEvent) => {
  console.log(e.clientX, e.clientY);
});
```

## 12.4 Common DOM Types

| Element | TypeScript Type |
| :--- | :--- |
| `<input>` | `HTMLInputElement` |
| `<button>` | `HTMLButtonElement` |
| `<form>` | `HTMLFormElement` |
| `<canvas>` | `HTMLCanvasElement` |
| `<select>` | `HTMLSelectElement` |
| `<div>` | `HTMLDivElement` |
| `<a>` | `HTMLAnchorElement` |

---

## ⚡ Key Takeaways — Module 12

- DOM queries return broad/nullable types — narrow or assert
- Use `querySelector<HTMLInputElement>()` for typed queries
- Event listeners receive typed events: `MouseEvent`, `KeyboardEvent`, `SubmitEvent`

---

## ✅ Checklist — Module 12

- [ ] I understand why DOM queries return broad types
- [ ] I can use type assertions and generic `querySelector<T>`
- [ ] I can type DOM event listeners
- [ ] I know common HTML element type names

---
