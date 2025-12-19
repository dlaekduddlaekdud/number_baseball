from rules.rule_base import GameRule


class NoConsecutiveRule(GameRule):
    """
    정렬했을 때 인접한 숫자끼리 차이가 1이면 금지
    예) [3,4,7] → 3,4가 연속 → False
    """
    def verify(self, numbers: list[int]) -> bool:
        nums = sorted(numbers)
        for i in range(len(nums) - 1):
            if abs(nums[i] - nums[i + 1]) == 1:
                return False
        return True

    def get_description(self) -> str:
        return "No consecutive digits (e.g., 3 & 4)"
