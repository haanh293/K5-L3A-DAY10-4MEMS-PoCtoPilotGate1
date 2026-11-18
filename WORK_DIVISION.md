# Kế hoạch & Phân công công việc Nhóm 4 người · LAB 10 (From PoC to Pilot - Gate 1)

Tài liệu này tổng hợp cấu trúc repo, các quy tắc sống còn và bảng phân chia công việc chi tiết theo từng giai đoạn (240 phút) cho nhóm 4 thành viên.

---

## 1. Tổng quan nhanh về Repo & Luật sống còn

- **Bối cảnh:** Đội dự án của **LogiX-VN** đánh giá **Gate 1** cho trợ lý AI hoàn tiền giao hàng trễ (từ PoC lên Pilot).
- **7 nơi ĐƯỢC PHÉP SỬA** (mọi file khác như `lab10/agent.py`, `lab10/tools.py`, `data/*` đều bị khoá bằng hash trong `lab10/MANIFEST.json`, chạm vào sẽ bị lỗi `1 integrity ❌`):
  1. `TEAM.md`: Bảng thành viên + mục cá nhân của từng người.
  2. `config/acceptance_criteria.json`: Điền ngưỡng và **ký đúng 1 lần trước khi chạy eval** (phút 60–65). Ký xong tuyệt đối không sửa (kể cả format dấu cách).
  3. `lab10/guards.py`: Viết hàm `pre_guard(ctx)` và `write_gate(ctx, action)`.
  4. `config/operating_gates.json`: Điền con số và tên nhân sự cho 3 khối `business`, `operations`, `legal`.
  5. `lab10/monitors.py`: Viết thêm ít nhất 1 hàm monitor mới vào dict `MONITORS` ở Vòng 2.
  6. Ba phiếu báo cáo trong `templates/`: `form-a-criteria.md`, `form-b-evaluation-gates.md`, `form-c-incident.md`.
  7. `submission/submission.json`: Tổng hợp kết quả cuối buổi.

---

## 2. Phân công vai trò cho nhóm 4 người

Đề bài thiết kế **3 vai chuẩn** cho bàn 3–4 người. Với **4 thành viên**, cách chia cân bằng và hiệu quả nhất là **2 Kỹ sư cổng + 1 Sản phẩm & Kinh doanh + 1 Vận hành & Pháp lý**:

| Thành viên | Vai trò trong Lab | Thế mạnh phù hợp | File phụ trách chính |
| :--- | :--- | :--- | :--- |
| **Thành viên 1 (TV1)** *(Trưởng nhóm)* | **Kỹ sư cổng 1 (Lead Code & Git)** | Code Python tốt, nắm vững Git & CLI | `lab10/guards.py`, quản lý Git/Checkpoint, chạy lệnh `eval`, `gate`, `checkpoint`, `grade` |
| **Thành viên 2 (TV2)** | **Kỹ sư cổng 2 (Trace, Test & Monitor)** | Đọc hiểu code/log, tư duy test & tìm bug | `lab10/monitors.py`, chạy lệnh `trace`, phân tích lỗi chìm, viết Behavioral Test (`--adhoc`), phụ code `guards.py` |
| **Thành viên 3 (TV3)** | **Sản phẩm và Kinh doanh (PM / Biz)** | Tư duy dữ liệu, tài chính, ROI, lập luận quyết định | `config/acceptance_criteria.json`, mục `business` trong `config/operating_gates.json`, chủ trì **Phiếu A**, mục B3/B7.4/B8 (**Phiếu B**), mục C5/C12 (**Phiếu C**) |
| **Thành viên 4 (TV4)** | **Vận hành và Pháp lý (Ops / Legal)** | Cẩn thận, tư duy quy trình, rủi ro con người & pháp lý | Mục `operations` & `legal` trong `config/operating_gates.json`, `submission/submission.json`, chủ trì HAZOP, Checklist 9 nhóm, Runbook 1–5 (**Phiếu B & C**) |

