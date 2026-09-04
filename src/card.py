from abc import ABC, abstractmethod


class Card(ABC):
    @abstractmethod
    def calculate_reward(self, mcc: str, currency: str, amount: float) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @staticmethod
    def round_to_nearest_1(amount: float) -> float:
        return amount // 1

    @staticmethod
    def round_to_nearest_5(amount: float) -> float:
        if amount < 5:
            return 0
        return (amount // 5) * 5


class UOBPrviMiles(Card):
    EXCLUDED_MCCS = {
        4829, 4900, 5199, 5960, 5965, 5993, 6012, 6050, 6051,
        6211, 6300, 6513, 6529, 6530, 6534, 6540, 7349, 7511,
        7523, 7995, 8062, 8211, 8220, 8241, 8244, 8249, 8299,
        8398, 8661, 8651, 8699, 8999, 9211, 9222, 9223, 9311,
        9402, 9405, 9399,
    }

    REGIONAL_CURRENCIES = {"idr", "myr", "thb", "vnd"}

    def get_name(self) -> str:
        return "UOB PRVI Miles"

    def calculate_reward(self, mcc: str, currency: str, amount: float) -> float:
        if int(mcc) in self.EXCLUDED_MCCS:
            return 0

        rounded = self.round_to_nearest_5(amount)
        if rounded == 0:
            return 0

        rate = self._get_rate(currency)
        return round(rounded * rate)

    def _get_rate(self, currency: str) -> float:
        if currency == "sgd":
            return 1.4
        if currency in self.REGIONAL_CURRENCIES:
            return 3.0
        return 2.4


CARDS: list[Card] = [
    UOBPrviMiles(),
]
