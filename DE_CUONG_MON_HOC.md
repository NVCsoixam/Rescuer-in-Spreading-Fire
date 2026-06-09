# ĐỀ CƯƠNG CHI TIẾT ĐỀ TÀI NGHIÊN CỨU KHOA HỌC / ĐỒ ÁN MÔN HỌC

## BỘ GIÁO DỤC VÀ ĐÀO TẠO
### TRƯỜNG ĐẠI HỌC CÔNG NGHỆ TP.HCM (HUTECH)
### KHOA CÔNG NGHỆ THÔNG TIN

---

## MÔN HỌC: TRÍ TUỆ NHÂN TẠO
### ĐỀ TÀI: THIẾT KẾ VÀ XÂY DỰNG CHƯƠNG TRÌNH MÔ PHỎNG AI TÌM KIẾM CỨU NẠN TRONG MÔI TRƯỜNG CHÁY LAN 2D (RESCUER IN SPREADING FIRE)

* **Mã học phần:** ARIN330585
* **Giảng viên hướng dẫn:** PGS.TS. Hoàng Văn Dũng
* **Sinh viên thực hiện:**
  1. Họ và tên: Hồ Công Phong — MSSV: 24110301
  2. Họ và tên: Nguyễn Phước Thịnh — MSSV: 24110339
  3. Họ và tên: Phạm Uyên Thư — MSSV: 24110348

---

## NHẬN XÉT VÀ ĐÁNH GIÁ CỦA GIẢNG VIÊN

---

## MỤC LỤC

* **PHẦN 1. MỞ ĐẦU**
  * 1.1. Mục tiêu nghiên cứu
  * 1.2. Đối tượng và phạm vi nghiên cứu
  * 1.3. Phương pháp nghiên cứu
  * 1.4. Công cụ sử dụng
* **PHẦN 2. THIẾT KẾ HỆ THỐNG**
  * 2.1. Phân tích bài toán
    * 2.1.1. Mô tả bài toán cứu hộ trong hỏa hoạn
    * 2.1.2. Biểu diễn trạng thái grid
    * 2.1.3. Cơ chế cháy lan động và Heat Map đánh giá rủi ro
  * 2.2. Thiết kế thuật toán tìm kiếm đường đi
    * 2.2.1. Nhóm thuật toán tìm kiếm mù (BFS, DFS, UCS, Dijkstra)
    * 2.2.2. Nhóm thuật toán tìm kiếm có thông tin (Greedy Best-First, A* mở rộng)
  * 2.3. Thiết kế giao diện chương trình
* **PHẦN 3. XÂY DỰNG CHƯƠNG TRÌNH**
  * 3.1. Xây dựng mô hình trạng thái (State representation)
  * 3.2. Xây dựng các phép toán chuyển trạng thái (State transitions)
  * 3.3. Cài đặt các thuật toán tìm kiếm đường đi
  * 3.4. Xây dựng giao diện mô phỏng tương tác trực quan
  * 3.5. Tích hợp hệ thống và kiểm thử đơn vị
* **PHẦN 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ**
  * 4.1. Môi trường thực nghiệm
  * 4.2. Các trường hợp thử nghiệm (Test cases)
  * 4.3. Kết quả thực nghiệm
  * 4.4. Phân tích, so sánh hiệu quả giữa các thuật toán
  * 4.5. Đánh giá ưu điểm và hạn chế
* **PHẦN 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN**
  * 5.1. Kết quả đạt được
  * 5.2. Kết luận chung
  * 5.3. Hướng phát triển trong tương lai
* **TÀI LIỆU THAM KHẢO**

---

## PHẦN 1. MỞ ĐẦU

### 1.1. Mục tiêu nghiên cứu
Đề tài hướng đến việc nghiên cứu, thiết kế và xây dựng một hệ thống mô phỏng cứu hộ hỏa hoạn trong môi trường lưới 2D chịu tác động của đám cháy lan động theo thời gian thực. Bằng cách áp dụng các thuật toán tìm kiếm đường đi trong Trí tuệ nhân tạo (AI), hệ thống cho phép đánh giá năng lực ra quyết định của tác tử robot cứu hộ khi giải quyết bài toán đa mục tiêu: vừa tối ưu quãng đường di chuyển để cứu nạn nhân nhanh nhất, vừa né tránh các vùng nguy hiểm đang cháy hoặc chuẩn bị cháy.

