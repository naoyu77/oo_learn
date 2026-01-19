"""
===========================================
抽象化 (Abstraction)
===========================================

抽象化とは、複雑な実装の詳細を隠し、
必要な機能だけをシンプルなインターフェースとして提供することです。

目的:
- 複雑さの管理
- 使いやすいインターフェースの提供
- 実装の詳細からの独立
"""

from abc import ABC, abstractmethod
from typing import Any
import json


# ============================================
# 抽象化の例: データベース接続
# ============================================
class Database(ABC):
    """
    データベースの抽象クラス
    利用者は具体的なDB実装を知らなくても使える
    """

    @abstractmethod
    def connect(self) -> None:
        """接続を確立"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """接続を切断"""
        pass

    @abstractmethod
    def execute(self, query: str) -> list[dict]:
        """クエリを実行"""
        pass

    # 共通の高レベルメソッド
    def find_by_id(self, table: str, id: int) -> dict | None:
        """IDで検索（共通実装）"""
        results = self.execute(f"SELECT * FROM {table} WHERE id = {id}")
        return results[0] if results else None


class MySQLDatabase(Database):
    """MySQL実装（実際はmysql-connector等を使用）"""

    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._connected = False

    def connect(self) -> None:
        print(f"MySQL: {self.host}に接続中...")
        # 実際の接続処理
        self._connected = True
        print("MySQL: 接続完了")

    def disconnect(self) -> None:
        print("MySQL: 切断中...")
        self._connected = False
        print("MySQL: 切断完了")

    def execute(self, query: str) -> list[dict]:
        if not self._connected:
            raise RuntimeError("データベースに接続されていません")
        print(f"MySQL: 実行 - {query}")
        # 実際のクエリ実行処理（ここではダミーデータ）
        return [{"id": 1, "name": "サンプル"}]


class SQLiteDatabase(Database):
    """SQLite実装"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._connected = False

    def connect(self) -> None:
        print(f"SQLite: {self.filepath}を開いています...")
        self._connected = True
        print("SQLite: 接続完了")

    def disconnect(self) -> None:
        print("SQLite: ファイルを閉じています...")
        self._connected = False

    def execute(self, query: str) -> list[dict]:
        if not self._connected:
            raise RuntimeError("データベースに接続されていません")
        print(f"SQLite: 実行 - {query}")
        return [{"id": 1, "name": "サンプル"}]


# ============================================
# ファサードパターンによる抽象化
# ============================================
class EmailService:
    """メール送信の詳細"""

    def send(self, to: str, subject: str, body: str):
        print(f"  [Email] To: {to}, Subject: {subject}")


class SMSService:
    """SMS送信の詳細"""

    def send(self, phone: str, message: str):
        print(f"  [SMS] To: {phone}, Message: {message[:20]}...")


class PushNotificationService:
    """プッシュ通知の詳細"""

    def send(self, device_id: str, title: str, body: str):
        print(f"  [Push] Device: {device_id}, Title: {title}")


class NotificationFacade:
    """
    通知サービスのファサード
    複雑な内部サービスをシンプルなインターフェースで提供
    """

    def __init__(self):
        self._email = EmailService()
        self._sms = SMSService()
        self._push = PushNotificationService()

    def notify_user(self, user: dict, message: str, title: str = "お知らせ"):
        """
        ユーザーに通知を送信
        利用者は内部の複雑さを知る必要がない
        """
        print(f"ユーザー {user['name']} に通知を送信:")

        if email := user.get("email"):
            self._email.send(email, title, message)

        if phone := user.get("phone"):
            self._sms.send(phone, message)

        if device_id := user.get("device_id"):
            self._push.send(device_id, title, message)


# ============================================
# 抽象化によるテスト容易性
# ============================================
class WeatherAPI(ABC):
    """天気APIの抽象クラス"""

    @abstractmethod
    def get_temperature(self, city: str) -> float:
        pass


class RealWeatherAPI(WeatherAPI):
    """本番用: 実際のAPIを呼び出す"""

    def get_temperature(self, city: str) -> float:
        # 実際はrequests等でAPIを呼び出す
        print(f"外部API呼び出し: {city}の気温を取得")
        return 25.0


class MockWeatherAPI(WeatherAPI):
    """テスト用: 固定値を返す"""

    def __init__(self, temperature: float = 20.0):
        self.temperature = temperature

    def get_temperature(self, city: str) -> float:
        return self.temperature


class WeatherReport:
    """天気レポート生成クラス"""

    def __init__(self, api: WeatherAPI):
        self._api = api  # 抽象に依存（依存性注入）

    def generate(self, city: str) -> str:
        temp = self._api.get_temperature(city)
        if temp >= 30:
            feeling = "暑い"
        elif temp >= 20:
            feeling = "快適"
        elif temp >= 10:
            feeling = "涼しい"
        else:
            feeling = "寒い"

        return f"{city}の気温は{temp}°C（{feeling}）です"


# ============================================
# 使用例
# ============================================
if __name__ == "__main__":
    print("="*50)
    print("データベース抽象化")
    print("="*50)

    # 利用者はどのDBを使っているか意識しなくてよい
    def fetch_user(db: Database, user_id: int):
        db.connect()
        user = db.find_by_id("users", user_id)
        db.disconnect()
        return user

    print("\n--- MySQL ---")
    mysql = MySQLDatabase("localhost", "root", "password", "myapp")
    fetch_user(mysql, 1)

    print("\n--- SQLite ---")
    sqlite = SQLiteDatabase("data.db")
    fetch_user(sqlite, 1)

    print("\n" + "="*50)
    print("ファサードによる抽象化")
    print("="*50)

    notifier = NotificationFacade()

    user = {
        "name": "田中太郎",
        "email": "tanaka@example.com",
        "phone": "090-1234-5678",
        "device_id": "device_abc123"
    }

    notifier.notify_user(user, "ご注文の商品が発送されました")

    print("\n" + "="*50)
    print("抽象化によるテスト容易性")
    print("="*50)

    # 本番環境
    print("\n--- 本番環境 ---")
    real_api = RealWeatherAPI()
    report = WeatherReport(real_api)
    print(report.generate("東京"))

    # テスト環境（APIを呼ばずにテスト可能）
    print("\n--- テスト環境 ---")
    mock_api = MockWeatherAPI(temperature=35.0)
    report = WeatherReport(mock_api)
    print(report.generate("東京"))

    mock_api = MockWeatherAPI(temperature=5.0)
    report = WeatherReport(mock_api)
    print(report.generate("東京"))
