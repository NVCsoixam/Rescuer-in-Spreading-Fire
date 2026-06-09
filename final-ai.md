1. TỔNG QUAN DỰ ÁN

Dự án là một hệ thống mô phỏng cứu hộ 2D có cháy lan, lấy bối cảnh một bản đồ dạng lưới ô vuông. Người cứu hộ sẽ di chuyển trong môi trường này để tìm nạn nhân, cõng từng nạn nhân một, đưa về các trạm cứu hộ, trong khi đám cháy lan dần theo thời gian và làm thay đổi tính khả thi của đường đi.

Ý tưởng gốc của đề tài đã xác định rõ đây là bài toán tìm kiếm trong môi trường động, không phải mê cung tĩnh thông thường, vì lửa lan liên tục và robot phải cân nhắc rủi ro theo thời gian. Đề cương gốc cũng nêu rõ mục tiêu là mô phỏng cứu nạn, sinh/chỉnh map, mô phỏng cháy lan, áp dụng nhiều thuật toán tìm kiếm như BFS, DFS, UCS, Dijkstra, Greedy Best-First Search và A*, đồng thời đánh giá hiệu quả bằng các chỉ số như số nạn nhân cứu được, số bước di chuyển và thời gian xử lý. 

2. TINH THẦN CỦA DỰ ÁN

Dự án hiện tại không còn là “bài tìm đường” đơn thuần nữa. Nó đã được nâng lên thành một mini rescue simulation có phong cách game mô phỏng nhẹ, trực quan và có tính trình diễn cao.

Người xem khi mở chương trình sẽ không nhìn thấy một bảng điều khiển khô cứng. Họ sẽ thấy:

một map lớn chiếm phần lớn màn hình, 

robot cứu hộ di chuyển trên map, 

nạn nhân nằm trong các phòng hoặc hành lang, 

lửa lan dần qua các tick thời gian, 

vùng nguy hiểm được tô bằng heat map, 

nhiều trạm cứu hộ để robot lựa chọn, 

các thuật toán AI chạy ngay khi bấm, 

và một sidebar nhỏ gọn bên phải để điều khiển. 

Mục tiêu là: nhìn vào là hiểu ngay hệ thống đang làm gì.

3. MỤC TIÊU THIẾT KẾ

Dự án này có các mục tiêu rõ ràng:

3.1. Mục tiêu học thuật

minh họa các thuật toán tìm kiếm cơ bản và có thông tin; 

thể hiện được sự khác nhau giữa BFS, DFS, UCS, Dijkstra, Greedy và A*; 

làm rõ vai trò của heuristic trong môi trường động; 

cho thấy ảnh hưởng của nguy cơ cháy tới lựa chọn đường đi. 

3.2. Mục tiêu mô phỏng

tạo bản đồ dạng công trình thật hơn là map random vô nghĩa; 

có cháy lan theo thời gian; 

có vùng nguy hiểm; 

có nhiều trạm cứu hộ; 

có chế độ cứu người theo nhiệm vụ cụ thể. 

3.3. Mục tiêu trình diễn

giao diện đẹp, trực quan, dễ demo; 

map lớn, control gọn; 

robot, victim, fire, rescue station đều có icon/sprite rõ ràng; 

có thể chỉnh sửa map để tạo tình huống thực nghiệm. 

4. BỐI CẢNH VÀ PHẠM VI

Môi trường là một grid 2D. Mỗi ô trên bản đồ có thể là:

ô trống, 

tường, 

nạn nhân, 

lửa, 

robot, 

trạm cứu hộ. 

Đề cương gốc cũng giới hạn hệ thống trong một môi trường mô phỏng 2 chiều dạng lưới, cho phép bản đồ thủ công hoặc sinh tự động, và cho phép thay đổi kích thước, số lượng nạn nhân, số nguồn cháy, vị trí robot và điểm an toàn. 

Phạm vi hiện tại đã được chốt lại như sau:

map 2D dạng ô vuông; 

kích thước map từ 10x10 đến 35x35; 