---

## 3. Chi tiết công việc từng người theo Timeline (240 phút)

### Giai đoạn 0: Phút 0–15 · Cài đặt & Khởi tạo (CP1)
- **TV1 (Kỹ sư cổng 1 - Trưởng nhóm):**
  - Tạo repo đúng chuẩn tên `K5-L3A-DAY10-4MEMS-PoCtoPilotGate1` (chế độ Private, mời tài khoản chấm).
  - Cài đặt `git remote add upstream ...`, cấu hình `git config user.name` và `user.email`.
  - Chạy `python -m unittest discover -s tests` đảm bảo báo `Ran 13 tests ... OK`.
- **TV2, TV3, TV4:** Điền thông tin cá nhân vào bảng thành viên trong `TEAM.md`, đọc `data/world.json` và `lab10/agent.py` để hiểu các điểm yếu của trợ lý.

---

### Giai đoạn 1: Phút 15–65 · Thiết lập Tiêu chí & Ký (CP2 - Phiếu A)
*(Lưu ý: Tuyệt đối CHƯA chạy `lab10.eval` ở giai đoạn này)*
- **TV3 (Sản phẩm & Kinh doanh):**
  - Làm **Câu 1.1** (Mục tiêu cấp hệ thống - mục A1).
  - Làm **Câu 1.6** (Mục A4): Viết câu tiêu chí *"Nếu ... thì chúng tôi sẽ ..."*, trả lời 4 câu hỏi soát, viết 2 câu ranh giới đầu ra.
  - Điền đầy đủ ngưỡng vào `config/acceptance_criteria.json` (dựa trên `ops_facts` và `ops_limits` trong `data/world.json`, không chép y nguyên file example).
- **TV4 (Vận hành & Pháp lý):**
  - Làm **Câu 1.2** (Mục tiêu nhìn từ chị Oanh kế toán đối soát `NV-OANH` và chị Hạnh trưởng ca CSKH `NV-HANH` - mục A1).
  - Làm **Câu 1.4** (Thiết kế Telemetry production không có nhãn, có khung thời gian & ngưỡng báo động - mục A2 cột phải).
- **TV2 (Kỹ sư cổng 2):**
  - Làm **Câu 1.3** (Thiết kế Offline metric cho 1 bước của agent: Thước đo → Dữ liệu → Cách tính → Điểm mù - mục A2 cột trái).
  - Cùng cả nhóm chốt nhanh **Câu 1.5** (Đọc khoảng tin cậy 95% - mục A3).
- **TV1 (Kỹ sư cổng 1):**
  - Đọc rà soát code `lab10/agent.py` và `lab10/tools.py` để chuẩn bị sẵn logic cho `guards.py` ở Vòng 1.
  - **Đúng phút 60–65:** Kiểm tra file JSON của TV3, chạy lệnh ký `python -m lab10.criteria sign`, commit và push lên GitHub, điền mục **A5**.

---

### Giai đoạn 2A: Phút 65–85 · Đo Baseline & Tìm rủi ro (CP3 phần 1 - Phiếu B)
- **TV1 (Kỹ sư cổng 1):**
  - **Câu 2.1 (Mục B0, B1):** Chạy `eval --suite base --stage base` và `gate`, ghi mã lần chạy vào B0 & B1, phân tích ưu/nhược điểm tự chặn vs. người duyệt.
- **TV2 (Kỹ sư cổng 2):**
  - **Câu 2.2 (Mục B2):** Chạy `trace --suite base --ticket T-002 --seed 55`, phân tích lỗi model tin lời khách khai (`model_override`) và điền bảng soát lỗi 3 phần ở B2.
- **TV3 (Sản phẩm & Kinh doanh):**
  - **Câu 2.3 (Mục B3):** Điền Bản đồ dữ liệu (nguồn sự thật vs. bản sao) và nêu 1 ví dụ Drift cụ thể trong 3 tháng tới (ví dụ: đổi chính sách sang `REFUND-v4` ngày `2026-12-01` trong `world.json`).
