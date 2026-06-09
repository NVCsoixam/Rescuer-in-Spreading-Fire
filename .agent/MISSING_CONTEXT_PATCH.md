# MISSING_CONTEXT_PATCH.md

## Purpose

Bổ sung các ngữ cảnh còn thiếu từ UI Specification mới nhất.

File này KHÔNG ghi đè FINAL_CONTEXT_OVERRIDE.md.

Nếu có xung đột:

FINAL_CONTEXT_OVERRIDE.md ưu tiên cao hơn.

---

# 1. Environment Generator

Hệ thống không sinh map bằng random wall đơn giản.

Sử dụng:

Procedural Building Generator

## Supported Environment Types

* Apartment
* Office
* Hospital
* Warehouse
* Mixed

### Apartment

* nhiều phòng nhỏ
* hành lang ngắn

### Office

* không gian mở
* ít vách ngăn hơn

### Hospital

* hành lang dài
* nhiều phòng
* phù hợp nhất với bài toán cứu hộ

### Warehouse

* ít phòng
* nhiều vật cản

### Mixed

* kết hợp ngẫu nhiên nhiều phong cách

---

# 2. Complexity System

Map generator hỗ trợ:

* Low
* Medium
* High

Complexity ảnh hưởng:

* số phòng
* số cửa
* số giao lộ
* độ dài hành lang
* mật độ vật cản

Ví dụ:

Low:
ít phòng
ít ngõ cụt

Medium:
cân bằng

High:
nhiều phòng
nhiều nhánh
nhiều giao lộ

---

# 3. Random Seed

Map Generator phải hỗ trợ Random Seed.

Ví dụ:

12345

hoặc

Auto

Mục đích:

* benchmark thuật toán
* debug
* tái tạo map
* nghiên cứu AI

Cùng seed phải sinh cùng map.

---

# 4. Fire Speed Presets

Ngoài Fire Interval dạng milliseconds.

UI có thể cung cấp preset:

Very Fast
Fast
Normal
Slow
Very Slow

Mapping:

Very Fast = 500 ms

Fast = 750 ms

Normal = 1000 ms

Slow = 1500 ms

Very Slow = 3000 ms

Lưu ý:

Backend vẫn sử dụng milliseconds.

Preset chỉ là lớp UI.

---

# 5. Current Target

STATUS có thể hiển thị:

Current Target

Ví dụ:

Victim #5

hoặc

Rescue Station #2

Mục đích:

giúp người xem hiểu AI đang hướng tới đâu.

---

# 6. Rescue Rate

STATUS có thể hiển thị:

Rescue Rate

Công thức:

RescueRate =
saved_victims /
total_victims
× 100

Ví dụ:

80%

Đây là chỉ số hiển thị.

Không ảnh hưởng logic mô phỏng.

---

# 7. Tooltip Metadata

Các thuật toán nên có metadata.

Ví dụ:

BFS

Optimal: Yes

Heuristic: No

DFS

Optimal: No

Memory Usage: Low

Greedy

Optimal: No

Uses Heuristic: Yes

A*

Optimal: Yes

Uses Heuristic: Yes

Mục đích:

hỗ trợ trình diễn đồ án.

---

# 8. Formal State Machine

State machine chuẩn:

READY

USER_MODE

BFS
DFS
UCS
DIJKSTRA
GREEDY
ASTAR

PAUSED

MISSION_COMPLETE

MISSION_FAILED

Tất cả UI chỉ phản ánh state hiện tại.

Không tự quản lý trạng thái riêng.

---

# 9. Connectivity Validation

Sau khi sinh map:

BFS Validation phải chạy.

Kiểm tra:

* robot reachable
* victim reachable
* rescue reachable

Nếu tỷ lệ reachable thấp:

Regenerate.

Không chấp nhận map bị khóa cứng.

---

# 10. Placement Rules

Robot:

ưu tiên gần rescue station.

Victims:

ưu tiên trong phòng.

Fire Sources:

ưu tiên trong phòng.

Rescue Stations:

ưu tiên gần biên hoặc lối thoát.

Mục tiêu:

tăng tính thực tế của môi trường cứu hộ.

---

# 11. Benchmark Support

Map Generator phải hỗ trợ:

* same seed
* same environment type
* same complexity

để so sánh:

BFS
DFS
UCS
Dijkstra
Greedy
A*

một cách công bằng.

---

# 12. Project Positioning

Đây không phải Maze Solver.

Định nghĩa chính thức:

AI Rescue & Fire Simulation System

Core Features:

* Procedural Building Generation
* Fire Propagation
* Victim Rescue
* Manual Control
* Multi-Algorithm Benchmark
* Real-Time Statistics Dashboard

Mọi quyết định thiết kế nên phục vụ định hướng này.