mặc định 20x20; 

có 1 robot; 

mặc định 5 nạn nhân; 

mặc định 3 trạm cứu hộ; 

mặc định 1 nguồn lửa; 

lửa lan theo thời gian thực; 

robot chỉ chở được 1 nạn nhân mỗi lượt; 

nạn nhân phải được đưa về rescue station mới tính là cứu; 

nếu robot bị cháy thì mô phỏng thất bại; 

nếu không còn nạn nhân nào trên map thì mô phỏng kết thúc thành công. 

5. LUẬT CHƠI CHÍNH

Đây là phần cốt lõi của logic dự án.

5.1. Robot

chỉ có một robot; 

robot di chuyển từng ô trên grid; 

robot có thể điều khiển bằng bàn phím trong User Mode; 

robot có thể chạy tự động bằng thuật toán; 

robot chỉ cõng được một nạn nhân tại một thời điểm. 

5.2. Nạn nhân

nạn nhân được đặt trên map; 

có thể dùng sprite chibi người hoặc các sprite vui như mèo, chó, gà, khủng long; 

khi robot đứng đúng ô nạn nhân, robot nhặt nạn nhân lên; 

sau đó robot phải đưa nạn nhân tới trạm cứu hộ; 

chỉ khi tới trạm cứu hộ thì nạn nhân mới được tính là rescued. 

5.3. Trạm cứu hộ

có nhiều trạm cứu hộ; 

robot không bị buộc phải về đúng một điểm; 

robot sẽ chọn trạm phù hợp để thả nạn nhân; 

điều này làm bài toán thú vị hơn vì có thêm lựa chọn chiến lược. 

5.4. Lửa

lửa lan theo thời gian; 

tường có thể chặn lửa; 

vùng gần lửa trở nên nguy hiểm hơn; 

robot phải tránh vùng cháy và vùng sắp cháy; 

nếu robot bị lửa chạm vào thì thất bại. 

6. CƠ CHẾ RANDOM MAP

Đây là một trong những phần quan trọng nhất.

6.1. Mặc định khi tạo map

20x20 

5 victims 

3 rescue stations 

1 fire source 

1 robot 

walls sinh ngẫu nhiên có cấu trúc 

6.2. Kích thước map

nhỏ nhất: 10x10 

lớn nhất: 35x35 

không cho nhập tự do ngoài khoảng đó 

6.3. Fire interval

mặc định: 1000 ms 

min: 0 

max: 10000 

giá trị này điều khiển tốc độ lửa lan 

6.4. Logic sinh tường

Không sinh tường kiểu random từng ô một cách vô tổ chức, vì kiểu đó làm map xấu và dễ bị nghẽn. Thay vào đó, map sẽ sinh theo kiểu:

phòng; 

hành lang; 

cụm tường; 

khu vực nối với nhau bằng cửa hoặc khoảng hở; 

layout giống công trình thật. 

Ý tưởng này rất hợp với hình bạn gửi vì map kiểu phòng-hành lang:

nhìn giống tòa nhà thật, 

dễ hiểu hơn, 

cháy lan có câu chuyện hơn, 

đường đi của thuật toán cũng dễ quan sát hơn. 

6.5. Yêu cầu liên thông

Random map phải đảm bảo:

robot không bị nhốt hoàn toàn; 

nạn nhân không bị cô lập vô lý; 

rescue station phải reachable; 

ít nhất phải có đường hợp lệ trong map để mô phỏng chạy được. 

Nếu random ra map lỗi thì hệ thống phải:

sửa lại, 

hoặc generate lại, 

hoặc đục hành lang nối thông. 

7. EDIT MODE

Edit Mode là khối cho phép can thiệp trực tiếp lên bản đồ.

7.1. Các nút chỉnh sửa

Robot 

Victim 

Fire 

Wall 

Rescue 

Erase 

7.2. Cơ chế hoạt động

chọn một nút; 

nút đó sáng lên; 

click lên map để thao tác; 

click lại đúng object đó thì xóa; 

