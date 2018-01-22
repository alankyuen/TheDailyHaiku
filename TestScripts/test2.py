truth_phonemes = "12345567890"
phoneme_matches = [False for i in truth_phonemes]
truth_phonemes_2d = [[p,p*2] for p in truth_phonemes]
print(truth_phonemes_2d)
detected_phonemes = "11233995678890"

n = len(truth_phonemes)
m = len(detected_phonemes)
interval = m/n
for i in range(len(truth_phonemes_2d)):
    for variation in truth_phonemes_2d[i]:
        print(variation, detected_phonemes[max((i*interval),0):min(((i+1)*interval), m)])
        if(variation in detected_phonemes[max((i*interval),0):min(((i+1)*interval), m)]):

            phoneme_matches[i] = True

print(phoneme_matches)


"""
print(variation, detected_phonemes[max((i*interval) - 1,0):min(((i+1)*interval) + 1, m)])
if(variation in detected_phonemes[max((i*interval) - 1,0):min(((i+1)*interval) + 1, m)]):
"""