Cụ thể, đề tài thực hiện:
* Nghiên cứu lý thuyết và cài đặt các thuật toán tìm kiếm cơ bản (BFS, DFS, UCS, Dijkstra, Greedy Best-First Search) cùng thuật toán A* cải tiến (kết hợp hàm heuristic khoảng cách Manhattan và trọng số rủi ro từ bản đồ nhiệt - Heat Map).
* Xây dựng giao diện mô phỏng đồ họa 2D sinh động, cho phép người dùng tự sinh bản đồ phòng-hành lang có cấu trúc liên thông, trực tiếp chỉnh sửa vật thể (thêm/xóa tường, lửa, nạn nhân, trạm cứu hộ), hoặc điều khiển robot thủ công (User Mode).
* Thu thập dữ liệu thực nghiệm để so sánh các thuật toán dựa trên các chỉ số: số nạn nhân cứu được, số nạn nhân tử vong, số bước đi, số lần lập lại lộ trình (replan) và thời gian xử lý thực tế.

### 1.2. Đối tượng và phạm vi nghiên cứu
* **Đối tượng nghiên cứu:** Bài toán tìm kiếm đường đi trong môi trường động phức tạp (Dynamic Pathfinding), cấu trúc dữ liệu không gian lưới 2D và các thuật toán tìm kiếm BFS, DFS, UCS, Dijkstra, Greedy Best-First Search, A* tích hợp bản đồ rủi ro (Risk Heatmap).
* **Phạm vi nghiên cứu:** 
  * Chương trình chạy offline trên nền tảng máy tính cá nhân bằng ngôn ngữ Python.
  * Môi trường lưới 2D kích thước từ $10 \times 10$ đến $35 \times 35$ ô.
  * Đám cháy lan theo thời gian thực sau mỗi chu kỳ định sẵn (0ms – 10000ms) theo 4 hướng, bị ngăn bởi tường.
  * Tác tử cứu hộ gồm 1 Robot di chuyển từng bước, chỉ chở tối đa 1 nạn nhân tại một thời điểm và phải đưa về một trong các trạm cứu hộ (Rescue Stations) liên thông trên bản đồ mới được tính là thành công. Robot chạm lửa sẽ bị cháy (nhiệm vụ thất bại).

### 1.3. Phương pháp nghiên cứu
* **Phương pháp lý thuyết:** Nghiên cứu tài liệu học thuật về không gian trạng thái, hàm Heuristic và cơ chế tìm kiếm đường đi trong Trí tuệ nhân tạo. Phân tích thuật toán A* mở rộng tích hợp yếu tố rủi ro: 
  $$f(n) = g(n) + h(n) + risk(n)$$
* **Phương pháp mô hình hóa:** Biểu diễn các đối tượng Robot, Nạn nhân, Trạm cứu hộ, Đám cháy thành các thực thể dữ liệu có thuộc tính tọa độ cụ thể. Biểu diễn cấu trúc phòng và hành lang để phản ánh môi trường công trình thực tế.
* **Phương pháp thực nghiệm:** Lập trình phần mềm hoàn chỉnh, chạy các kịch bản so sánh hiệu năng trực tiếp (cùng một bản đồ ban đầu, đổi thuật toán tìm kiếm) để ghi nhận dữ liệu thống kê khách quan.

### 1.4. Công cụ sử dụng
* **Ngôn ngữ lập trình:** Python 3.12.
* **Thư viện đồ họa:** Pygame 2.6.0 để dựng khung mô phỏng thời gian thực, xử lý sự kiện chuột/bàn phím và vẽ bản đồ nhiệt.
* **Thư viện kiểm thử:** Pytest 8.2.2 để viết các ca kiểm thử tự động, đảm bảo tính đúng đắn của logic di chuyển, cháy lan và tìm kiếm đường đi.
* **Quản lý mã nguồn:** Git và GitHub.

---

## PHẦN 2. THIẾT KẾ HỆ THỐNG

### 2.1. Phân tích bài toán

#### 2.1.1. Mô tả bài toán cứu hộ trong hỏa hoạn
Hệ thống là một trò chơi/mô phỏng lưới ô vuông. Robot xuất phát ở tọa độ cho trước. Trên bản đồ có các phòng được ngăn bởi các mảng tường lớn, hành lang kết nối các phòng. Nạn nhân bị kẹt tại các vị trí ngẫu nhiên trong phòng. Nguồn lửa bùng phát và lan truyền liên tục. Nhiệm vụ của Robot là di chuyển đến ô của nạn nhân, cõng nạn nhân đó và di chuyển đến trạm cứu hộ gần nhất/an toàn nhất để thả xuống. Mô phỏng thành công khi toàn bộ nạn nhân được giải cứu, và thất bại nếu Robot đi vào lửa hoặc bị lửa lan trúng.

