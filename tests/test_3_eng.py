from src.sentiment import sentiment

"""neutral rew"""

text = """
average facilities need overhaul feel dated, service ok. reason stay good rate need central location    
"""


def test_neutral():
    print("Test 3 - ", sentiment(text, '../src/algos'))
    return sentiment(text, '../src/algos')[0]
