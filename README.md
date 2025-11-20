#

# Logic - PetersonChecker

## Student Information
- **Full Name:** Juan Carlos Muñoz Trejos and Juan José Álvarez Ocampo
- **Class:** MT5008 and CM0845
- **Course:** Logic
- **Professor:** Sergio Steven Ramirez Rico 
- **Assignment:** Final Project

## Environment
- **Operating System:** macOS Tahoe 26.1 and Windows 11 24h2
- **Processor:** Apple Silicon M4, Ryzen 7 4800
- **Memory:** 16 GB RAM, 512 GB
- **Visual Studio Code Version:** 1.105.1
- **Python Version:** 3.9.6
- **Terminal:** zsh 5.9 (arm64-apple-darwin25.0), PowerShell 5.1


## Project Description 

**PetersonChecker** is a Python tool that models **Peterson’s mutual exclusion** algorithm (two processes) and verifies:
- **Safety (mutual exclusion):** `□¬(cs_p ∧ cs_q)`
- **Liveness (progress):** `□(wait_p → ◇cs_p)` and `□(wait_q → ◇cs_q)`

## Algorithm Description

- Model: Two automata (process P and Q) with local locations {try, set_turn, wait, critical, exit} and shared vars want_p, want_q, turn.
- Exploration: BFS generates all reachable interleavings from the initial state.
- Safety: ensure never cs_p ∧ cs_q (□¬(cs_p ∧ cs_q)).
- Liveness: detect SCC cycles where a process is forever in wait and never reaches cs (□(wait → ◇cs)); uses Tarjan.

## Repository Contents

- **main.py -** Code source
- **README.md -** Documentation file (this document).

## Step-by-Step Instructions to Run the Code

#### 1. Install Python 
If you have Python already installed, you can skip this step, but if you do not have Python installed, you can install Python [here.](https://www.python.org/downloads/)

After installation, verify with
```
python3 --version
```

Expected output
```
Python 3.9.6 
```
or instead of 3.9.6, your python version


#### 2. Clone the Repository

```
# Clone the Repository
git clone https://github.com/katals/entrega_final_logica.git
```

```
cd entrega_final_logica
```

```bash
# Run the program
python3 main.py
```

## Algorithm Explanation

The program models Peterson’s two-process protocol as a tiny state machine (each process has locations like try, wait, cs) with shared vars want_p, want_q, and turn. It systematically explores all interleavings from the initial state to build the reachable state graph. On that graph it checks:
- Safety: it ensures both processes are never in the critical section at the same time.
- Liveness: it looks for cycles where a process stays in wait and never reaches its critical section (using SCC detection).

If it finds a violation, it prints a counterexample trace (or bad cycle); otherwise it reports that Peterson’s algorithm passes both checks.


## How to Compile and Run

1. Open project folder in the terminal.

```powershell
PS C:\Users\USER\GitHub\entrega_final_logica>
```

2. Run the following command

```bash
python3 main.py
```

## Learning Outcome

This exercise demonstrates how to:
- Model concurrency as a finite-state transition system.
- Build a reachable state graph via BFS (all interleavings).
- Verify invariants (safety) and progress (liveness via SCC analysis).
- Produce counterexamples (error traces / bad cycles) when properties fail.
- Reason about fairness and state-space explosion limits.

## Troubleshooting (common issues)

**- python3 / py not found**
Install Python 3.10+ and re-open the terminal. Verify with python3 --version (macOS/Linux) or py -3 --version (Windows).

## Reference

- M. Ben-Ari, Mathematical Logic for Computer Science, Chapter 16 (Concurrent program verification).
