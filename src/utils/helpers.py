def calculate_returns(prices):
    """
    Calculate the returns from a list of prices.
    :param prices: List of stock prices
    :return: List of returns
    """
    returns = []
    for i in range(1, len(prices)):
        returns.append((prices[i] - prices[i - 1]) / prices[i - 1])
    return returns
