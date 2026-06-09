# HƯỚNG DẪN CHƠI GAME & CƠ CHẾ HOẠT ĐỘNG
## HỆ THỐNG MÔ PHỎNG GIẢI CỨU HOẢ HOẠN 2D (AI RESCUE & FIRE SIMULATION)

Chào mừng bạn đến với hệ thống mô phỏng cứu hộ hoả hoạn tương tác 2D. Dự án sử dụng thư viện **Pygame** làm giao diện đồ họa chính, kết hợp với các thuật toán tìm kiếm đường đi (Pathfinding) thông minh, giúp robot tự động điều hướng và cứu hộ nạn nhân trong điều kiện đám cháy lan rộng theo thời gian thực.

---

## 1. Mục Tiêu Trò Chơi (Game Goal)
Nhiệm vụ của **Robot Giải Cứu (R)** là di chuyển qua các hành lang và phòng trong tòa nhà để:
1. Tiếp cận các **Nạn nhân (V)** đang bị mắc kẹt.
2. Nhặt nạn nhân lên (mỗi lần Robot chỉ chở được tối đa **1 nạn nhân**).
3. Vận chuyển nạn nhân đến một trong các **Trạm cứu hộ an toàn (Rescue Station)** ở rìa bản đồ.
4. Hoàn thành giải cứu toàn bộ nạn nhân còn sống sót trước khi họ hoặc chính Robot bị lửa thiêu rụi.

* **Nhiệm vụ Thành công**: Tất cả nạn nhân được đưa tới Trạm cứu hộ an toàn và Robot còn sống.
* **Nhiệm vụ Thất bại**: Robot bị cháy (đi vào ô lửa) hoặc tất cả nạn nhân bị chết cháy/không thể tiếp cận được.

---

## 2. Giao Diện & Màu Sắc Quy Ước (UI & Visual Theme)
Màn hình ứng dụng được chia thành hai phần chính:
* **Khu vực bản đồ lưới (80% bên trái)**: Hiển thị môi trường tòa nhà kích thước cố định **30x25**.
* **Thanh điều khiển Sidebar (20% bên phải)**: Hiển thị bảng điều khiển và thông số thời gian thực.

### Quy ước màu sắc trên bản đồ:
* **Màu xám nhạt (Empty)**: Hành lang hoặc sàn phòng trống, Robot có thể di chuyển qua.
* **Màu xám đậm (Wall)**: Tường gạch, vật cản không thể đi xuyên qua.
* **Xanh dương (Robot)**: Robot cứu hộ. Khi chở nạn nhân, sẽ có vòng tròn nhỏ màu vàng kèm ký hiệu nạn nhân (ví dụ: `V1`) nằm ở trung tâm của Robot.
* **Màu vàng (Victim)**: Nạn nhân đang chờ cứu hộ. Ký hiệu là `V` kèm ID của họ. Nếu nạn nhân bị lửa thiêu chết, biểu tượng chuyển sang màu đen xám kèm chữ X đỏ.
* **Xanh lá cây (Rescue Station)**: Trạm cứu hộ an toàn để đưa nạn nhân tới bàn giao.
* **Màu đỏ cam (Fire)**: Tâm của đám cháy đang hoạt động. Có lõi màu vàng sáng.
* **Bản đồ nhiệt rủi ro (Risk Heatmap)**: Các ô xung quanh đám cháy sẽ đổi màu từ **Vàng nhạt -> Cam -> Đỏ** tùy theo mức độ rủi ro tăng dần (cận kề nguồn lửa).
* **Đường đi dự kiến (Cyan Path)**: Các dấu chấm màu xanh ngọc nối từ Robot đến mục tiêu hiện tại của nó.

---

## 3. Các Chế Độ Chạy & Thuật Toán AI (Play Modes)
Hệ thống hỗ trợ 7 chế độ chạy khác nhau, bấm trực tiếp ở Sidebar để kích hoạt:

1. **MANUAL CONTROL (Điều khiển thủ công)**: 
   * Người chơi sử dụng **4 phím mũi tên** (`LÊN`, `XUỐNG`, `TRÁI`, `PHẢI`) để trực tiếp di chuyển robot trên lưới.
   * Chế độ này thích hợp cho việc tự mình trải nghiệm thử thách hoặc kiểm tra bản đồ tự chế.
2. **BFS (Breadth-First Search)**:
   * Tìm kiếm theo chiều rộng. Robot sẽ tìm đường ngắn nhất về mặt số bước đi.
   * **Nhược điểm**: BFS hoàn toàn bỏ qua yếu tố lửa và rủi ro nguy hiểm, Robot có thể lao thẳng qua vùng rủi ro cao nếu đó là đường ngắn nhất.
3. **DFS (Depth-First Search)**:
   * Tìm kiếm theo chiều sâu (sử dụng ngăn xếp Stack giới hạn độ sâu tối đa để tránh tràn bộ nhớ).
   * **Nhược điểm**: Đường đi dài, uốn lượn không tối ưu và cũng không né tránh vùng nguy hiểm.
4. **UCS (Uniform Cost Search) & DIJKSTRA**:
   * Tìm đường tối ưu có tính đến chi phí rủi ro hoả hoạn.
   * Chi phí di chuyển qua một ô = $1.0 + Risk \times 10.0$. Ô càng gần lửa thì chi phí đi qua càng cực kỳ đắt, giúp thuật toán bẻ hướng đường đi vòng xa hơn để bảo đảm an toàn cho Robot và nạn nhân.
