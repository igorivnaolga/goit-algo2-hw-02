from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using memoization (top-down DP)

    Args:
        length: The total length of the rod
        prices: A list of prices, where prices[i] is the price of a rod of length i+1

    Returns:
        A dictionary with max profit, list of cut lengths, and number of cuts
    """
    memo = {}  # Cache to store computed results
    cut_solution = {}  # To store which cut gives best profit for a given length

    def helper(n):
        if n == 0:
            return 0
        if n in memo:
            return memo[n]

        max_profit = float("-inf")
        best_cut = 0

        for i in range(1, n + 1):
            profit = prices[i - 1] + helper(n - i)
            if profit > max_profit:
                max_profit = profit
                best_cut = i

        memo[n] = max_profit
        cut_solution[n] = best_cut

        return max_profit

    max_profit = helper(length)

    # Reconstruct the list of cuts from cut_solution
    cuts = []
    n = length
    while n > 0:
        cuts.append(cut_solution[n])
        n -= cut_solution[n]

    return {"max_profit": max_profit, "cuts": cuts, "number_of_cuts": len(cuts) - 1}


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using tabulation (bottom-up DP)

    Args:
        length: The total length of the rod
        prices: A list of prices, where prices[i] is the price of a rod of length i+1

    Returns:
        A dictionary with max profit, list of cut lengths, and number of cuts
    """
    dp = [0] * (length + 1)  # dp[i] stores the max profit for rod of length i
    cuts = [0] * (length + 1)  # cuts[i] stores the best first cut for rod of length i

    for i in range(1, length + 1):
        max_profit = float("-inf")
        for j in range(1, i + 1):
            if j <= len(prices):
                if prices[j - 1] + dp[i - j] > max_profit:
                    max_profit = prices[j - 1] + dp[i - j]
                    cuts[i] = j
        dp[i] = max_profit

    # Reconstruct the list of cuts
    result_cuts = []
    n = length
    while n > 0:
        result_cuts.append(cuts[n])
        n -= cuts[n]

    return {
        "max_profit": dp[length],
        "cuts": result_cuts,
        "number_of_cuts": len(result_cuts) - 1,
    }


def run_tests():
    """Runs a list of test cases to validate the functions"""
    test_cases = [
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Basic case"},
        {"length": 3, "prices": [1, 3, 8], "name": "Best not to cut"},
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Uniform cuts"},
    ]

    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Rod length: {test['length']}")
        print(f"Prices: {test['prices']}")

        # Test memoization approach
        try:
            memo_result = rod_cutting_memo(test["length"], test["prices"])
            print("\nMemoization result:")
            print(f"Maximum profit: {memo_result['max_profit']}")
            print(f"Cuts: {memo_result['cuts']}")
            print(f"Number of cuts: {memo_result['number_of_cuts']}")
        except Exception as e:
            print(f"Memoization failed: {e}")

        # Test tabulation approach
        try:
            table_result = rod_cutting_table(test["length"], test["prices"])
            print("\nTabulation result:")
            print(f"Maximum profit: {table_result['max_profit']}")
            print(f"Cuts: {table_result['cuts']}")
            print(f"Number of cuts: {table_result['number_of_cuts']}")

            print("\nTest completed successfully!")
        except Exception as e:
            print(f"Tabulation failed: {e}")


if __name__ == "__main__":
    run_tests()
