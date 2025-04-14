# 🧠 Math Expression Simplifier

Built in the summer of 2023

A symbolic simplifier that parses mathematical expressions into trees and applies a wide range of hand-coded transformation rules to explore both simplified and expanded forms of the expression.

---

## ✨ Features

- **Parses math expressions** with:
  - Numbers and variables (e.g., `x`, `y`)
  - Operators: `+`, `-`, `*`, `/`, `^`
  - Parentheses: `(...)`
  - Functions: `sin(...)`, `cos(...)`, `ln(...)`
  
- **Converts expressions into tree structures** for easier rule application.

- **Applies transformation rules** such as:
  - Constant folding (e.g., `2 + 3 → 5`)
  - Algebraic identities (e.g., `x * 1 → x`)
  - Expansion and factorization (e.g., `(x + 2)^2 → x^2 + 4x + 4`)
  - Function evaluation (e.g., `sin(0) → 0`)
  
- **Tracks and explores** all generated expressions from all applicable rules.

- **Outputs** both:
  - A **simplified** form (heuristically shortest or cleanest)
  - An **expanded** form (useful for understanding underlying transformations)

- With very basic web site for testing.

**⚠️ Note**
- Variables must be a single letter (e.g., x, a, z).

- Multiplication must be explicit. For example:

    ✅ 2 * a * b

    ❌ 2ab (not supported)
- If the solving fails, check server output for info.
---

## ⚙️ How It Works

1. **Parsing:**  
   The input expression is parsed into a tree, breaking down operators, variables, constants, and supported functions into individual nodes.

2. **Rule Application:**  
   A collection of manually-defined rules is applied to the parsed tree, including:
   - Simplifications (e.g., algebraic identities)
   - Various tree shifts and manipulations like:
   ```
        (+)                     (+)                  (+)
       /    \                 /     \               /   \
     (1)     (+)     ->     (a)     (+)       ->  (a)   (3)
            /   \                  /   \
         (a)     (2)             (2)    (1)
    ```
   - Know operations like: `(a/b)/(c/d)` -> `a*d/b*c`
   - Exponent operation: `x^a+x^b` = `x^(a+b)` etc...
   - Raising expression to power etc...
   - etc...


3. **Tree Exploration:**  
   Every transformation creates a new expression tree. The program recursively applies these rules to each new tree, exploring all possible rewrites.

4. **Result Selection:**  
   From the generated space of expression trees, the program selects:
   - A **simplified** form, which is heuristically considered the shortest
   - An **expanded** form, the most expanded form found

> ⚠️ **Note:** Defining "simplest" is challenging — the concept of simplicity varies. Whether an expression is "simplified" depends on context (e.g., algebraic manipulation vs. function evaluation). This is one of the primary challenges in this approach since a precise definition of an ideal form is elusive. Consequently, the expansion process explores various forms without a fixed endpoint and sense of right direction.

---


## 🧪 Example

**Input:**
a^(b + c) / a^b

**Output:**

- **Simplified:** `a ^ c`
- **Expanded:** `(1 / (a ^ b)) * (a ^ (b + c))`

---

## 🛠 Requirements

- Python **3.10+** is required
- Only library needed is flask, for the testing site.

---

## 🚧 Future Improvements

- **Rule Priorities and Cost-Based Ranking:**  
  Introducing a system for ranking transformations based on "cost" or priority could make the simplification process smarter.

- **User-Configurable Simplification Strategies:**  
  Allow users to define their preferred simplification rules or strategies.

- **Support for More Functions:**  
  Currently supports `sin`, `cos`, and `ln`. Future versions could include additional functions like `tan`, `log` and define operations above functions.

- **Smarter Tree Exploration:**  
  Enhance the tree exploration algorithm to avoid redundant transformations and reduce computation time.

- **Tree Hashing for Comparisons:**  
  Implement tree hashing to quickly identify and avoid revisiting already explored trees, improving efficiency.

---
