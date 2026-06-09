# 07_algorithm_benchmarks.md

# PURPOSE

Tài liệu này định nghĩa framework chuẩn để đánh giá các thuật toán AI trong hệ thống.

Mục tiêu:

* So sánh công bằng
* Reproducible
* Deterministic
* Có thể mở rộng cho các thuật toán tương lai

---

# 1. BENCHMARK PRINCIPLES

---

## RULE-001

Mọi thuật toán phải chạy trên:

```text id="b001"
Same map

Same victims

Same fire sources

Same rescue stations

Same random seed
```

---

## RULE-002

Không được thay đổi:

```text id="b002"
Map layout

Risk map

Initial state
```

---

## RULE-003

Mỗi lần benchmark:

```text id="b003"
Reset snapshot

Run algorithm

Collect metrics

Store result
```

---

# 2. SUPPORTED ALGORITHMS

---

## ALG-001

Breadth First Search

```text id="b004"
BFS
```

Characteristics

```text id="b005"
Complete

Optimal (uniform cost)

Memory expensive
```

---

## ALG-002

Depth First Search

```text id="b006"
DFS
```

Characteristics

```text id="b007"
Fast memory usage

Not optimal

May explore bad branches
```

---

## ALG-003

Uniform Cost Search

```text id="b008"
UCS
```

Characteristics

```text id="b009"
Optimal

Supports weighted costs
```

---

## ALG-004

Dijkstra

```text id="b010"
Dijkstra
```

Characteristics

```text id="b011"
Optimal

Weighted shortest path
```

---

## ALG-005

Greedy Best First Search

```text id="b012"
Greedy
```

Characteristics

```text id="b013"
Fast

Often non-optimal
```

---

## ALG-006

A*

```text id="b014"
AStar
```

Characteristics

```text id="b015"
Optimal

Efficient

Risk-aware extension possible
```

---

# 3. METRICS

---

## METRIC-001

Execution Time

Unit

```text id="b016"
Milliseconds
```

---

Formula

```python id="b017"
end_time - start_time
```

---

Purpose

```text id="b018"
Speed comparison
```

---

## METRIC-002

Expanded Nodes

Definition

```text id="b019"
Number of explored states
```

---

Purpose

```text id="b020"
Search efficiency
```

---

## METRIC-003

Path Length

Definition

```text id="b021"
Number of movement steps
```

---

Formula

```python id="b022"
len(path)
```

---

## METRIC-004

Path Cost

Definition

```text id="b023"
Accumulated movement cost
```

---

Formula

```python id="b024"
sum(edge_costs)
```

---

## METRIC-005

Victims Saved

Definition

```text id="b025"
Total rescued victims
```

---

## METRIC-006

Victims Dead

Definition

```text id="b026"
Total victims burned
```

---

## METRIC-007

Mission Success

Values

```python id="b027"
True

False
```

---

# 4. BENCHMARK RESULT DTO

---

## DTO-001

BenchmarkResult

```python id="b028"
@dataclass
class BenchmarkResult:

    algorithm: str

    success: bool

    execution_time_ms: float

    expanded_nodes: int

    path_length: int

    path_cost: float

    victims_saved: int

    victims_dead: int

    total_steps: int
```

---

# 5. TEST SCENARIOS

---

## SCENARIO-001

Small Map

Size

```python id="b029"
10x10
```

---

Entities

```python id="b030"
1 robot

3 victims

1 rescue station

1 fire source
```

---

Purpose

```text id="b031"
Basic correctness
```

---

## SCENARIO-002

Medium Map

Size

```python id="b032"
20x20
```

---

Entities

```python id="b033"
1 robot

5 victims

2 rescue stations

2 fire sources
```

---

Purpose

```text id="b034"
Normal workload
```

---

## SCENARIO-003

Large Map

Size

```python id="b035"
35x35
```

---

Entities

```python id="b036"
1 robot

10 victims

3 rescue stations

4 fire sources
```

---

Purpose

```text id="b037"
Stress test
```

---

# 6. DYNAMIC FIRE BENCHMARK

---

## SCENARIO-004

Fire Expansion Test

Goal

```text id="b038"
Measure adaptation ability
```

---

Procedure

```text id="b039"
Compute path

Spread fire

Recompute path

Continue mission
```

---

Metrics

```text id="b040"
Replanning time

Path changes

Mission outcome
```

---

# 7. FAIRNESS RULES

---

## RULE-004

Same Seed

```python id="b041"
random.seed(SEED)
```

---

## RULE-005

Same Start State

```text id="b042"
Snapshot restored before run
```

---

## RULE-006

Same Hardware

```text id="b043"
Same machine

Same runtime
```

---

## RULE-007

No Parallel Execution

Reason

```text id="b044"
Avoid timing distortion
```

---

# 8. PERFORMANCE TARGETS

---

## TARGET-001

BFS

20x20 map

```text id="b045"
< 100 ms
```

---

## TARGET-002

DFS

20x20 map

```text id="b046"
< 100 ms
```

---

## TARGET-003

UCS

20x20 map

```text id="b047"
< 150 ms
```

---

## TARGET-004

Dijkstra

20x20 map

```text id="b048"
< 150 ms
```

---

## TARGET-005

Greedy

20x20 map

```text id="b049"
< 100 ms
```

---

## TARGET-006

A*

20x20 map

```text id="b050"
< 100 ms
```

---

# 9. SCORE FORMULA

---

## SCORE-001

Benchmark Score

```python id="b051"
score =

(
    victims_saved * 100
)

-
(
    victims_dead * 100
)

-
(
    path_cost
)

-
(
    execution_time_ms * 0.1
)
```

---

Purpose

```text id="b052"
Leaderboard ranking
```

---

# 10. VISUALIZATION CONTRACT

---

UI Table

Columns

```text id="b053"
Algorithm

Success

Time

Expanded Nodes

Path Length

Path Cost

Saved

Dead

Score
```

---

Sort

```text id="b054"
Highest score first
```

---

# 11. FUTURE ALGORITHMS

Reserved

```text id="b055"
IDA*

Beam Search

Bidirectional BFS

D* Lite

RRT

Genetic Search

Q-Learning

Deep RL
```

---

Requirement

```text id="b056"
Must implement PathResult contract
```

---

# 12. SUCCESS CRITERIA

Benchmark system is complete when:

```text id="b057"
All algorithms executable

Results reproducible

Metrics consistent

Ranking deterministic

UI displays comparison
```

---

# END OF FILE

File Number

```text id="b058"
07_algorithm_benchmarks.md
```

Next File

```text id="b059"
08_test_plan.md
```

Purpose

```text id="b060"
Full QA strategy

Unit testing

Integration testing

Stress testing

Performance testing

Regression testing

Acceptance testing
```