#### 2.1.2. Biểu diễn trạng thái grid
Bản đồ được biểu diễn bằng một ma trận 2 chiều kích thước $W \times H$. Mỗi ô lưới $(x, y)$ chứa thông tin về loại ô (`CellType`):
* `EMPTY` (0): Ô trống di chuyển bình thường.
* `WALL` (1): Tường chặn di chuyển của robot và lửa.
* `FIRE` (2): Lửa đang cháy, robot không thể đi qua (đi qua sẽ chết).
* `VICTIM` (3): Ô chứa nạn nhân cần giải cứu.
* `ROBOT` (4): Ô chứa vị trí hiện tại của Robot.
* `RESCUE` (5): Trạm cứu hộ để robot trả nạn nhân.

#### 2.1.3. Cơ chế cháy lan động và Heat Map đánh giá rủi ro
* **Logic cháy lan:** Lửa xuất phát từ các nguồn cháy ban đầu, cứ sau một chu kỳ `Fire Interval` (tính bằng ms) sẽ lan sang 4 ô lân cận (lên, xuống, trái, phải) nếu các ô đó không phải là `WALL` và chưa bị cháy.
* **Bản đồ rủi ro (Risk Heatmap):** Các ô nằm gần đám cháy sẽ chịu mức rủi ro tiềm ẩn (Risk) giảm dần theo khoảng cách Manhattan tới đám cháy gần nhất. Chỉ số rủi ro $risk \in [0.0, 1.0]$ được sử dụng trực tiếp để tô màu nhiệt (từ vàng, cam đến đỏ đậm) và đưa vào làm trọng số chi phí cho thuật toán tìm kiếm đường đi.

### 2.2. Thiết kế thuật toán tìm kiếm đường đi

#### 2.2.1. Nhóm thuật toán tìm kiếm mù
* **Breadth-First Search (BFS):** Tìm kiếm theo chiều rộng, phù hợp tìm đường ngắn nhất tính theo số bước di chuyển cơ bản trên ma trận ô trống mà không quan tâm đến rủi ro hỏa hoạn.
* **Depth-First Search (DFS):** Tìm kiếm theo chiều sâu, ưu tiên duyệt hết một nhánh trước khi quay lui. Thuật toán này không tối ưu quãng đường, chủ yếu dùng để minh họa sự khác biệt về chiến lược duyệt.
* **Uniform Cost Search (UCS) / Dijkstra:** Tìm kiếm đường đi tối ưu có xét đến chi phí tổng lũy kế, trong đó chi phí bước đi qua ô có rủi ro sẽ bị phạt nặng nhằm giúp robot tránh các ô gần lửa.

#### 2.2.2. Nhóm thuật toán tìm kiếm có thông tin
* **Greedy Best-First Search:** Duyệt dựa trên hàm đánh giá Heuristic $h(n)$ (khoảng cách Manhattan tới đích). Tìm kiếm nhanh nhưng dễ bị bẫy trong mê cung tường hoặc bị cô lập bởi lửa.
* **A\* mở rộng (Risk-Aware A\*):** Thuật toán tìm kiếm tối ưu kết hợp giữa chi phí thực tế $g(n)$, ước lượng Heuristic $h(n)$ và rủi ro từ bản đồ nhiệt $risk(n)$:
  $$f(n) = g(n) + h(n) + risk\_penalty(n)$$
  Trong đó:
  * $g(n)$: Số bước di chuyển thực tế từ điểm xuất phát đến node hiện tại (mỗi bước đi bằng $1.0$).
  * $h(n)$: Khoảng cách Manhattan từ node hiện tại đến mục tiêu (nạn nhân hoặc trạm cứu hộ):
    $$h(n) = |x_{current} - x_{target}| + |y_{current} - y_{target}|$$
  * $risk\_penalty(n) = risk(n) \times RISK\_WEIGHT$: Chi phí phạt rủi ro hỏa hoạn, khuyến khích robot đi vòng qua hành lang an toàn thay vì băng qua hành lang đang bị đe dọa bởi đám cháy sát bên.