5. **GREEDY SEARCH (Tìm kiếm tham lam)**:
   * Sử dụng hàm heuristic khoảng cách Manhattan để đi thẳng tới mục tiêu nhanh nhất. Không quan tâm chi phí rủi ro.
6. **A\* SEARCH (Thuật toán đề xuất chính)**:
   * Thuật toán tìm kiếm tối ưu kết hợp giữa chi phí thực tế và ước lượng khoảng cách: $f(n) = g(n) + h(n) + Risk\_Penalty(n)$.
   * Đạt hiệu quả cao nhất: tìm đường ngắn nhất nhưng tự động bẻ lái né tránh các hành lang bị bao phủ bởi khói và lửa.

---

## 4. Các Cơ Chế Hoạt Động Cốt Lõi (Core Mechanics)

### A. Cơ chế lan lửa (Fire Propagation)
* Đám cháy tự động lan rộng theo chu kỳ thời gian (có thể chọn tốc độ từ `Very Slow` đến `Very Fast` trên Sidebar).
* Lửa lan sang 4 ô chung cạnh lân cận nếu ô đó không phải là tường (`WALL`).
* Nếu lửa lan trúng ô chứa Robot hoặc Nạn nhân, thực thể đó sẽ bốc cháy và chuyển sang trạng thái tử vong (`DEAD`).

### B. Bản đồ nhiệt rủi ro khói bụi (Risk Heatmap)
* Xung quanh mỗi nguồn lửa, hệ thống dùng thuật toán BFS giới hạn độ sâu tối đa là **4 ô** để lan truyền mức độ rủi ro nhiệt/khói bụi.
* Càng gần đám cháy, hệ số rủi ro ($Risk$) càng tiến gần $1.0$.
* Các thuật toán an toàn (UCS, Dijkstra, A\*) sẽ đọc giá trị rủi ro này của các ô lưới để tìm cung đường an toàn nhất.

### C. Cơ chế tự động lập lại lộ trình (Dynamic Replanning)
* Trong lúc Robot đang chạy theo lộ trình tìm được, nếu lửa lan rộng ra và **chặn đứng** đường đi dự kiến (ô nằm trên đường đi chuyển thành ô lửa hoặc tường), hệ thống sẽ **hủy bỏ** đường cũ ngay lập tức.
* Robot tự động kích hoạt thuật toán để tính toán đường đi mới vòng qua ngả khác. Số lần tính lại này được đếm ở mục **Replans** trên Sidebar.

### D. Ưu tiên mục tiêu (Target Selection)
* **Khi chưa chở nạn nhân**: Robot tìm đường tới nạn nhân còn sống có đường đi ngắn nhất và ít nguy hiểm nhất.
* **Khi đã nhặt nạn nhân**: Robot đổi mục tiêu ngay lập tức sang trạm cứu hộ (`Rescue Station`) gần nhất để thả nạn nhân xuống.

---

## 5. Hướng Dẫn Biên Tập Bản Đồ (Map Editor)
Bạn hoàn toàn có thể tự vẽ một bản đồ thử nghiệm theo ý mình:
1. Khi game ở trạng thái **READY** (bấm nút **RESET** để đưa về READY nếu đang chạy).
2. Chọn một trong các công cụ ở mục **EDITOR MODE TOOLS** trên Sidebar:
   * **Wall**: Nhấp chuột trái hoặc nhấn giữ kéo rê trên bản đồ để xây tường.
   * **Robot**: Nhấp chuột trái để dời điểm xuất phát của Robot.
   * **Victim**: Đặt thêm nạn nhân.
   * **Fire**: Đặt thêm nguồn cháy ban đầu.
   * **Rescue**: Đặt thêm trạm cứu hộ.
   * **Erase**: Nhấp chuột trái hoặc kéo rê để xóa vật cản/thực thể về ô trống. Bạn cũng có thể nhấn **chuột phải** trực tiếp trên bản đồ lưới để xóa nhanh.
3. Bấm các thuật toán ở Sidebar để xem Robot tự tìm đường giải cứu trên bản đồ bạn vừa tự thiết kế!

---

## 6. Các Nút Điều Khiển Khác trên Sidebar
* **GENERATE RANDOM MAP**: Tạo ngẫu nhiên một tòa nhà mới với các cài đặt tùy chỉnh:
  * *Env*: Kiểu kiến trúc tòa nhà (`HOSPITAL` - bệnh viện, `OFFICE` - văn phòng, `APARTMENT` - chung cư, `WAREHOUSE` - nhà kho).
  * *Complexity*: Độ phức tạp/mật độ phòng (`LOW` - thấp, `MEDIUM` - trung bình, `HIGH` - cao).
* **PAUSE / RESUME**: Tạm dừng hoặc tiếp tục chạy mô phỏng để bạn dễ dàng phân tích từng bước đi của Robot.
* **RESET**: Đưa toàn bộ mô phỏng trở lại trạng thái ban đầu của bản đồ hiện tại (đưa Robot về điểm xuất phát, dập các đám cháy lan thêm, hồi sinh các nạn nhân về trạng thái ban đầu để có thể chạy thử lại bằng một thuật toán AI khác để so sánh).

*Chúc bạn có những trải nghiệm mô phỏng thú vị và trực quan với hệ thống!*
