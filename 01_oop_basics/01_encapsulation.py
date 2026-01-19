"""
===========================================
カプセル化 (Encapsulation)
===========================================

カプセル化とは、データ（属性）とそれを操作するメソッドを
1つのクラスにまとめ、外部からの直接アクセスを制限することです。

目的:
- データの保護（不正な値の設定を防ぐ）
- 実装の詳細を隠蔽（内部構造の変更が外部に影響しない）
- インターフェースの明確化
"""


# ============================================
# 悪い例: カプセル化されていない
# ============================================
class BankAccountBad:
    def __init__(self, balance):
        self.balance = balance  # 外部から直接アクセス可能


# 問題点: 不正な操作が可能
bad_account = BankAccountBad(1000)
bad_account.balance = -500  # マイナス残高を設定できてしまう！
print(f"悪い例 - 残高: {bad_account.balance}")  # -500


# ============================================
# 良い例: カプセル化されている
# ============================================
class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0):
        self._owner = owner           # 慣例的なprotected（1つのアンダースコア）
        self.__balance = initial_balance  # private（2つのアンダースコア）
        self.__transaction_history = []

    # プロパティ: 読み取り専用アクセスを提供
    @property
    def balance(self) -> float:
        """残高を取得（読み取り専用）"""
        return self.__balance

    @property
    def owner(self) -> str:
        return self._owner

    # バリデーション付きのメソッド
    def deposit(self, amount: float) -> bool:
        """入金処理"""
        if amount <= 0:
            print(f"エラー: 入金額は正の数である必要があります")
            return False

        self.__balance += amount
        self.__record_transaction("deposit", amount)
        print(f"入金完了: ¥{amount:,.0f} → 残高: ¥{self.__balance:,.0f}")
        return True

    def withdraw(self, amount: float) -> bool:
        """出金処理"""
        if amount <= 0:
            print(f"エラー: 出金額は正の数である必要があります")
            return False
        if amount > self.__balance:
            print(f"エラー: 残高不足です（残高: ¥{self.__balance:,.0f}）")
            return False

        self.__balance -= amount
        self.__record_transaction("withdraw", amount)
        print(f"出金完了: ¥{amount:,.0f} → 残高: ¥{self.__balance:,.0f}")
        return True

    # privateメソッド: 内部でのみ使用
    def __record_transaction(self, transaction_type: str, amount: float):
        """取引履歴を記録（内部使用のみ）"""
        from datetime import datetime
        self.__transaction_history.append({
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        })

    def get_statement(self) -> list:
        """取引履歴のコピーを返す（元データは保護）"""
        return self.__transaction_history.copy()


# ============================================
# 使用例
# ============================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("良い例 - カプセル化された銀行口座")
    print("="*50)

    account = BankAccount("田中太郎", 10000)

    # プロパティでアクセス
    print(f"口座名義: {account.owner}")
    print(f"初期残高: ¥{account.balance:,.0f}")

    # メソッド経由で操作（バリデーション付き）
    print("\n--- 取引操作 ---")
    account.deposit(5000)
    account.withdraw(3000)
    account.withdraw(100000)  # エラー: 残高不足
    account.deposit(-1000)     # エラー: 不正な金額

    # 直接アクセスしようとしても...
    # account.__balance = -500  # AttributeError
    # account.balance = -500    # プロパティはsetterがないため設定不可

    print("\n--- 取引履歴 ---")
    for tx in account.get_statement():
        print(f"  {tx['type']}: ¥{tx['amount']:,.0f}")