robot là trường hợp đặc biệt: chỉ có 1, nên click mới là chuyển robot sang ô đó. 

7.3. Nguyên tắc

một ô không nên chứa nhiều object cùng lúc; 

khi thuật toán đang chạy thì khóa Edit Mode; 

khi Pause cũng nên khóa sửa map để tránh xung đột logic; 

Erase chỉ xóa object tại vị trí đang click. 

7.4. Kiểu nút

Bố cục edit mode không cần Select kiểu chuyên nghiệp. Nó chỉ cần dạng icon/nút đơn giản, ví dụ:

👨‍🚒 Robot 

🐱 Victim 

🔥 Fire 

🧱 Wall 

🏥 Rescue 

❌ Erase 

Lý do: nhanh, gọn, trực quan, dễ code, dễ demo.

8. RUN MODE

Khối này là nơi chọn chế độ chạy.

8.1. Chế độ có trong Run Mode

USER MODE 

BFS 

DFS 

UCS 

Dijkstra 

Greedy 

A* 

8.2. Quy tắc vận hành

bấm vào thuật toán là chạy ngay; 

không có nút Start riêng; 

không có AI Mode riêng; 

không có Human vs AI; 

chỉ một chế độ được hoạt động tại một thời điểm. 

8.3. USER MODE

Khi bật User Mode:

robot được điều khiển bằng phím mũi tên; 

↑ ↓ ← → sẽ di chuyển robot; 

robot không xuyên tường; 

robot không đi ra ngoài map; 

robot có thể đi vào ô victim, rescue station; 

robot có thể đi vào fire, nhưng sẽ chết nếu chạm lửa. 

8.4. Thuật toán

BFS

đi theo tầng; 

tốt để minh họa đường ngắn theo số bước. 

DFS

đi sâu trước; 

không tối ưu nhưng minh họa chiến lược tìm sâu. 

UCS

xét cost; 

phù hợp với map có nguy hiểm. 

Dijkstra

đường đi tối ưu theo chi phí toàn cục. 

Greedy

ưu tiên heuristic; 

nhanh nhưng có thể chọn đường sai. 

A*

quan trọng nhất; 

cân bằng giữa cost, heuristic và risk. 

9. A MỞ RỘNG*

Công thức nền vẫn là:

f(n) = g(n) + h(n)

Nhưng với dự án này, A* được mở rộng thành:

f(n) = g(n) + h(n) + risk(n)

Trong đó:

g(n) = chi phí đi từ điểm xuất phát đến node hiện tại; 

h(n) = khoảng cách ước lượng đến mục tiêu, thường là Manhattan; 

risk(n) = mức nguy hiểm từ heat map. 

Đây là phần quan trọng nhất của toàn bộ thiết kế thuật toán vì nó khiến robot không chỉ chọn đường ngắn mà còn chọn đường an toàn hơn.

10. HEAT MAP / RISK MAP

Heat Map là lớp hiển thị và logic đánh giá nguy hiểm.

10.1. Mục tiêu

biểu diễn vùng an toàn / nguy hiểm; 

cho robot biết vùng nào nên tránh; 

giúp thuật toán tìm đường “thông minh” hơn. 

10.2. Thang nguy hiểm

Có thể hiểu như:

xanh: an toàn; 

vàng: cảnh báo; 

cam: nguy hiểm; 

đỏ: rất nguy hiểm; 

đỏ đậm: cháy / sắp cháy. 

10.3. Vai trò

lửa hiện tại chưa phải là tất cả; 

vùng gần lửa cũng nguy hiểm; 

robot phải né cả nơi “chưa cháy nhưng sắp cháy”; 

giúp A* có cơ sở để tránh đường tối ưu nhưng rủi ro. 

11. LOGIC CHÁY LAN

Mô phỏng cháy là phần rất quan trọng vì nó quyết định độ hấp dẫn của bài toán.

11.1. Tốc độ cháy

cháy chạy theo thời gian; 

mặc định 1000 ms/lần; 