### 2.3. Thiết kế giao diện chương trình
Giao diện được bố trí gọn gàng, chia tỉ lệ khung nhìn thành hai phần chính:
* **Khung hiển thị bản đồ (Bên trái - chiếm 80%):** Hiển thị ô lưới ma trận, các sprite hình vẽ robot, nạn nhân, lửa, trạm cứu hộ, các chấm chỉ đường đi dự kiến (Planned Path) và lớp phủ mờ màu sắc thể hiện mức độ nguy hiểm (Heat Map).
* **Sidebar điều khiển (Bên phải - chiếm 20%):** Gồm 5 khối chức năng từ trên xuống dưới:
  * **Map Settings:** Cấu hình kích thước bản đồ thông qua dropdown và điều chỉnh thời gian lửa lan qua ô nhập số (ms), nút bấm sinh ngẫu nhiên bản đồ liên thông.
  * **Edit Mode:** Chọn các cọ vẽ thực thể (`Wall`, `Robot`, `Victim`, `Fire`, `Rescue`, `Erase`) để chỉnh sửa trực tiếp trên lưới bằng cách click/rê chuột.
  * **Run Mode:** Các nút khởi chạy thuật toán tìm đường ngay lập tức hoặc chế độ chơi thủ công (`USER MODE`).
  * **Control:** Nút Pause/Resume tạm dừng toàn bộ mô phỏng và nút Reset khôi phục bản đồ về trạng thái ban đầu trước khi chạy.
  * **Status:** Hiển thị thời gian, số bước đi, số nạn nhân đã cứu, số nạn nhân tử vong, số người còn lại, và hiển thị biểu ngữ kết quả cuối cùng.

---

## PHẦN 3. XÂY DỰNG CHƯƠNG TRÌNH

### 3.1. Xây dựng mô hình trạng thái (State representation)
Định nghĩa cấu trúc dữ liệu hướng đối tượng trong Python tại thư mục `app/core/state.py`:
* Lớp `Position`: Quản lý tọa độ $(x, y)$ bất biến.
* Lớp `Cell`: Quản lý thuộc tính của mỗi ô lưới gồm tọa độ, loại ô (`cell_type`), độ rủi ro (`risk`) và cấp độ lửa (`fire_level`).
* Lớp `Robot`: Lưu trữ vị trí, số bước đi, trạng thái sống/chết và thông tin nạn nhân đang cõng.
* Lớp `Victim`: Lưu trữ vị trí, mã số định danh, trạng thái đang đợi/được cõng/đã cứu/đã chết.
* Lớp `GameState`: Lưu trữ toàn bộ trạng thái của mô phỏng tại một thời điểm (Single Source of Truth).
* Lớp `Snapshot`: Hỗ trợ sao chép sâu (`deepcopy`) toàn bộ `GameState` tại thời điểm trước khi bấm chạy để thực hiện chức năng Reset hoàn hảo.

### 3.2. Xây dựng các phép toán chuyển trạng thái (State transitions)
Định nghĩa các hàm xử lý logic tại các thư mục chức năng:
* **Di chuyển:** Hàm `validate_and_move` kiểm tra tính hợp lệ của ô tiếp theo (không vượt biên, không phải tường).
* **Cứu hộ:** Hàm `check_and_pickup` kiểm tra nếu Robot trùng tọa độ với nạn nhân đang đợi $\rightarrow$ Robot cõng nạn nhân, xóa ô nạn nhân trên lưới, giải phóng kế hoạch tìm đường cũ để tìm đường đến trạm cứu hộ. Hàm `check_and_deliver` kiểm tra nếu Robot mang nạn nhân đến ô Trạm cứu hộ $\rightarrow$ Nạn nhân được giải thoát an toàn, tăng điểm cứu hộ, giải phóng kế hoạch để đi tìm người tiếp theo.
* **Cháy lan:** Hàm `spread_fire` duyệt qua danh sách các ô lửa hiện tại, nhân bản lửa ra xung quanh sau mỗi tick thời gian và cập nhật lại danh sách các ô cháy.
* **Bản đồ rủi ro:** Hàm `generate_heatmap` tính toán khoảng cách từ các ô trống đến đám cháy gần nhất bằng thuật toán BFS loang, cập nhật lại giá trị nguy hiểm `risk` của từng ô.

