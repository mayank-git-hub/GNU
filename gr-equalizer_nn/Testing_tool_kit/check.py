import numpy as np

def get_expected(path):
    f = open(path, 'rb')
    for i in f:
            string_format = str([str(i)])
    return np.array(string_format[2:-2].split('\\x0')[1:]).astype(np.float32)

training_size = 10000
expected = get_expected('training')[training_size:]
actual = get_expected('training_output')[training_size:]

print(actual.shape, expected.shape)
count = 0.0
for i in range(actual.shape[0]):
	if expected[i] == actual[i]:
		count+=1


print(count/expected.shape[0])

print(actual[-20:])
print(expected[-20:])