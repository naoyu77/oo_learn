# オブジェクト指向学習

## 学習内容

### カプセル化 (Encapsulation)

データと操作を1つのクラスにまとめ、外部からの直接アクセスを制限する。

**Pythonでの実現方法:**

| 記法 | 意味 |
|------|------|
| `_name` | 慣例的なprotected（基本これでOK） |
| `__name` | 名前マングリング（継承時の衝突回避用） |
| `@property` | 読み取り専用アクセスを提供 |

**ポイント:**
- `_`は強制ではなく「触らないで」という約束
- Pythonは「大人なんだから約束を守ってね」という文化
- バリデーションはメソッド経由で行う

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # 内部用

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
```

**Q: なぜ@propertyを使う？メンバー変数ではダメ？**

メンバー変数だと直接書き換えられてしまう:
```python
# メンバー変数の場合
account.balance = -99999  # できてしまう（危険）

# @propertyの場合
account.balance = -99999  # エラーになる（安全）
```

| 方法 | 読み取り | 書き込み |
|------|---------|---------|
| `self.balance`（メンバー変数） | できる | できる（危険） |
| `@property` + `self._balance` | できる | エラー（安全） |

変更は`deposit()`や`withdraw()`経由のみ → バリデーションできる
