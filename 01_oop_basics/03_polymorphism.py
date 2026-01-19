"""
===========================================
ポリモーフィズム (Polymorphism)
===========================================

ポリモーフィズム（多態性）とは、同じインターフェースで
異なる型のオブジェクトを扱える性質です。

目的:
- 柔軟で拡張性のあるコード
- 条件分岐を減らす
- 「何をするか」と「どうするか」の分離
"""

from abc import ABC, abstractmethod
from typing import Protocol


# ============================================
# 継承によるポリモーフィズム
# ============================================
class PaymentMethod(ABC):
    """支払い方法の抽象クラス"""

    @abstractmethod
    def pay(self, amount: int) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class CreditCard(PaymentMethod):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: int) -> str:
        masked = "*" * 12 + self.card_number[-4:]
        return f"クレジットカード({masked})で¥{amount:,}を支払いました"

    def get_name(self) -> str:
        return "クレジットカード"


class BankTransfer(PaymentMethod):
    def __init__(self, bank_name: str, account: str):
        self.bank_name = bank_name
        self.account = account

    def pay(self, amount: int) -> str:
        return f"{self.bank_name}から¥{amount:,}を振り込みました"

    def get_name(self) -> str:
        return "銀行振込"


class ElectronicMoney(PaymentMethod):
    def __init__(self, service_name: str, balance: int):
        self.service_name = service_name
        self.balance = balance

    def pay(self, amount: int) -> str:
        if amount > self.balance:
            return f"残高不足です（残高: ¥{self.balance:,}）"
        self.balance -= amount
        return f"{self.service_name}で¥{amount:,}を支払いました（残高: ¥{self.balance:,}）"

    def get_name(self) -> str:
        return self.service_name


def process_payment(method: PaymentMethod, amount: int):
    """
    ポリモーフィズムの真価:
    この関数は具体的な支払い方法を知らなくても動作する
    """
    print(f"【{method.get_name()}】")
    print(f"  {method.pay(amount)}")


# ============================================
# ダックタイピングによるポリモーフィズム（Python的）
# ============================================
class FileLogger:
    def log(self, message: str):
        print(f"[FILE] {message}")


class ConsoleLogger:
    def log(self, message: str):
        print(f"[CONSOLE] {message}")


class RemoteLogger:
    def log(self, message: str):
        print(f"[REMOTE] Sending: {message}")


def write_log(logger, message: str):
    """
    ダックタイピング:
    loggerが何のクラスかは問わない
    log()メソッドを持っていれば動作する
    """
    logger.log(message)


# ============================================
# Protocol（構造的部分型）- Python 3.8+
# ============================================
class Drawable(Protocol):
    """描画可能なオブジェクトのプロトコル"""

    def draw(self) -> str:
        ...


class Button:
    def __init__(self, label: str):
        self.label = label

    def draw(self) -> str:
        return f"[  {self.label}  ]"


class TextField:
    def __init__(self, placeholder: str):
        self.placeholder = placeholder
        self.value = ""

    def draw(self) -> str:
        content = self.value if self.value else self.placeholder
        return f"| {content} |"


class CheckBox:
    def __init__(self, label: str, checked: bool = False):
        self.label = label
        self.checked = checked

    def draw(self) -> str:
        mark = "x" if self.checked else " "
        return f"[{mark}] {self.label}"


def render_ui(components: list[Drawable]):
    """Drawableプロトコルに従うオブジェクトを描画"""
    print("┌" + "─" * 30 + "┐")
    for component in components:
        print(f"│ {component.draw():<28} │")
    print("└" + "─" * 30 + "┘")


# ============================================
# 悪い例: ポリモーフィズムを使わない場合
# ============================================
def process_payment_bad(payment_type: str, amount: int, **kwargs):
    """
    悪い例: 型による条件分岐
    新しい支払い方法を追加するたびにこの関数を修正する必要がある
    """
    if payment_type == "credit_card":
        card = kwargs.get("card_number", "")
        print(f"クレジットカードで¥{amount:,}を支払いました")
    elif payment_type == "bank":
        print(f"銀行振込で¥{amount:,}を支払いました")
    elif payment_type == "emoney":
        print(f"電子マネーで¥{amount:,}を支払いました")
    # 新しい支払い方法を追加するには、ここにelif を追加...
    # → 開放閉鎖の原則（OCP）に違反


# ============================================
# 使用例
# ============================================
if __name__ == "__main__":
    print("="*50)
    print("継承によるポリモーフィズム")
    print("="*50)

    payments: list[PaymentMethod] = [
        CreditCard("1234567890123456"),
        BankTransfer("三菱UFJ銀行", "123-4567890"),
        ElectronicMoney("PayPay", 5000),
    ]

    for payment in payments:
        process_payment(payment, 1000)
        print()

    print("="*50)
    print("ダックタイピング")
    print("="*50)

    loggers = [FileLogger(), ConsoleLogger(), RemoteLogger()]

    for logger in loggers:
        write_log(logger, "アプリケーションが起動しました")

    print("\n" + "="*50)
    print("Protocol（構造的部分型）")
    print("="*50)

    ui_components: list[Drawable] = [
        TextField("名前を入力"),
        TextField("メールアドレス"),
        CheckBox("利用規約に同意する"),
        Button("送信"),
    ]

    render_ui(ui_components)
