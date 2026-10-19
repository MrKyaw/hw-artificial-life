# Artificial Life — Evolving Robots, Morphologies & Brains

**Northwestern University · CS396 Artificial Life · Coursework + Final Project**

[![Course](https://img.shields.io/badge/course-CS396%20Artificial%20Life-6A5ACD)](#)
[![Simulation](https://img.shields.io/badge/simulation-PyBullet-0E7C7B)](#)
[![Method](https://img.shields.io/badge/method-evolutionary%20algorithms-1F6FEB)](#)
[![Python](https://img.shields.io/badge/python-3.x-3776AB)](#)

> Can a robot evolve a body and a brain that work together? These experiments answer with a two-level evolutionary algorithm — morphology on the outside, control on the inside — and a menagerie of creatures that learn to hop, climb, crawl, and snake across challenging terrain.

---

## Overview

This repository collects the assignments and final project for **CS396 Artificial Life** at **Northwestern University**, authored by **Qinjie Lin**. Every experiment uses physics simulation (PyBullet / Pyrosim) and evolutionary computation to explore the boundary between morphology and behaviour.

The work spans three threads:

1. **Course assignments (5–8)** — progressively richer creature generators, from hand-designed virus-shaped robots and 1D snakes to branching 3D bodies with evolved controllers.
2. **Final project** — *Evolving Robots for Challenging Environments: Morphology Optimization for Versatile Locomotion*, a two-level EA that co-optimizes body and brain across four environments.
3. **GPT-2 project** — a compact language-model fine-tuning pipeline (data download → preprocessing → tokenizer → training → evaluation) built alongside the course.

The original, full final-project write-up — with method figures, teaser GIFs, and experiment discussion — is preserved in **[FINAL_PROJECT.md](FINAL_PROJECT.md)**.

---

## Repository Map

| Path | What it contains |
|---|---|
| `Assignment5/` | **Design your own creatures** — virus-shaped robot evolved to climb steps |
| `Assignment6/` | **Random 1D morphologies** — jointed, motorized, sensorized snakes |
| `Assignment7/` | **3D morphospace** — branching lizards and horses, not just snakes |
| `Assignment8/` | **Morphology + behaviour** — parallel hill climber for locomotion |
| `final/` | **Final project** — two-level EA over four challenging environments |
| `gpt/` | **GPT-2 fine-tuning project** — preprocessing, training, inference |
| `FINAL_PROJECT.md` | Full original write-up with figures, results, and notes |

---

## Final Project — Evolving Robots for Challenging Environments

**Thesis.** Animals are versatile because their bodies and controllers co-evolved. Task-specific robots are not. This project asks whether a **two-level evolutionary algorithm** can discover morphologies that generalize across rough terrain, obstacles, steps, and bumper jumps.

### Method

```text
Level 1 — Morphology EA
  population of bodies (tree-structured links, joints, sensors)
        │  each body is scored by…
        ▼
Level 2 — Brain EA
  evolve a controller for that body; fitness = final X position
        │
        ▼
  best brain fitness becomes the body's fitness → next morphology generation
```

- **Body representation:** a tree of links (sphere / box), joints (revolute / fixed / spherical), sizes, and sensor placement.
- **Brain:** a fully connected linear controller evolved by parallel hill climbing.
- **Fitness:** distance travelled along **X** in the physics simulation.
- **Environments:** `obstacle`, `step`, `terrain`, `bumper`.
- **Scale:** **200,000 simulations** = 4 environments × 5 seeds × 10 morphology population × 20 morphology generations × 10 brain population × 5 brain generations.

### What emerged

| Environment | Evolved behaviour | Animal analogue |
|---|---|---|
| Bumper | Jumping over obstacles | Kangaroo |
| Step | Climbing ledges | Mountain goat |
| Terrain | Low, flexible crawling | Insect / snake |
| Obstacle | Agile navigation | Crawling insect |

Because every environment starts from the **same seed and the same first generation**, the divergence in final morphologies is evidence that **the environment shapes the body**.

### Run and replay

```bash
cd final

# Run the two-level EA (opens many parallel simulations)
python search_morphology.py --seed 1234 --env terrain

# Replay the best evolved body + brain
python replay_brain.py --brain best --urdf best --seed 1234 --env terrain

# Compare against a random body + random brain
python replay_brain.py --brain random --urdf random --seed 1234 --env terrain
```

> The search launches a large number of parallel simulations. Reduce `population_size` in `final/ea_brain/constants.py` and `final/ea_morphology/constants.py` on smaller machines.

---

## Course Assignments

| Assignment | Goal | Fitness | Entry point |
|---|---|---|---|
| **5** | Design a virus-shaped creature that climbs steps | `Z + X` position | `Assignment5/search.py` |
| **6** | Generate random 1D snake morphologies with sensors | `-X` position (crawl) | `Assignment6/search.py` |
| **7** | Expand the morphospace to 3D branching bodies | `X` position | `Assignment7/search.py` |
| **8** | Co-design morphology and behaviour for locomotion | `X` position | `Assignment8/search_morphology.py` |

Each assignment ships a `replay.py` (or `replay_brain.py`) for watching the best and random creatures side by side.

> Assignments 5 and 6 were written for **~60 CPUs** (`numberOfGenerations` × `populationSize`). Lower those constants if you are running locally.

---

## GPT-2 Fine-Tuning Project

The `gpt/` folder is a self-contained language-model pipeline:

```text
gpt/
├── main.py                     # training entry point
├── preprocess.py               # dataset construction
├── train.ipynb / evaluate.ipynb
└── src/
    ├── data_preprocessing/     # downloader, transformer, tokenizer
    ├── model/                  # GPT-2 model, trainer, inference
    └── utils/                  # data + seed helpers
```

- **Model:** `gpt2` via Hugging Face `transformers`
- **Training:** `Trainer` + `TrainingArguments`, 3 epochs, batch size 4, `max_length=512`
- **Artifacts:** checkpoint and fine-tuned model written under `gpt/data/`

```bash
cd gpt
python main.py
```

---

## Quickstart

### Prerequisites

- Python 3.8+
- PyBullet (install with `pip install pybullet`)
- Pyrosim (bundled under `final/pyrosim/`)
- For the GPT project: `torch`, `transformers`, `numpy`

### Replay a final-project result

```bash
cd final

python replay_brain.py --brain best   --urdf best   --env bumper  --seed 4444
python replay_brain.py --brain best   --urdf best   --env step    --seed 3333
python replay_brain.py --brain best   --urdf best   --env obstacle --seed 2222
python replay_brain.py --brain best   --urdf best   --env terrain  --seed 3333
```

### Experimental batch runs

`final/run.sh` contains the seed × environment sweep used for the reported experiments. It is a template — edit the seed and environment lists before running.

---

## Tech Stack

**Simulation** · PyBullet · Pyrosim · URDF · SDF
**Evolution** · parallel hill climbing · tree-structured morphology encoding · mutation / selection
**Learning** · fully connected linear controllers · PyTorch · Hugging Face Transformers · GPT-2
**Tooling** · Python · NumPy · Matplotlib · Jupyter

**Tags:** `artificial-life` · `evolutionary-algorithms` · `neuroevolution` · `robotics` · `morphology-optimization` · `pybullet` · `parallel-hill-climbing` · `gpt2` · `northwestern-university`

---

## Notes and Limitations

- Morphology mutation occasionally fails to produce structural change; the encoding is the main debugging frontier.
- Some generated morphologies separate at joints during simulation.
- Assignment runtime assumes a large CPU pool; the constants are deliberately easy to scale down.
- This repository is a **fork** of [QinjieLin-NU/hw-artificial-life](https://github.com/QinjieLin-NU/hw-artificial-life). The original coursework, write-up, and results are the upstream author's work.

## Attribution

Original author: **Qinjie Lin**, Northwestern University CS396 — Artificial Life.
Upstream repository: <https://github.com/QinjieLin-NU/hw-artificial-life>

References cited by the project include *Evolving 3D Morphology and Behavior by Competition*, *Evolving Virtual Creatures*, and the [Ludobots](https://www.reddit.com/r/ludobots/) course.

---

## ⭐ Star this repo if you find it useful! ⭐

Report Bug · Request Feature · Ask Question