người dùng có thể chỉnh từ 0 đến 10000 ms. 

11.2. Cách lan

lửa lan theo 4 hướng; 

tường chặn lửa; 

lửa không xuyên tường; 

vùng gần lửa sẽ tăng risk trước khi cháy thật. 

11.3. Tại sao không chọn cháy quá nhanh

Nếu quá nhanh:

map cháy sạch; 

thuật toán chết quá sớm; 

người xem không quan sát được. 

Nếu quá chậm:

mất áp lực; 

không thấy khác biệt giữa thuật toán; 

mô phỏng nhạt. 

Nên tốc độ cháy phải cân bằng, và fire interval là thứ người dùng điều chỉnh để tạo độ khó.

12. RESCUE LOGIC

Đây là logic cứu người cốt lõi của mô phỏng.

12.1. Quy trình

robot tìm tới nạn nhân; 

robot cõng nạn nhân; 

robot tìm tới rescue station gần nhất hoặc an toàn nhất; 

robot thả nạn nhân; 

nạn nhân được tính là cứu xong; 

robot quay lại cứu người tiếp theo. 

12.2. Vì sao chỉ chở 1 người

dễ hiểu; 

dễ code; 

cân bằng gameplay; 

tránh biến dự án thành bài toán multi-agent hoặc logistics phức tạp. 

12.3. Nhiều rescue station

Việc có nhiều trạm cứu hộ làm cho:

robot có nhiều lựa chọn; 

đường đi không còn cố định; 

A* có thêm chiều sâu; 

mô phỏng thực tế hơn. 

13. ĐIỀU KIỆN KẾT THÚC

13.1. Mission Complete

Khi:

không còn nạn nhân nào trên bản đồ. 

13.2. Mission Failed

Khi:

robot bị cháy. 

13.3. Không dùng success theo %

Đã loại bỏ các tiêu chí kiểu “cứu được 70% là xong”, vì nó không hợp lý về mặt mô phỏng cứu hộ. Nếu trên map còn người cần cứu, mô phỏng vẫn phải tiếp tục; chỉ khi hết người mới kết thúc.

14. USER FLOW CHI TIẾT

14.1. Luồng 1: Chạy thuật toán

mở app; 

generate map; 

chọn thuật toán; 

thuật toán chạy ngay; 

fire lan; 

robot di chuyển; 

robot cứu victim; 

đưa victim về rescue station; 

lặp lại; 

kết thúc khi hết victim hoặc robot chết. 

14.2. Luồng 2: User Mode

mở app; 

generate map; 

chọn USER MODE; 

robot được điều khiển bằng phím mũi tên; 

người chơi tự quyết định đường đi; 

lửa vẫn lan theo thời gian; 

mô phỏng kết thúc như bình thường. 

14.3. Luồng 3: Reset để so sánh

generate map; 

chạy BFS; 

reset; 

chạy A*; 

so sánh saved / steps / time / dead. 

15. CONTROL

Khối control chỉ còn 2 nút:

PAUSE 

RESET 

15.1. Pause

dừng toàn bộ mô phỏng; 

robot đứng yên; 

timer dừng; 

fire dừng; 

thuật toán dừng; 

đổi thành Resume. 

15.2. Reset

Reset sẽ:

quay về trạng thái ngay trước khi bắt đầu chạy; 

áp dụng cho cả User Mode và thuật toán; 

không tạo map mới; 

không đổi settings; 

giữ nguyên bản đồ gốc đã edit. 

Đây là thiết kế rất tốt vì nó giúp so sánh thuật toán công bằng và rất thuận tiện cho demo.

16. STATUS PANEL

Status Panel là phần hiển thị trạng thái hiện tại và cũng là nơi tổng kết cuối cùng.

16.1. Nội dung status

Mode 

Saved 

Dead 

Remaining 

Steps 

Time 

Carrying 

16.2. Ý nghĩa

Mode: đang ở chế độ nào; 

Saved: số nạn nhân đã cứu thành công; 

Dead: số nạn nhân bị cháy; 

