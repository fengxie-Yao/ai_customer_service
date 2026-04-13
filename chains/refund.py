# chains/refund.py

def handle_refund(data):
    if data["order_id"]:
        return "已进入退款审核流程"
    else:
        return "请提供订单号"