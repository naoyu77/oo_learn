"""
===========================================
継承 (Inheritance)
===========================================

継承とは、既存のクラス（親クラス）の属性とメソッドを
新しいクラス（子クラス）が引き継ぐ仕組みです。

目的:
- コードの再利用
- 階層的な関係の表現
- 共通の振る舞いの一元管理
"""

from abc import ABC, abstractmethod


# ============================================
# 基本的な継承
# ============================================
class Animal:
    """動物の基底クラス"""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def introduce(self) -> str:
        return f"私は{self.name}、{self.age}歳です"

    def speak(self) -> str:
        return "..."


class Dog(Animal):
    """犬クラス - Animalを継承"""

    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)  # 親クラスの__init__を呼び出し
        self.breed = breed  # 子クラス固有の属性

    def speak(self) -> str:  # メソッドのオーバーライド
        return "ワンワン！"

    def fetch(self) -> str:  # 子クラス固有のメソッド
        return f"{self.name}がボールを取ってきた！"


class Cat(Animal):
    """猫クラス - Animalを継承"""

    def __init__(self, name: str, age: int, indoor: bool = True):
        super().__init__(name, age)
        self.indoor = indoor

    def speak(self) -> str:
        return "ニャー！"

    def scratch(self) -> str:
        return f"{self.name}が爪を研いでいる"


# ============================================
# 抽象クラスを使った継承（推奨パターン）
# ============================================
class Shape(ABC):
    """図形の抽象基底クラス"""

    @abstractmethod
    def area(self) -> float:
        """面積を計算（子クラスで実装必須）"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """周囲の長さを計算（子クラスで実装必須）"""
        pass

    def describe(self) -> str:
        """共通の説明メソッド"""
        return f"面積: {self.area():.2f}, 周囲: {self.perimeter():.2f}"


class Rectangle(Shape):
    """長方形"""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Circle(Shape):
    """円"""

    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius


# ============================================
# 多重継承（注意して使用）
# ============================================
class Flyable:
    """飛べる能力を表すMixin"""

    def fly(self) -> str:
        return f"{self.name}が空を飛んでいる"


class Swimmable:
    """泳げる能力を表すMixin"""

    def swim(self) -> str:
        return f"{self.name}が泳いでいる"


class Duck(Animal, Flyable, Swimmable):
    """アヒル - 複数の能力を持つ"""

    def speak(self) -> str:
        return "ガーガー！"


# ============================================
# 使用例
# ============================================
if __name__ == "__main__":
    print("="*50)
    print("基本的な継承")
    print("="*50)

    dog = Dog("ポチ", 3, "柴犬")
    cat = Cat("タマ", 5)

    print(dog.introduce())  # 親クラスのメソッド
    print(f"犬種: {dog.breed}")
    print(f"鳴き声: {dog.speak()}")  # オーバーライドされたメソッド
    print(dog.fetch())  # 子クラス固有のメソッド

    print()
    print(cat.introduce())
    print(f"鳴き声: {cat.speak()}")

    print("\n" + "="*50)
    print("抽象クラスを使った継承")
    print("="*50)

    shapes: list[Shape] = [
        Rectangle(10, 5),
        Circle(7),
    ]

    for shape in shapes:
        print(f"{shape.__class__.__name__}: {shape.describe()}")

    # 抽象クラスは直接インスタンス化できない
    # shape = Shape()  # TypeError

    print("\n" + "="*50)
    print("多重継承（Mixin）")
    print("="*50)

    duck = Duck("ドナルド", 2)
    print(duck.introduce())
    print(duck.speak())
    print(duck.fly())
    print(duck.swim())

    # MRO（メソッド解決順序）の確認
    print(f"\nMRO: {[c.__name__ for c in Duck.__mro__]}")
