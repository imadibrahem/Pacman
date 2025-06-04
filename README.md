
# Pacman AI Project – Phase B

**Course**: Introduction to AI – CS487, Fall 2021  
**Deadline**: 18/01/2022

## Overview

This project is based on the Berkeley Pacman AI project. It allows students to apply various AI techniques, including:

- Informed and uninformed search
- Multi-agent decision-making
- Reflex agents
- Probabilistic inference

The visualizations and modular structure support experimentation with intelligent agents in the classic Pacman game.

---

## General Instructions

### Getting Started

1. Play classic Pacman:
   ```bash
   python pacman.py
   ```

2. Run the Reflex Agent:
   ```bash
   python pacman.py -p ReflexAgent
   ```

3. Test on a layout:
   ```bash
   python pacman.py -p ReflexAgent -l testClassic
   ```

---

## 🔍 Questions

### Question 1: Reflex Agent

- Improve the `ReflexAgent` in `multiAgents.py`.
- Your agent should perform well in:
  ```bash
  python pacman.py -p ReflexAgent -l testClassic
  python pacman.py --frameTime 0 -p ReflexAgent -k 1
  python pacman.py --frameTime 0 -p ReflexAgent -k 2
  ```

#### Grading:
- 0 points if it never wins or times out.
- Up to 4 points based on wins and average score on `openClassic`.

---

### Question 2: Minimax Agent

- Implement `MinimaxAgent` in `multiAgents.py`.
- Should support any number of ghosts.
- Score leaves using `self.evaluationFunction`.

#### Test:
```bash
python autograder.py -q q2
```

---

### Question 3: Alpha-Beta Pruning

- Implement `AlphaBetaAgent` with proper pruning.
- Maintain child order and avoid pruning on equality.

#### Test:
```bash
python autograder.py -q q3
```

---

### Question 4: Expectimax

- Implement `ExpectimaxAgent` to model ghost randomness.
- Assume ghosts choose actions uniformly at random.

#### Test:
```bash
python autograder.py -q q4
```

---

### Question 5: Better Evaluation Function

- Improve `betterEvaluationFunction` to evaluate game states.
- Should win >5 out of 10 games on `smallClassic` and score well.

#### Test:
```bash
python autograder.py -q q5
```

---

## 💡 Tips & Observations

- Use reciprocal distances to food and ghosts.
- Design evaluation as a weighted sum of meaningful features.
- Randomness can make testing hard — use `-f` to fix the seed.
- Disable graphics for faster tests:
  ```bash
  python pacman.py -q ...
  ```

---

## 📦 Submission Instructions

Only submit `multiAgents.py`.  
Do **not** modify or submit other files.

---

## 🛑 Academic Honesty

Your code will be checked for plagiarism. Submissions with copied or slightly modified code will be flagged. Please submit your own work only.

---

## License

This project is adapted from the UC Berkeley Pacman projects.
