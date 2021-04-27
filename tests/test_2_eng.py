from src.sentiment import sentiment

"""negative rew"""

text = """
warwick bad good reviews warwick shocks staff quite rude rooms fairly dirty, cut asked 
bandaid did not, requested bottle opener did not better service 
"""


def test_negative():
    print("Test 2 - ", sentiment(text, '../src/algos'))
    return sentiment(text, '../src/algos')[0]
