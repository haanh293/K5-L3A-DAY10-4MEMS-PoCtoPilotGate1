"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def approval_or_cap_risk_rate(trials):
    """Tỉ lệ lần chạy chạm tới bước xét phê duyệt vượt hạn mức (`approval_used`) hoặc bị guard chặn
    do phê duyệt không hợp lệ (`invalid_or_missing_approval`) / vượt trần hoàn tự động khách hàng trong ngày (`customer_daily_cap_exceeded`)."""
    if not trials:
        return 0.0
    hits = 0
    for t in trials:
        evs = t.get("events") or []
        if any(e.get("type") == "approval_used" or (
            e.get("type") == "guard" and e.get("kind") in ("invalid_or_missing_approval", "customer_daily_cap_exceeded")
        ) for e in evs):
            hits += 1
    return hits / len(trials)


def staff_recheck_rate(trials):
    """Tỉ lệ quyết định tự động (refunded/denied) bị nhân viên CSKH phải kiểm lại (`review_kind == 'recheck'`)."""
    auto = [t for t in trials if t.get("status") in ("refunded", "denied")]
    if not auto:
        return 0.0
    return sum(t.get("review_kind") == "recheck" for t in auto) / len(auto)


def max_queue_wait_minutes(trials):
    """Thời gian chờ người duyệt lâu nhất trong ca (phút)."""
    waits = [t["queue_wait_min"] for t in trials if t.get("queue_wait_min") is not None]
    return max(waits, default=0.0)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "approval_or_cap_risk_rate": approval_or_cap_risk_rate,
    "staff_recheck_rate": staff_recheck_rate,
    "max_queue_wait_minutes": max_queue_wait_minutes,
}
STARTER_MONITORS = ("escalation_rate",)