- **TV4 (Vận hành & Pháp lý):**
  - **Câu 2.4 (Mục B4, B5):** Viết bảng HAZOP vòng 1 trên 1 tool ghi (≥ 3 dòng kỹ thuật + ≥ 2 dòng ngoài kỹ thuật) và điền Checklist 9 nhóm việc go-live lần 1 (bắt buộc gắn tên PIC cụ thể cho từng dòng).
- **Cả 4 người (Phút 75–85):**
  - **Câu 2.5 (Mục B6):** Làm Pre-mortem 4 lăng kính (Kỹ thuật, Kinh doanh, Con người & Vận hành, Pháp lý) và chọn ra 2–3 lý do để code thành cổng phòng ngừa.

---

### Giai đoạn 2B: Phút 85–115 · Dựng Cổng Vòng 1 & Quyết định v1 (CP3 phần 2 - Phiếu B)
- **TV1 (Kỹ sư cổng 1):**
  - **Câu 2.6 (Mục B7.1):** Viết 2–3 cổng phòng ngừa trong `lab10/guards.py` (ví dụ: kiểm tra `db_delay_days`, kiểm tra `effective_policy`, chặn directive injection, kiểm tra `entitlement_vnd`, kiểm tra kiện hàng bị lỗi, chặn phê duyệt giả/hết hạn...).
  - Chạy `eval --suite base --stage after` và `unittest` để đảm bảo không làm hỏng ticket hợp lệ. Điền bảng B7.1.
- **TV2 (Kỹ sư cổng 2):**
  - **Câu 2.7 (Mục B7.2):** Viết 2 bước cụ thể tránh rò rỉ dữ liệu (data leakage / overfitting vào bộ base).
  - **Câu 2.8 (Mục B7.3):** Cùng TV3 thiết kế 1 tính chất (behavioral test) và chạy 2 "ticket hiểm" bằng lệnh `trace --adhoc`, dán kết quả vào B7.3 (giữ lại để đi phản biện bàn khác lúc Demo).
- **TV3 (Sản phẩm & Kinh doanh):**
  - **Câu 2.9 (Mục B7.4):** Điền mục `business` trong `config/operating_gates.json` (`daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`, `pilot_scope`, `roi_min`) kèm lý do dựa trên `ops_limits` & `ops_facts`.
  - **Phút 105–115 (Mục B8):** Cùng TV1 chạy `checkpoint` → `eval --stage prepared` → `gate`, sau đó viết **Quyết định Gate 1 v1** vào mục B8.
- **TV4 (Vận hành & Pháp lý):**
  - **Câu 2.10 (Mục B7.5, B7.6):** Điền mục `operations` và `legal` trong `config/operating_gates.json` (`pic`, `approver_id`, `reviewers_on_shift`, `max_queue_wait_minutes`, `pii_fields_blocked_to_third_party` = `["recipient_contact", "customer_note"]`, `carrier_fault_requires_recorded_cause` = `true`...).
  - Viết **Runbook phần 1–3** (B7.5) và kịch bản **Giờ cao điểm** (B7.6) khớp 100% với các con số trong config.

---

### Giai đoạn 3: Phút 125–200 · Xử lý Thẻ Sự cố & Quyết định v2 (CP4 & CP5 - Phiếu C)
- **Phút 125–135 (Câu 3.0 - Mục C0, C1):**
  - **TV1:** Kéo thẻ sự cố từ `upstream`, ghi tên thẻ `Sx` vào đầu `templates/form-c-incident.md`, chạy ngay `python -m lab10.grade --incident Sx` trước khi sửa bất kỳ thứ gì.
  - **TV3 & TV4:** Đọc kết quả mốc `prepared`, điền C0, C1 (đối chiếu lại Pre-mortem ở B6).