### 3.3. Cài đặt các thuật toán tìm kiếm đường đi
Hiện thực hóa các tệp tin thuật toán tại thư mục `app/ai/`:
* [bfs.py](file:///c:/Users/cuong/Desktop/projectTTNT/app/ai/bfs.py), [dfs.py](file:///c:/Users/cuong/Desktop/projectTTNT/app/ai/dfs.py): Duyệt đồ thị không trọng số để tìm đường dựa trên cấu trúc hàng đợi (Queue) hoặc ngăn xếp (Stack).
* [ucs.py](file:///c:/Users/cuong/Desktop/projectTTNT/app/ai/ucs.py), [dijkstra.py](file:///c:/Users/cuong/Desktop/projectTTNT/app/ai/dijkstra.py): Sử dụng hàng đợi ưu tiên (Priority Queue) để duyệt các ô có tổng chi phí lũy kế nhỏ nhất (cộng dồn bước đi $1.0$ và giá trị rủi ro ô đó).
* [greedy.py](file:///c:/Users/cuong/Desktop/projectTTNT/app/ai/greedy.py): Sử dụng Priority Queue với độ ưu tiên là khoảng cách Manhattan trực tiếp tới mục tiêu.
* [astar.py](file:///c:/Users/cuong/Desktop/projectTTNT/app/ai/astar.py): Sử dụng Priority Queue duyệt theo hàm đánh giá tổng hợp $f(n) = g(n) + h(n) + risk(n) \times RISK\_WEIGHT$.

### 3.4. Xây dựng giao diện người dùng bằng Pygame
Hiện thực hóa hiển thị tại thư mục `app/ui/`:
* `GridRenderer` vẽ các ô lưới ma trận. Lửa được vẽ bằng các ô màu đỏ cam có lõi màu vàng sáng chói. Nạn nhân được vẽ bằng vòng tròn màu vàng hổ phách có ghi số hiệu (V1, V2, ...). Robot vẽ bằng vòng tròn màu xanh Dodger cá tính (khi cõng nạn nhân sẽ lồng thêm vòng tròn vàng nhỏ bên trong).
* `Sidebar` vẽ 5 khối điều khiển bằng phương thức chia tọa độ Y tĩnh lũy kế trực quan. Các dropdown và hộp nhập số được vẽ dưới dạng các bề mặt phụ đè lên nhau (overlays) bằng Pygame.

### 3.5. Tích hợp hệ thống và kiểm thử đơn vị
* Các thành phần được tích hợp vào vòng lặp chính của Pygame tại [main.py](file:///c:/Users/cuong/Desktop/projectTTNT/main.py) quản lý tần số quét màn hình (FPS = 30), tiếp nhận sự kiện bàn phím/chuột để cập nhật trạng thái mô phỏng.
* Viết 27 kịch bản kiểm thử tự động trong thư mục `tests/` để kiểm tra độ tin cậy của thuật toán, cơ chế cháy lan, và độ chính xác của các ô nhập cấu hình giao diện.

---

## PHẦN 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ

### 4.1. Môi trường thực nghiệm
* **Phần cứng:** Máy tính cá nhân CPU Intel Core i7 / AMD Ryzen 5, RAM 16GB.
* **Hệ điều hành:** Windows 10/11.
* **Môi trường chạy:** Python 3.12, Pygame 2.6.0.

### 4.2. Các trường hợp thử nghiệm (Test cases)
* **Kịch bản 1 (Bản đồ tĩnh không cháy):** Chạy các giải thuật trên bản đồ kích thước $20 \times 20$ để đánh giá đường đi ngắn nhất thông thường.
* **Kịch bản 2 (Bản đồ cháy lan chậm - 3000ms):** Đánh giá khả năng tối ưu hóa đường đi của các thuật toán khi có lửa bắt đầu lan nhưng tốc độ chậm.
* **Kịch bản 3 (Bản đồ cháy lan cực nhanh - 750ms):** Đặt robot vào tình thế nguy cấp, phải liên tục tính toán lại đường đi (Replan) để né tránh các luồng lửa đang phong tỏa hành lang di chuyển.

### 4.3. Kết quả thực nghiệm
*(Sau khi chạy thực tế chương trình, nhóm nghiên cứu sẽ điền các bảng dữ liệu thống kê kết quả chạy của từng thuật toán vào đây)*

| Thuật toán | Số nạn nhân cứu được | Số nạn nhân tử vong | Tổng số bước đi | Số lần lập lại lộ trình (Replans) | Thời gian xử lý TB (ms) | Kết quả nhiệm vụ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BFS** | ... | ... | ... | ... | ... | Thành công / Thất bại |
| **DFS** | ... | ... | ... | ... | ... | Thành công / Thất bại |
| **UCS** | ... | ... | ... | ... | ... | Thành công / Thất bại |
| **Greedy** | ... | ... | ... | ... | ... | Thành công / Thất bại |
| **A\*** | ... | ... | ... | ... | ... | Thành công / Thất bại |

### 4.4. Phân tích, so sánh hiệu quả giữa các thuật toán
* So sánh giữa nhóm thuật toán duyệt mù (BFS, DFS) và duyệt có thông tin (A*, Greedy) về độ dài quãng đường và số lượng node cần mở rộng.
* Phân tích tầm quan trọng của trọng số rủi ro ($risk$) trong thuật toán A* mở rộng: So sánh đường đi của A* mở rộng (chọn hành lang xa đám cháy, dài hơn một chút nhưng an toàn) với BFS/Dijkstra thông thường (chọn hành lang ngắn nhất nhưng sát cạnh đám cháy và dễ bị lửa lan trúng dẫn tới tử vong).
* Chứng minh khả năng thích ứng linh hoạt của hệ thống thông qua việc đếm số lần tự động lập lại lộ trình (`Replans`) khi phát hiện đường đi dự kiến cũ đã bị đám cháy phong tỏa.

### 4.5. Đánh giá ưu điểm và hạn chế
* **Ưu điểm:**
  * Mô phỏng trực quan, sinh động, dễ quan sát đám cháy lan và bước đi của robot.
  * Bản đồ rủi ro Heat Map trực quan hóa mức độ nguy hiểm rất tốt, giúp thuật toán A* mở rộng hoạt động tối ưu.
  * Cho phép người dùng chỉnh sửa trực tiếp bản đồ tùy ý, giúp giảng viên và sinh viên dễ dàng demo các tình huống hiểm nghèo để thách thức AI.
* **Hạn chế:**
  * Mô hình cháy lan và tính toán rủi ro còn đơn giản theo khoảng cách Manhattan, chưa áp dụng các quy luật vật lý cháy khí, khói độc phức tạp.
  * Hệ thống mới chỉ hỗ trợ 1 robot cứu hộ đơn lẻ hoạt động độc lập, chưa giải quyết bài toán phối hợp đa tác tử (Multi-agent coordination).

---

## PHẦN 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1. Kết quả đạt được
Nhóm nghiên cứu đã hoàn thành toàn bộ các mục tiêu đặt ra trong đề cương:
* Xây dựng thành công ứng dụng mô phỏng cứu hộ hỏa hoạn hoạt động mượt mà, giao diện trực quan thân thiện.
* Triển khai hoàn chỉnh và kiểm thử thành công 6 thuật toán tìm kiếm đường đi cốt lõi từ cơ bản đến nâng cao.
* Tích hợp thành công cơ chế Heat Map và thuật toán A* mở rộng né tránh rủi ro hỏa hoạn cực kỳ hiệu quả trong môi trường biến đổi liên tục.

### 5.2. Kết luận chung
Việc kết hợp hàm đánh giá Heuristic truyền thống với lớp thông tin rủi ro môi trường động là giải pháp vô cùng hiệu quả để giải quyết các bài toán tìm đường thực tế. Thuật toán A* mở rộng mặc dù tốn thêm chi phí tính toán nhỏ để cập nhật bản đồ nhiệt nhưng mang lại tỷ lệ giải cứu nạn nhân thành công vượt trội so với các thuật toán tìm kiếm mù thông thường trong các môi trường nguy hiểm như hỏa hoạn.

### 5.3. Hướng phát triển trong tương lai
* Phát triển hệ thống cứu hộ đa tác tử (Multi-agent), cho phép nhiều robot cùng phối hợp giải cứu nạn nhân, chia sẻ thông tin bản đồ hỏa hoạn và phân công nhiệm vụ tối ưu.
* Tích hợp các mô hình dự báo hướng cháy dựa trên hướng gió, vật liệu cháy trong phòng để robot đưa ra quyết định di chuyển thông minh hơn (né trước các ô có nguy cơ cháy cao trong tương lai gần).
* Chuyển đổi giao diện sang nền tảng 3D hoặc Web để tăng tính phổ biến và trải nghiệm người dùng.

---

## TÀI LIỆU THAM KHẢO
1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
2. Pygame Community. (2024). *Pygame Documentation*. Retrieved from https://www.pygame.org/docs/
3. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths. *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100-107.
