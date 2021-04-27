from src.sentiment import sentiment

"""positive rew"""

text = """
nice hotel expensive parking got good deal stay hotel anniversary, arrived late evening took advice previous reviews 
did valet parking, check quick easy, little disappointed non-existent view room room clean nice size, bed comfortable 
woke stiff neck high pillows, not soundproof like heard music room night morning loud bangs doors opening closing hear 
people talking hallway, maybe just noisy neighbors, 
aveda bath products nice, did not goldfish stay nice touch taken advantage staying longer, location great walking 
distance shopping, overall nice experience having pay 40 parking night
"""


def test_positive():
    print("Test 1 - ", sentiment(text, '../src/algos'))
    return sentiment(text, '../src/algos')[0]