Remaining: số nạn nhân còn lại trên map; 

Steps: số bước robot đã đi; 

Time: thời gian mô phỏng; 

Carrying: robot có đang cõng nạn nhân không. 

16.3. Khi kết thúc

Status Panel tự đổi thành:

MISSION COMPLETEhoặc 

MISSION FAILED 

Không cần result panel riêng, vì status panel đã đủ kiêm luôn kết quả cuối.

17. UI LAYOUT CUỐI CÙNG

Sau khi tối ưu, UI được chốt như sau:

17.1. Bên trái

map area chiếm khoảng 80% màn hình; 

đây là phần chính, cần rộng, thoáng, trực quan. 

17.2. Bên phải

Sidebar gồm 5 khối:

Map Settings 

Edit Mode 

Run Mode 

Control 

Status 

17.3. Không cần

top bar; 

bottom panel; 

result panel riêng; 

AI mode riêng; 

Human vs AI. 

18. MAP SETTINGS CUỐI CÙNG

Khối này rất gọn:

Map Size: dropdown 

Fire Interval: numeric input 

Generate Random Map: button 

Mặc định:

map size = 20x20 

fire interval = 1000 ms 

Quy tắc:

map size chỉ từ 10x10 đến 35x35; 

fire interval chỉ từ 0 đến 10000 ms. 

19. CHIẾN LƯỢC RANDOM MAP KHI TẠO MỚI

Khi bấm Generate Random Map, hệ thống phải:

sinh layout có cấu trúc; 

đặt robot; 

đặt 5 victims; 

đặt 3 rescue stations; 

đặt 1 fire source; 

tạo tường theo cụm; 

đảm bảo đường đi hợp lệ; 

đảm bảo không chồng object; 

nếu map lỗi thì regenerate hoặc sửa kết nối. 

20. NHỮNG THỨ ĐÃ LOẠI BỎ

Để giữ dự án gọn và khả thi, đã loại bỏ hoặc không ưu tiên:

Human vs AI; 

AI Mode riêng; 

nhiều robot; 

success theo %; 

result panel riêng; 

settings quá nhiều thông số; 

view options quá phức tạp; 

random tường kiểu nhiễu; 

mô hình cháy vật lý nặng; 

multi-agent coordination. 

21. CÁI GÌ LÀ “ĐIỂM NHẤN” CỦA DỰ ÁN

Theo mình, 4 điểm mạnh nhất là:

Heat Map / Risk MapLàm AI có chiều sâu và làm UI sống động hơn. 

Nhiều trạm cứu hộLàm bài toán chiến lược hơn, không bị cố định một điểm thoát. 

Một robot chở một nạn nhân rồi thả ở trạmLogic rất dễ hiểu nhưng vẫn có chiều sâu. 

Map kiểu công trình phòng-hành langNhìn giống môi trường thật và giúp cháy lan hợp lý hơn. 

22. TÓM TẮT SIÊU NGẮN CỦA TOÀN BỘ DỰ ÁN

Nếu phải nói ngắn nhất:

Một mô phỏng cứu hộ 2D có cháy lan theo thời gian, nơi một robot chibi di chuyển trên map phòng-hành lang, cứu từng nạn nhân một, đưa về nhiều trạm cứu hộ, trong khi heat map/risk map và các thuật toán BFS, DFS, UCS, Dijkstra, Greedy, A* quyết định đường đi; người dùng có thể chỉnh map, chạy thuật toán ngay khi bấm, hoặc điều khiển thủ công bằng phím mũi tên.

23. TRẠNG THÁI HIỆN TẠI CỦA Ý TƯỞNG

Hiện tại, dự án đã đủ để bước sang giai đoạn thiết kế kỹ thuật và code thực sự.Tức là:

ý tưởng đã chốt khá đầy đủ; 

logic chính đã rõ; 

UI đã rõ; 

thuật toán đã rõ; 

điều kiện kết thúc đã rõ; 

random map đã rõ; 

reset/pause đã rõ.