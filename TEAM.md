# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): 4MEMS
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-4MEMS-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S8`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Hà Anh | 2A202603605 | Kỹ sư cổng 1 (Lead Code & Git) | X |
|   2 | Trần Thành Nam | 2A202603564 | Kỹ sư cổng 2 (Trace, Test & Monitor) | |
|   3 | Đỗ Đắc Duy | 2A202603604 | Vận hành và Pháp lý (Ops / Legal) | |
|   4 | Lê Xuân Hạ | 2A202603571 | Sản phẩm và Kinh doanh (PM / Biz) | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenHaAnh-2A202603605

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng 1 (Trưởng nhóm · Lead Code & Git).
- **Câu của đề & Mục phiếu:** Câu 1.5 (Phiếu A mục A3), Ký tiêu chí (Phiếu A mục A5), Câu 2.1 (Phiếu B mục B0, B1), Câu 2.5 (Phiếu B mục B6), Câu 2.6 (Phiếu B mục B7.1), Chốt cổng vòng 1 (Phiếu B mục B8), Câu 3.0 & 3.5 (Phiếu C mục C0, C1, C7).
- **File phụ trách:** `lab10/guards.py`, `lab10/guards_round1.py`, `config/acceptance_criteria.lock`, `config/round1.lock`, quản lý nhánh Git và chạy `lab10.eval`, `lab10.gate`, `lab10.checkpoint`, `lab10.grade`, `lab10.check_submission`.

### Đóng góp cụ thể

- Khởi tạo repo của bàn, cấu hình Git, ký và niêm phong Bản tiêu chí chấp nhận trước lần đánh giá đầu tiên.
- Chạy đánh giá baseline trên bộ nền, phân tích kết quả theo kho/hãng và đề xuất cơ chế kết hợp tự chặn với người duyệt ở mục B1.
- Thiết kế và lập trình 3 cổng phòng ngừa cấp hệ thống trong `lab10/guards.py` (`pre_guard` kiểm tra đơn/chủ đơn và ghim `H.effective_policy`; `write_gate` đối chiếu `H.entitlement_vnd` theo `H.db_delay_days`, chặn hoàn đúp, xác thực `_valid_approval` với 6 điều kiện, kiểm soát trần `300.000đ/khách/ngày`, kiểm tra `H.carrier_at_fault` cho đúng kiện trễ và lọc sạch PII khỏi `notify_carrier`). Có sử dụng trợ lý AI để rà soát cú pháp code và kiểm tra tính đầy đủ của các nhánh điều kiện trong `guards.py`.
- Chốt mốc `prepared` (`aace4610`), nhận thẻ sự cố `S8`, chạy kiểm tra 3 mốc (`base · prepared · after`) và gom bài nộp đạt `ĐỦ THÀNH PHẦN`.

### Bằng chứng

- Mã commit ký tiêu chí: `72eca32` (`Sign acceptance criteria`, hash `730c1d36`); commit chốt vòng 1: `21f1932` (hash checkpoint `aace4610`); commit nhận thẻ S8: `1fdb74a`.
- Mã lần chạy: `R-base-before-20261118-153616-394096` (baseline), `R-base-after-20261118-161506-93ed44`, `R-base-prepared-20261118-161506-93ed44` (prepared vòng 1), `R-S8-grade-20261118-170314-93ed44` và `R-S8-grade-20261118-170740-f6da77`.
- Dòng trong phiếu: Phiếu A mục A5; Phiếu B mục B0, B1, B6, B7.1, B8; Phiếu C mục C0, C1, C7.

### Exit ticket

- **Một điều học được:** Một cổng kiểm tra tất định đặt ngay trước lệnh ghi (`write_gate`) đối chiếu trực tiếp với nguồn sự thật (tracking DB, bảng `approvals` và sổ cái `ledger`) có thể chặn đứng hoàn toàn cả lỗi ảo giác của model lẫn lỗi lạm dụng mã phê duyệt mà không cần sửa prompt.
- **Một điều còn chưa chắc:** Trong môi trường production thực tế khi tracking DB hoặc dịch vụ tra cứu `approvals` bị trễ đồng bộ vài phút (eventual consistency), nên giữ ticket chờ thử lại bao lâu trước khi chuyển hẳn sang hàng chờ của `NV-HANH` để không làm tăng đột biến `escalation_rate`.

---

## TranThanhNam-2A202603564

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng 2 (Trace, Behavioral Test & Monitor).
- **Câu của đề & Mục phiếu:** Câu 1.3 (Phiếu A mục A2 cột Offline), Câu 2.2 (Phiếu B mục B2), Câu 2.7 & 2.8 (Phiếu B mục B7.2, B7.3), Câu 3.1 & 3.6 (Phiếu C mục C2, C8).
- **File phụ trách:** `lab10/monitors.py`, `templates/form-a-criteria.md` (mục A2), `templates/form-b-evaluation-gates.md` (mục B2, B7.2, B7.3), `templates/form-c-incident.md` (mục C2, C8).

### Đóng góp cụ thể

- Thiết kế offline metric đo tỷ lệ chọn đúng phiên bản chính sách hoàn tiền đang có hiệu lực (`policy.policy_id == effective_policy(as_of)`) ở mục A2.
- Chạy `lab10.trace` phân tích ca hỏng `T-002@55` trên bộ nền, phân loại hai lỗi chìm (hoàn sai `20.000đ` và phạt oan hãng `VNX` do `model_override`) ở mục B2.
- Xây dựng quy trình 2 bước chống rò rỉ dữ liệu (B7.2) và thiết kế 2 "ticket hiểm" kiểm thử tính chất bằng `--adhoc` trên đơn `O-1002` và `O-1001` (B7.3).
- Dò trace các ca hỏng của thẻ `S8` (`S8-01@11`, `S8-02@11`, `S8-03@11`, `S8-06@11`, `S8-43@11`), điền bảng soát lỗi C2 và viết 3 hàm chỉ số theo dõi mới trong `lab10/monitors.py` (`approval_or_cap_risk_rate`, `staff_recheck_rate`, `max_queue_wait_minutes`). Có dùng trợ lý AI để hỗ trợ rà soát câu chữ trong bảng soát lỗi.

### Bằng chứng

- Mã commit: `9986633` (`B7.3 commit`), `56aed6a` (merge PR #6).
- Mã lần chạy: `R-S8-after-20261118-170740-f6da77`, `R-base-after-20261118-170740-f6da77`, `R-S8-grade-20261118-170740-f6da77` (`6 monitor ✅` sáng đèn cả 3 chỉ số mới).
- Dòng trong phiếu: Phiếu A mục A2 (cột Offline); Phiếu B mục B2, B7.2, B7.3; Phiếu C mục C2, C8.

### Exit ticket

- **Một điều học được:** Các lỗi nguy hiểm nhất của agent có quyền ghi sổ thường là "lỗi chìm" (trạng thái trả về vẫn là `refunded` thành công nhưng dùng mã phê duyệt đã hết hạn hoặc đã dùng cho đơn khác), nên monitor trong production không thể chỉ đếm `escalation_rate` mà phải đo trực tiếp tỷ lệ chạm ranh giới phê duyệt và tỷ lệ nhân viên phải kiểm lại (`staff_recheck_rate`).
- **Một điều còn chưa chắc:** Làm sao thiết kế ngưỡng báo động động (dynamic threshold) cho `approval_or_cap_risk_rate` vào các ngày sale lớn khi số lượng đơn giá trị cao tăng tự nhiên mà không gây báo động giả (false alarm).

---

## DoDacDuy-2A202603604

### Phần việc phụ trách

- **Vai trong bàn:** Vận hành và Pháp lý (Ops / Legal).
- **Câu của đề & Mục phiếu:** Câu 1.2 & 1.4 (Phiếu A mục A1, A2 cột Telemetry production), Câu 2.4 (Phiếu B mục B4 HAZOP vòng 1, B5 Checklist 9 nhóm), Câu 2.10 (Phiếu B mục B7.5 Runbook 1–3, B7.6 Giờ cao điểm), Câu 3.1, 3.3, 3.7 (Phiếu C mục C3.1, C3.4, C4, C5 câu 3.3, C10 Risk register, C11 Checklist & Runbook 4–5).
- **File phụ trách:** `config/operating_gates.json` (mục `operations` và `legal`), `submission/submission.json`, `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`.

### Đóng góp cụ thể

- Xác định mục tiêu từ góc nhìn kế toán đối soát (`NV-OANH`) và trưởng ca CSKH (`NV-HANH`), thiết kế telemetry production phát hiện hành động rủi ro gửi hãng theo cửa sổ trượt 60 phút ở Phiếu A.
- Thực hiện phân tích HAZOP vòng 1 trên `file_carrier_fault` và 3 thành phần ngoài kỹ thuật (Người duyệt, Dữ liệu gửi bên thứ ba, Ngân sách), lập Checklist 9 nhóm việc go-live có gắn PIC cụ thể.
- Thiết lập các cổng vận hành và pháp lý trong `config/operating_gates.json` (`pic = "NV-TUNG"`, `approver_id = "NV-HANH"`, `reviewers_on_shift = 1`, `max_queue_wait_minutes = 60`, `decision_note = true`, `review_sampling_pct = 10`, chặn trường PII `recipient_contact`, `customer_note` và bật `carrier_fault_requires_recorded_cause = true`).
- Phân tích hiệu chỉnh lòng tin cho thẻ `S8` (mục C3.1, C3.4), viết HAZOP của thẻ S8 (mục C4), cập nhật Risk register (C10), Runbook 4–5 (C11) và điền `submission/submission.json`. Có tham khảo AI để chuẩn hóa cấu trúc bảng Runbook.

### Bằng chứng

- Mã commit: `5a80823` (`Add operations and legal gates`), `52f8dac` (merge PR #5).
- Mã lần chạy: `R-base-prepared-20261118-161506-93ed44`, `R-S8-grade-20261118-170740-f6da77` (`Niềm tin của nhân viên duyệt: đạt`, `recheck_pct = 10%`, `queue.stuck = 0`).
- Dòng trong phiếu: Phiếu A mục A1 (câu 1.2), A2 (câu 1.4); Phiếu B mục B4, B5, B7.5, B7.6; Phiếu C mục C3.1, C3.4, C4, C5 (câu 3.3), C10, C11.

### Exit ticket

- **Một điều học được:** Lòng tin của nhân viên vận hành không thể giải quyết chỉ bằng việc sửa thuật toán của model; nó đòi hỏi sự kết hợp giữa tính minh bạch ở từng quyết định (`decision_note`), việc tôn trọng ranh giới quyền hạn của người đứng tên (`NV-HANH`) và một tỷ lệ kiểm mẫu hợp lý (`10%`) để hàng chờ không bị vỡ trận.
- **Một điều còn chưa chắc:** Khi triển khai thật ở nhiều ca trực khác nhau, quy trình bàn giao quyền `approver_id` và `pic` lúc giao ca hoặc khi `NV-HANH` nghỉ phép cần được tự động hóa trong config như thế nào để không làm gián đoạn việc duyệt đơn vượt hạn mức.

---

## LeXuanHa-2A202603571

### Phần việc phụ trách

- **Vai trong bàn:** Sản phẩm và Kinh doanh (PM / Biz).
- **Câu của đề & Mục phiếu:** Câu 1.1 & 1.6 (Phiếu A mục A1, A4), Câu 2.3 (Phiếu B mục B3 Bản đồ dữ liệu & Drift), Câu 2.9 (Phiếu B mục B7.4 Cổng kinh doanh), Quyết định Gate 1 v1 (Phiếu B mục B8), Câu 3.2, 3.4, 3.7 & Quyết định Gate 1 v2 (Phiếu C mục C3.5, C5 câu 3.2, C6, C9, C12).
- **File phụ trách:** `config/acceptance_criteria.json`, `config/operating_gates.json` (mục `business`), `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`.

### Đóng góp cụ thể

- Xây dựng mục tiêu cấp hệ thống nối tiếp PRD v1.1 (Lab 9) và thiết lập bộ ngưỡng trong `config/acceptance_criteria.json` (`pass_rate_min = 0.90`, `pass_k_min = 0.85`, 3 ngưỡng an toàn `= 0`, `cost_per_ticket_vnd_max = 7500`, `roi_min = 0.30`, `queue_stuck_max = 0`) kèm 4 quy tắc `decision_rule` trước khi chạy đánh giá.
- Lập bản đồ dữ liệu (nguồn sự thật vs. bản sao) và phân tích kịch bản concept drift khi đổi chính sách `REFUND-v3` sang `REFUND-v4` vào ngày `2026-12-01` ở mục B3.
- Thiết lập cổng kinh doanh trong `config/operating_gates.json` (`daily_refund_cap_vnd = 1000000`, `cost_budget_per_ticket_vnd = 1200`, `pilot_scope` giới hạn ở 4 kho bán lẻ `HN, HCM, DN, CT` và loại kho sỉ `HCM-B2B`, `roi_min = 0.3`).
- Xây dựng Specification (câu 3.2), vẽ Fault Tree trước và sau khi sửa (mục C6, C9), tổng hợp bằng chứng chi phí/ROI theo phân khúc kho và viết Quyết định Gate 1 v1 (mục B8) cùng Quyết định v2 và 3 dòng bắt buộc (mục C12). Có dùng trợ lý AI để kiểm tra tính nhất quán của các con số chi phí và ROI.

### Bằng chứng

- Mã commit: `72eca32` (`Sign acceptance criteria`), `21f1932` (`LAB 10: chot cong vong 1, quyet dinh v1`).
- Mã lần chạy: `R-base-prepared-20261118-161506-93ed44` (chi phí `4.442đ/ticket`, `ROI = 1.25`), `R-S8-before-20261118-170315-93ed44`, `R-S8-prepared-20261118-170315-93ed44`, `R-S8-after-20261118-170741-f6da77` (chi phí `2.952đ/ticket`, `ROI = 2.39`, tiết kiệm ròng `+366.479đ/ngày`).
- Dòng trong phiếu: Phiếu A mục A1 (câu 1.1), A4 (câu 1.6); Phiếu B mục B3, B7.4, B8; Phiếu C mục C3.5, C5 (câu 3.2), C6, C9, C12.

### Exit ticket

- **Một điều học được:** Hiệu quả kinh tế (ROI và chi phí mỗi ticket) của một trợ lý AI phụ thuộc rất lớn vào chi phí vận hành của con người phía sau nó: trên thẻ S8, chỉ vì để lọt vài phê duyệt sai làm mất lòng tin mà nhân viên kiểm tay 100% khiến ROI rơi từ `+2.39` xuống `-2.45` (lỗ hơn 1,43 triệu đồng/ngày).
- **Một điều còn chưa chắc:** Khi `REFUND-v4` có hiệu lực từ `01/12/2026` hạ `auto_limit_vnd` từ `200.000đ` xuống `100.000đ`, tỷ lệ ticket phải chuyển người duyệt ở các kho có giá trị đơn cao (như `DN`) sẽ tăng bao nhiêu phần trăm và liệu ngưỡng `cost_per_ticket_vnd_max = 7.500đ` có cần điều chỉnh theo phân khúc kho hay không.
