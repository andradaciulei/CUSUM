import numpy
from scipy.stats import norm


class Mode:
    FORWARD = 'forward'
    BACKWARD = 'backward'


def get_CUSUM_P_value(epsilon: str, n: int):
    S = get_partial_sums(epsilon, n)

    z = numpy.max(numpy.abs(S))
    print('z=', z)

    k_min = int(numpy.floor((numpy.floor(-n / z) + 1)) / 4)
    k_max = int(numpy.floor((numpy.floor(n / z) - 1)) / 4)
    first_sum = 0
    for k in range(k_min, k_max + 1):
        first_term = norm.cdf((4 * k + 1) * z / numpy.sqrt(n))
        second_term = norm.cdf((4 * k - 1) * z / numpy.sqrt(n))
        first_sum += first_term - second_term

    k_min = int(numpy.floor(numpy.floor(-n / z - 3)) / 4)
    k_max = int(numpy.floor(numpy.floor(n / z) - 1) / 4)
    second_sum = 0
    for k in range(k_min, k_max + 1):
        first_term = norm.cdf((4 * k + 3) * z / numpy.sqrt(n))
        second_term = norm.cdf((4 * k + 1) * z / numpy.sqrt(n))
        second_sum += first_term - second_term

    return 1.0 - first_sum + second_sum


def get_partial_sums(epsilon: str, n: int):
    S = [get_adjusted_bit(epsilon[0])]
    for bit_index in range(1, n):
        S.append(S[bit_index - 1] + get_adjusted_bit(epsilon[bit_index]))
    print("S= ", S)
    return S


def get_adjusted_bit(bit: str):
    return -1 if bit == '0' else 1


def CUSUM(epsilon, mode):
    n = len(epsilon)

    if mode == Mode.BACKWARD:
        epsilon = epsilon[::-1]

    P_value = get_CUSUM_P_value(epsilon, n)
    print('P-value computed with mode: ' + mode + '=', P_value)
    if P_value > 0.01:
        print('Because P-value=' + str(P_value) + '>0.01 => sequence is random')
    else:
        print('Because P-value=' + str(P_value) + '<0.01 => sequence is NOT random')


def validate_inserted_bit_string(input):
    for bit in input:
        if bit not in ['0', '1']:
            return False
    return True


if __name__ == "__main__":
    # example given by NIST
    bit_string = '1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000'
    print('Example 3: \n For bit string: \n' + bit_string + '\n of length: ' + str(
        len(bit_string)) + '\n when running CUSUM test we obtain:')

    CUSUM(bit_string, Mode.BACKWARD)
    CUSUM(bit_string, Mode.FORWARD)

    string generated with numpy randint
    random_array = numpy.random.randint(2, size=(100,)).tolist()
    random_bit_string = "".join(map(str, random_array))
    print('Example 3: \n For bit string: \n' + random_bit_string + '\n of length: ' + str(
        len(random_bit_string)) + '\n when running CUSUM test we obtain:')

    CUSUM(random_bit_string, Mode.FORWARD)
    CUSUM(random_bit_string, Mode.BACKWARD)

    inserted_bit_string = input("Please enter a string:\n")
    while not validate_inserted_bit_string(inserted_bit_string):
        print("The inserted string is not a bit string, please provide another input")
        inserted_bit_string = input("Please enter a string:\n")

    print('Example 3: \n For bit string: \n' + inserted_bit_string + '\n of length: ' + str(
        len(inserted_bit_string)) + '\n when running CUSUM test we obtain:')
    CUSUM(inserted_bit_string, Mode.FORWARD)
    CUSUM(inserted_bit_string, Mode.BACKWARD)
