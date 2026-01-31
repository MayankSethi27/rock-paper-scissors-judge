# AI Judge for Rock-Paper-Scissors-Plus

## Overview

This project implements an AI-powered judge for a modified Rock-Paper-Scissors game that includes a special **“bomb”** move.  
The core focus of this assignment is **prompt engineering**, not hard-coded game logic.

The AI Judge is responsible for:
- Interpreting free-form user input
- Validating moves against the game rules
- Deciding round outcomes
- Clearly explaining every decision

Minimal Python code is used only to manage state and interact with the model.

---

## Why This Approach?

Instead of writing complex if-else logic to handle every possible user input, I designed prompts that allow the AI to:

- Understand natural language inputs  
  (e.g., “I’ll go with rock” vs “rock” vs “let’s use rock”)
- Validate moves based on game rules
- Enforce constraints like “bomb can only be used once”
- Explain decisions clearly
- Handle ambiguous and invalid inputs gracefully

This demonstrates how well-crafted prompts can replace traditional rule-based programming in conversational agents.

---

## Game Rules

1. **Valid Moves**: rock, paper, scissors, bomb  
2. **Standard RPS Rules**:
   - Rock beats Scissors
   - Scissors beats Paper
   - Paper beats Rock
3. **Bomb Rules**:
   - Bomb beats Rock, Paper, and Scissors
   - Each player can use bomb only **once per game**
   - Bomb vs Bomb → Draw
4. **Invalid or Unclear Moves**:
   - Waste the turn (no winner for that round)

---

## Architecture & Design Decisions

The solution is intentionally divided into three logical responsibilities.

---

### 1. Intent Understanding  
**What did the user try to do?**

The AI interprets natural language input and determines the intended move.

Examples:
- `rock` → VALID  
- `I choose rock` → VALID  
- `rokc` → VALID (typo handled)  
- `maybe rock?` → UNCLEAR  
- `rock and paper` → UNCLEAR  

**Why this approach?**
- Real user input is messy
- Hard-coding all variations is impractical
- The AI can reason about ambiguity better than rigid rules

---

### 2. Game Logic Validation  
**Is the move allowed? Who won the round?**

The AI checks:
- Whether the move is valid
- Whether constraints are violated (e.g., bomb reuse)
- The outcome against the bot’s move

All rules are enforced via the **system prompt**, not procedural code.

**Why prompt-driven logic?**
- Rules are transparent and explainable
- Changing rules only requires prompt updates
- The AI can explain *why* a move is invalid or unclear

---

### 3. Response Generation  
**What should the user see next?**

The AI returns structured JSON including:
- Round number
- Interpreted move
- Move status (VALID / INVALID / UNCLEAR)
- Bot move
- Round winner
- Clear explanation

Structured output ensures consistency and easy parsing.

---

## Prompt Design Rationale

The system prompt is structured into clear sections:

1. **Role Definition**  
   Establishes the AI as a neutral judge.

2. **Explicit Game Rules**  
   Ensures consistent and correct decision-making.

3. **Task Breakdown**  
   Separates:
   - Intent understanding
   - Validation
   - Judgment
   - Explanation  

   This helps the model reason step by step.

4. **Strict Output Format**  
   The AI must return valid JSON only, ensuring predictability and explainability.

---

## Edge Cases Considered

- Ambiguous language (e.g., “maybe rock?”)
- Questions instead of moves (e.g., “can I use bomb?”)
- Multiple moves in one input
- Repeated bomb usage
- Unrelated or nonsensical input
- Natural language phrasing and typos

Invalid or unclear inputs always waste the turn.

---

## Constraints

- No databases or UI
- Minimal state stored in memory
- No heavy rule-based logic in code
- Decision-making handled primarily through prompts

---

## What I Would Improve Next

- Add confidence scoring for intent interpretation
- Improve recovery from malformed model output
- Move bot strategy reasoning into the AI Judge
- Extend the judge to support additional game rules dynamically
