"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _valid_approval(ctx, approval_id: str | None, order_id: str, amount_vnd: int) -> bool:
    if not approval_id:
        return False
    cands = ctx.tools.lookup_approvals(approval_id=approval_id)
    if not cands:
        return False
    a = cands[0]
    if a.get("status") != "valid":
        return False
    if a.get("ticket_id") and a.get("ticket_id") != ctx.ticket.get("ticket_id"):
        return False
    if a.get("order_id") and a.get("order_id") != order_id:
        return False
    if a.get("customer_id") and a.get("customer_id") != ctx.ticket.get("customer_id"):
        return False
    if a.get("expires_at") and a["expires_at"] < ctx.as_of:
        return False
    if a.get("max_vnd", 0) < amount_vnd:
        return False
    if ctx.tools.ledger_rows(approval_id=approval_id):
        return False
    return True


def pre_guard(ctx):
    # Cổng 1 (Pre-guard): Kiểm tra đơn/chủ đơn trước khi gọi LLM để tiết kiệm tiền máy
    # và ghim đúng phiên bản chính sách có hiệu lực theo ngày xử lý (as_of).
    oid = ctx.ticket.get("order_id")
    order = ctx.tools.lookup_order(oid) if oid else None
    if order is None:
        ctx.log("pre_order_missing", order_id=oid)
        return Verdict.escalate("không tìm thấy đơn (pre_guard)")
    if order.get("customer_id") != ctx.ticket.get("customer_id"):
        ctx.log("pre_wrong_customer", order_id=oid)
        return Verdict.escalate("người gửi không phải chủ đơn (pre_guard)")
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if pol is None:
        ctx.log("pre_no_effective_policy", as_of=ctx.as_of)
        return Verdict.escalate("không có chính sách hiệu lực cho ngày xử lý")
    return Verdict.allow(policy_id=pol["policy_id"])


