# FINAL_CONTEXT_OVERRIDE.md

## Purpose

Tài liệu này ghi đè (override) các quyết định thiết kế cũ nếu có mâu thuẫn giữa các tài liệu trong repository.

Ưu tiên áp dụng:

1. FINAL_CONTEXT_OVERRIDE.md
2. Latest approved discussion summary
3. Technical specifications
4. Older design documents

Nếu có mâu thuẫn, luôn sử dụng quy định trong file này.

---

# 1. Fire System (FINAL)

## Previous ambiguity

Một số tài liệu mô tả FIRE_INTERVAL theo số tick hoặc số bước mô phỏng.

## Final decision

Fire Interval được hiểu là thời gian thực (milliseconds).

### Default

1000 ms

### Valid Range

0 → 10000 ms

### UI

Map Settings:

* Fire Interval

Ví dụ:

* 500 ms
* 1000 ms
* 2000 ms
* 5000 ms

### Behavior

Cứ mỗi Fire Interval:

* fire spread update
* heat map update
* risk map update

Fire không phụ thuộc số bước robot.

Robot và fire hoạt động độc lập theo thời gian.

---

# 2. Run Mode (FINAL)

## Previous ambiguity

Một số tài liệu có:

* Start
* Resume
* Execute

## Final decision

KHÔNG có nút Start.

Khi người dùng bấm:

* BFS
* DFS
* UCS
* Dijkstra
* Greedy
* A*

=> thuật toán chạy ngay lập tức.

### Allowed buttons

RUN MODE:

* USER MODE
* BFS
* DFS
* UCS
* Dijkstra
* Greedy
* A*

CONTROL:

* Pause
* Reset

Không có:

* Start
* Run
* Execute
* Resume

---

# 3. Mission Rules (FINAL)

Robot chỉ được mang:

1 victim

tại một thời điểm.

Quy trình:

Robot
→ tìm victim
→ nhặt victim
→ mang tới rescue station
→ thả victim
→ quay lại tìm victim tiếp theo

Chỉ khi victim được thả tại rescue station:

saved_count++

---

# 4. Default Map Configuration (FINAL)

### Default map size

20 x 20

### Allowed map size

* 10 x 10
* 15 x 15
* 20 x 20
* 25 x 25
* 30 x 30
* 35 x 35

### Default generated entities

Robot:

* 1

Victims:

* 5

Rescue Stations:

* 3

Fire Sources:

* 1

---

# 5. Map Generation (FINAL)

Không sử dụng:

* random noise walls
* random wall per cell

Sử dụng:

* room clusters
* corridors
* building-like layouts

Requirements:

* map connectivity validation
* robot reachable
* victim reachable
* rescue reachable

Nếu không hợp lệ:

generate again

---

# 6. Heat Map / Risk Map (FINAL)

Heat Map là thành phần chính của AI.

Mỗi cell có risk score.

Ví dụ:

0-20 Safe

21-40 Warning

41-60 Medium Risk

61-80 High Risk

81-100 Critical

100+ Fire

AI không chỉ tránh fire.

AI phải tránh risk zones.

---

# 7. A* Evaluation Function (FINAL)

Base:

f(n) = g(n) + h(n)

Project version:

f(n) = g(n) + h(n) + risk(n)

Where:

g(n):
travel cost

h(n):
Manhattan heuristic

risk(n):
heat map penalty

A* là thuật toán trọng tâm của dự án.

---

# 8. Mission Success / Failure (FINAL)

## Success

remaining_victims == 0

Không còn nạn nhân trên bản đồ.

## Failure

robot_dead == true

Robot bị cháy.

Không sử dụng:

* 70% rescued
* score threshold
* time threshold

---

# 9. Sidebar Layout (FINAL)

## MAP SETTINGS

* Map Size
* Fire Interval
* Generate Random Map

## EDIT MODE

* Robot
* Victim
* Fire
* Wall
* Rescue
* Erase

## RUN MODE

* USER MODE
* BFS
* DFS
* UCS
* Dijkstra
* Greedy
* A*

## CONTROL

* Pause
* Reset

## STATUS

Hiển thị:

* Mode
* Saved
* Dead
* Remaining
* Steps
* Time
* Carrying

---

# 10. Status Panel (FINAL)

Status panel đồng thời là:

* runtime monitor
* final result screen

Không cần:

* result popup
* separate summary panel

Final states:

MISSION COMPLETE

hoặc

MISSION FAILED

---

# 11. Re-planning Requirement (MANDATORY)

Khi fire spread:

* update heat map
* update risk map

Nếu current path không còn hợp lệ:

* discard path
* recompute path
* continue mission

Mọi thuật toán AI phải hỗ trợ re-planning.

---

# 12. Single Source of Truth

Nếu bất kỳ tài liệu nào mâu thuẫn với file này:

FINAL_CONTEXT_OVERRIDE.md thắng.

Agent phải coi đây là nguồn sự thật cuối cùng của dự án.
