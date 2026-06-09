# 19_benchmark_framework.md

# PURPOSE

Tài liệu này định nghĩa Benchmark Framework chính thức cho dự án.

Mục tiêu:

* So sánh thuật toán AI
* Đánh giá hiệu năng
* Đánh giá chất lượng quyết định
* Tạo kết quả có thể tái lập
* Hỗ trợ nghiên cứu học thuật

---

# 1. BENCHMARK PHILOSOPHY

---

Benchmark phải:

```text
Fair

Repeatable

Deterministic

Comparable
```

---

Không được:

```text
Random comparison

Different map conditions

Manual scoring
```

---

Rule

```text
All algorithms run on identical environments
```

---

# 2. BENCHMARK ARCHITECTURE

---

```text
Map Dataset

      │

      ▼

Algorithm Runner

      │

      ▼

Metrics Collector

      │

      ▼

Score Calculator

      │

      ▼

Ranking Engine

      │

      ▼

Benchmark Report
```

---

# 3. PARTICIPATING ALGORITHMS

---

Required

```text
BFS

DFS

UCS

Dijkstra

Greedy

A*
```

---

Future

```text
IDA*

D* Lite

Beam Search

Q-Learning

Deep RL
```

---

# 4. BENCHMARK DATASET

---

Dataset A

```text
Small Maps
```

---

Size

```python
10x10
```

---

Count

```python
20 maps
```

---

Dataset B

```text
Medium Maps
```

---

Size

```python
20x20
```

---

Count

```python
20 maps
```

---

Dataset C

```text
Large Maps
```

---

Size

```python
35x35
```

---

Count

```python
20 maps
```

---

Total

```python
60 maps
```

---

# 5. MAP REQUIREMENTS

---

Every map must contain:

```text
1 Robot

1+ Rescue Station

5+ Victims

1+ Fire Source
```

---

Connectivity

```text
Required
```

---

Rule

```text
All benchmark maps are frozen
```

---

# 6. EXECUTION RULES

---

For each map:

```text
Run BFS

Run DFS

Run UCS

Run Dijkstra

Run Greedy

Run A*
```

---

Rule

```text
Same seed

Same start state

Same fire schedule
```

---

# 7. COLLECTED METRICS

---

Metric 1

```python
execution_time_ms
```

---

Metric 2

```python
expanded_nodes
```

---

Metric 3

```python
path_cost
```

---

Metric 4

```python
path_length
```

---

Metric 5

```python
victims_saved
```

---

Metric 6

```python
victims_dead
```

---

Metric 7

```python
total_steps
```

---

Metric 8

```python
mission_success
```

---

# 8. PRIMARY SCORE

---

Formula

```python
score =

(victims_saved * 100)

-

(victims_dead * 50)

-

(total_steps * 0.5)
```

---

Purpose

```text
Reward rescue efficiency
```

---

# 9. SECONDARY SCORE

---

Formula

```python
speed_score =

1000 / execution_time_ms
```

---

Purpose

```text
Reward fast planning
```

---

# 10. SUCCESS RATE

---

Formula

```python
success_rate =

successful_runs

/

total_runs
```

---

Example

```python
54 / 60
```

---

Result

```python
90%
```

---

# 11. EFFICIENCY SCORE

---

Formula

```python
efficiency =

victims_saved

/

total_steps
```

---

Purpose

```text
Measure operational efficiency
```

---

# 12. RISK SCORE

---

Formula

```python
average_risk_encountered
```

---

Interpretation

```text
Lower is better
```

---

Purpose

```text
Measure safety
```

---

# 13. BENCHMARK REPORT

---

Required Columns

```text
Algorithm

Success Rate

Victims Saved

Victims Dead

Average Score

Average Time

Expanded Nodes

Average Risk
```

---

Example

```text
A*      95%

BFS     92%

UCS     91%

Greedy  89%

DFS     70%
```

---

# 14. RANKING SYSTEM

---

Sort Order

Priority 1

```text
Success Rate
```

---

Priority 2

```text
Average Score
```

---

Priority 3

```text
Average Risk
```

---

Priority 4

```text
Execution Time
```

---

# 15. BENCHMARK RUNNER

---

File

```text
app/benchmark/runner.py
```

---

Responsibilities

```text
Execute algorithms

Collect metrics

Generate reports
```

---

# 16. RESULT EXPORT

---

Supported Formats

```text
CSV

JSON

Markdown
```

---

Output Folder

```text
benchmark/results/
```

---

# 17. VISUALIZATION

---

Charts

```text
Success Rate Chart

Execution Time Chart

Victim Saved Chart

Risk Chart
```

---

Purpose

```text
Research presentation
```

---

# 18. RESEARCH VALIDITY

---

Requirement

```text
Deterministic execution
```

---

Requirement

```text
Repeatable results
```

---

Requirement

```text
Documented datasets
```

---

# 19. PERFORMANCE TARGETS

---

Benchmark Run

```python
< 5 minutes
```

for:

```text
60 maps

6 algorithms
```

---

# 20. SUCCESS CRITERIA

Benchmark Framework passes review when:

```text
Algorithms comparable

Results reproducible

Ranking stable

Metrics complete

Reports generated
```

---

# END OF FILE

File Number

```text
19_benchmark_framework.md
```

Next File

```text
20_project_structure_final.md
```

Purpose

```text
Final Folder Structure

Module Layout

Package Boundaries

Dependency Rules

Implementation Blueprint
```