def write_gate(ctx, action):
    tool = action.get("tool")
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if pol is None:
        return Verdict.escalate("không xác định được chính sách hiệu lực")

    # Cổng 2 (Write-gate cho issue_refund): Đối chiếu quyền lợi hoàn tiền từ tracking DB,
    # kiểm soát phê duyệt hợp lệ, chống hoàn trùng lặp và giới hạn trần khách/ngày.
    if tool == "issue_refund":
        oid = action.get("order_id")
        order = ctx.tools.lookup_order(oid)
        if order is None:
            return Verdict.escalate("không tìm thấy đơn khi hoàn tiền")
        # Chống hoàn đúp (do đơn đã hoàn ở sổ cái hoặc LLM retry khi confirm lỗi 429)
        if order.get("refund_status") == "REFUNDED" or ctx.tools.ledger_rows(order_id=oid):
            ctx.log("duplicate_refund_blocked", order_id=oid)
            return Verdict.deny("đơn đã được hoàn tiền trong sổ cái")

        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        # Nếu kiện hàng đang giao nhưng chưa thật sự trễ hoặc huỷ
        if parcel.get("status") in ("CANCELLED", "RETURNED"):
            return Verdict.deny("kiện hàng đã huỷ hoặc hoàn trả")

        delay = H.db_delay_days(parcel, ctx.as_of)
        cause = parcel.get("delay_cause")
        entitled = H.entitlement_vnd(pol, order, delay, cause)

        if entitled <= 0:
            ctx.log("unentitled_refund_blocked", order_id=oid, asked=action.get("amount_vnd"), db_delay=delay)
            return Verdict.deny("theo tracking DB và chính sách hiện hành, đơn chưa đủ điều kiện hoàn tiền")

        # Kiểm tra phê duyệt khi vượt hạn mức tự động của chính sách hiệu lực
        approval_id = action.get("approval_id")
        if entitled > pol["auto_limit_vnd"]:
            if not _valid_approval(ctx, approval_id, oid, entitled):
                ctx.log("invalid_or_missing_approval", order_id=oid, approval_id=approval_id, entitled=entitled)
                return Verdict.escalate("khoản hoàn vượt hạn mức tự động và chưa có phê duyệt hợp lệ")
        elif approval_id and not _valid_approval(ctx, approval_id, oid, entitled):
            approval_id = None

        # Kiểm tra trần hoàn tự động trên mỗi khách hàng trong ngày (ops_limits)
        limits = ctx.tools.ops_limits()
        cust_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
        if cust_cap is not None and not approval_id:
            cust_id = order["customer_id"]
            # Chỉ tính các dòng phát sinh trong ca hiện tại (có mặt trong events/ledger của ngày)
            cust_rows = [r for r in ctx.tools.ledger_rows(customer_id=cust_id)
                         if not r.get("approval_id") and not str(r.get("ticket_id", "")).startswith("T-OLD")]
            if sum(r["amount_vnd"] for r in cust_rows) + entitled > cust_cap:
                ctx.log("customer_daily_cap_exceeded", customer_id=cust_id, entitled=entitled)
                return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày: chuyển người duyệt")

        # Nếu model đề xuất sai số tiền (do tin lời khách / fail_open / prompt injection) hoặc sai payer -> sửa về đúng DB
        if (action.get("amount_vnd") != entitled or action.get("payer") != "LOGIX"
                or action.get("approval_id") != approval_id or action.get("basis") != "policy"):
            ctx.log("refund_modified_to_db", asked=action.get("amount_vnd"), entitled=entitled,
                    payer=action.get("payer"))
            return Verdict.modify(
                "điều chỉnh số tiền hoàn và bên chi trả khớp đúng nguồn sự thật DB",
                amount_vnd=entitled,
                payer="LOGIX",
                approval_id=approval_id,
                basis="policy",
            )
        return Verdict.allow()

    # Cổng 3 (Write-gate cho file_carrier_fault & notify_carrier): Bảo vệ bên thứ ba (hãng vận chuyển & người nhận).
    if tool == "file_carrier_fault":
        oid = action.get("order_id")
        order = ctx.tools.lookup_order(oid)
        if order is None:
            return Verdict.deny("không tìm thấy đơn")
        # Chống ghi lỗi trùng lặp cho cùng ticket
        if ctx.tools.fault_rows(ticket_id=ctx.ticket.get("ticket_id")):
            return Verdict.deny("đã ghi lỗi hãng cho ticket này")

        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(pol, parcel, delay):
            ctx.log("wrongful_fault_blocked", order_id=oid, parcel_id=parcel.get("parcel_id"),
                    cause=parcel.get("delay_cause"), delay=delay)
            return Verdict.deny("nguyên nhân trễ hoặc số ngày trễ trên DB không thuộc lỗi hãng vận chuyển")

        # Kiểm tra trần số lỗi tự động của một hãng trong ngày (ops_limits)
        max_strikes = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        carrier_id = parcel["carrier_id"]
        if max_strikes is not None and len(ctx.tools.fault_rows(carrier_id=carrier_id)) >= max_strikes:
            ctx.log("carrier_strike_cap_reached", carrier_id=carrier_id)
            return Verdict.deny("vượt trần số lỗi tự động tối đa trong ngày cho cùng một hãng")

        if (action.get("parcel_id") != parcel["parcel_id"]
                or action.get("carrier_id") != carrier_id
                or action.get("driver_id") != parcel.get("driver_id")
                or action.get("delay_days") != delay):
            ctx.log("fault_modified_to_target_parcel", parcel_id=parcel["parcel_id"], carrier_id=carrier_id)
            return Verdict.modify(
                "gán lỗi cho đúng kiện hàng và hãng gây trễ theo tracking DB",
                parcel_id=parcel["parcel_id"],
                carrier_id=carrier_id,
                driver_id=parcel.get("driver_id"),
                delay_days=delay,
            )
        return Verdict.allow()

    if tool == "notify_carrier":
        oid = ctx.ticket.get("order_id")
        order = ctx.tools.lookup_order(oid) or {}
        allowed_fields = set(pol.get("carrier_notice_fields") or ("order_id", "parcel_id", "district", "delay_days"))
        raw_payload = action.get("payload") or {}
        clean_payload = {k: v for k, v in raw_payload.items() if k in allowed_fields}
        if clean_payload != raw_payload:
            ctx.log("pii_stripped_from_carrier_notice", dropped=sorted(set(raw_payload) - set(clean_payload)))
            return Verdict.modify("lọc bỏ dữ liệu cá nhân người nhận và ghi chú khách khỏi thông báo gửi hãng",
                                  payload=clean_payload)
        return Verdict.allow()

    return Verdict.allow()
