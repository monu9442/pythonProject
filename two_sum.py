import collections
class Solution:
    @staticmethod
    def isPalindrome(self, x) -> bool:
        digit_list = []
        while x > 0:
            ld = x % 10
            digit_list.append(ld)
            x = x//10
        reversed_list = digit_list[::-1]
        for i in range(0, len(digit_list)):
            if digit_list[i] != reversed_list[i]:
                return False
        return True

solution = Solution()
print(Solution.isPalindrome(self= solution, x=-121))