- **Phút 135–155 (Câu 3.1–3.4 - Phân tích sự cố):**
  - **TV2:** Dò `trace` ít nhất 2 ticket hỏng theo kiểu khác nhau của thẻ `Sx`, điền **Bảng soát lỗi C2** (ít nhất 2 nguồn lỗi khác nhau, ≥ 1 lỗi chìm).
  - **TV4:** Làm **Phần riêng theo thẻ (Mục C3)**, viết **HAZOP của thẻ (Mục C4, ≥ 3 dòng)** và viết **Giả định môi trường (Câu 3.3 - Mục C5)**.
  - **TV3:** Viết **Specification (Câu 3.2 - Mục C5)** và cùng cả nhóm vẽ **Fault Tree TRƯỚC khi sửa (Câu 3.4 - Mục C6)**.
- **Phút 155–185 (Câu 3.5–3.7 - Sửa lỗi, Monitor & Cập nhật hồ sơ):**
  - **TV1:** Sửa code trong `lab10/guards.py` để chặn nguyên nhân kỹ thuật của thẻ `Sx`. Chạy `eval` và `grade` kiểm tra.
  - **TV2:** Viết hàm chỉ số theo dõi mới trong `lab10/monitors.py` để bắt đúng dấu hiệu sự cố (`6 monitor ✅`), điền **Mục C8** và bảng sửa **Mục C7**.
  - **TV3:** Tinh chỉnh các thông số kinh doanh trong `config/operating_gates.json` nếu thẻ liên quan đến chi phí/phạm vi; vẽ **Fault Tree SAU khi sửa (Mục C9)**.
  - **TV4:** Tinh chỉnh thông số vận hành/pháp lý trong `config/operating_gates.json` (người trực, kiểm mẫu, `decision_note`); điền **Risk Register (Mục C10)**, cập nhật **Checklist 9 nhóm & Runbook 4–5 (Mục C11)**.
- **Phút 185–200 (Quyết định v2 & Gom bài):**
  - **TV3:** Viết **Quyết định Gate 1 v2** và **3 dòng bắt buộc** ở **Mục C12** (đảm bảo quyết định khớp chặt với bằng chứng và không chọn "Tiếp tục" nếu còn vượt trần).
  - **TV4:** Điền `submission/submission.json` (chép 3 dòng bắt buộc từ C12 sang).
  - **TV1:** Chạy `python -m lab10.check_submission --collect`, cùng cả nhóm rà soát xử lý hết các mục báo `[THIẾU]` cho tới khi hiện `ĐỦ THÀNH PHẦN`.
  - **Cả 4 người:** Tự viết phần đóng góp cá nhân và Exit ticket vào mục `## HoVaTen-MSSV` trong `TEAM.md`.

---

### Giai đoạn 4: Phút 200–240 · Demo, Phản biện & Nộp bài
- **Khi trình bày (5 phút):**
  - **TV1** chiếu báo cáo 3 cột `base · prepared · after` và giải thích cổng vòng 1 đỡ được gì.
  - **TV2 & TV4** giải thích phần sửa vòng 2 (code, con số hay người) và chỉ số monitor mới.
  - **TV3** chốt quyết định v2 và các con số bảo vệ quyết định đó.
- **Khi phản biện bàn đối diện:**
  - **TV2** tung 2 "ticket hiểm" đã chuẩn bị ở câu 2.8 (`--adhoc`) hoặc yêu cầu đổi thử số người trực trong `operating_gates.json`.
- **Sau Demo (trước phút 240):**
  - **TV1** khôi phục lại mọi thông số đã thử nghiệm lúc demo, chạy lại `grade` và `check_submission --collect` để nhận `ĐỦ THÀNH PHẦN`, rồi `git commit` & `git push` lần cuối.
  - **Cả 4 thành viên** tự nộp link repo lên LMS cá nhân.
