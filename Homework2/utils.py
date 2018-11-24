#utils.py 
import numpy as np

ZigzagTable = [[0, 1, 5, 6, 14, 15, 27, 28],
               [2, 4, 7, 13, 16, 26, 29, 42],
               [3, 8, 12, 17, 25, 30, 41, 43],
               [9, 11, 18, 24, 31, 40, 44, 53],
               [10, 19, 23, 32, 39, 45, 52, 54],
               [20, 22, 33, 38, 46, 51, 55, 60],
               [21, 34, 37, 47, 50, 56, 59, 61],
               [35, 36, 48, 49, 57, 58, 62, 63]]

QuantizationTable = [[[16, 11, 10, 16, 24, 40, 51, 61],
                      [12, 12, 14, 19, 26, 58, 60, 55],
                      [14, 13, 16, 24, 40, 57, 69, 56],
                      [14, 17, 22, 29, 51, 87, 80, 62],
                      [18, 22, 37, 56, 68, 109, 103, 77],
                      [24, 35, 55, 64, 81, 104, 113, 92],
                      [49, 64, 78, 87, 103, 121, 120, 101],
                      [72, 92, 95, 98, 112, 100, 103, 99]],
                     [[17, 18, 24, 47, 99, 99, 99, 99],
                      [18, 21, 26, 66, 99, 99, 99, 99],
                      [24, 26, 56, 99, 99, 99, 99, 99],
                      [47, 66, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99]],
                     [[17, 18, 24, 47, 99, 99, 99, 99],
                      [18, 21, 26, 66, 99, 99, 99, 99],
                      [24, 26, 56, 99, 99, 99, 99, 99],
                      [47, 66, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99],
                      [99, 99, 99, 99, 99, 99, 99, 99]]]

'''
@msg: generate a DCT transform matrix
@return: a DCT transform matrix
'''
def getDCTtable():
    A = []  # DCT transform matrix
    for i in range(8):
        for j in range(8):
            if i == 0:
                a = 1 / np.sqrt(8)
            else:
                a = 1 / 2
            A.append(a * np.cos((j + 0.5) * np.pi * i / 8))
    A = np.array(A).reshape(8, 8).tolist()
    return A

'''
@msg: get the amplitude of the num
@param int: num
@return: a string amlitude
'''
def getAmplitude(num):
        amplitude = bin(abs(num)).replace('0b', '')
        if num > 0:
            return amplitude
        else:
            return ''.join(list(map(lambda c: '1' if c == '0' else '1', amplitude)))

'''
@msg: convert amplitude to value
@param string: amplitude
@return: value
'''
def amplitudeToValue(amplitude):
    if amplitude[0] == '0':
        amplitude =  ''.join(list(map(lambda c: '1' if c == '0' else '1', amplitude)))
        return -int(amplitude, 2)
    else:
        return int(amplitude, 2)


DC_HuffmanTable = [['00', '010', '011', '100', '101', '110', '1110', '11110', 
                        '111110', '1111110', '11111110', '111111110'],
                   ['00', '01', '10', '110', '1110', '11110', '111110', '1111110',
                       '11111110', '111111110', '1111111110', '11111111110'],
                   ['00', '01', '10', '110', '1110', '11110', '111110', '1111110', 
                        '11111110', '111111110', '1111111110', '11111111110']]

AC_HuffmanTable = [[['1010', '00', '01', '100', '1011' ,'11010' ,'1111000' ,'11111000' ,'1111110110' ,'1111111110000010' ,'1111111110000011'],
                    ['1100' ,'11011' ,'1111001' ,'111110110' ,'11111110110' ,'1111111110000100' ,'1111111110000101' ,'1111111110000110' ,'1111111110000111' ,'1111111110001000'],
                    ['11100', '11111001', '1111110111', '111111110100', '1111111110001001', '1111111110001010', '1111111110001011', '1111111110001100', '1111111110001101', '1111111110001110'],
                    ['111010', '111110111', '111111110101', '1111111110001111', '1111111110010000', '1111111110010001', '1111111110010010', '1111111110010011', '1111111110010100', '1111111110010101'],
                    ['111011', '1111111000', '1111111110010110', '1111111110010111', '1111111110011000', '1111111110011001', '1111111110011010', '1111111110011011', '1111111110011100', '1111111110011101'],
                    ['1111010', '11111110111', '1111111110011110', '1111111110011111', '1111111110100000', '1111111110100001', '1111111110100010', '1111111110100011', '1111111110100100', '1111111110100101'],
                    ['1111011', '111111110110', '1111111110100110', '1111111110100111', '1111111110101000', '1111111110101001', '1111111110101010', '1111111110101011', '1111111110101100', '1111111110101101'],
                    ['11111010', '111111110111', '1111111110101110', '1111111110101111', '1111111110110000', '1111111110110001', '1111111110110010', '1111111110110011', '1111111110110100', '1111111110110101'],
                    ['111111000', '111111111000000', '1111111110110110', '1111111110110111', '1111111110111000', '1111111110111001', '1111111110111010', '1111111110111011', '1111111110111100', '1111111110111101'],
                    ['111111001', '1111111110111110', '1111111110111111', '1111111111000000', '1111111111000001', '1111111111000010', '1111111111000011', '1111111111000100', '1111111111000101', '1111111111000110'],
                    ['111111010', '1111111111000111', '1111111111001000', '1111111111001001', '1111111111001010', '1111111111001011', '1111111111001100', '1111111111001101', '1111111111001110', '1111111111001111'],
                    ['1111111001', '1111111111010000', '1111111111010001', '1111111111010010', '1111111111010011', '1111111111010100', '1111111111010101', '1111111111010110', '1111111111010111', '1111111111011000'],
                    ['1111111010', '1111111111011001', '1111111111011010', '1111111111011011', '1111111111011100', '1111111111011101', '1111111111011110', '1111111111011111', '1111111111100000', '1111111111100001'],
                    ['11111111000', '1111111111100010', '1111111111100011', '1111111111100100', '1111111111100101', '1111111111100110', '1111111111100111', '1111111111101000', '1111111111101001', '1111111111101010'],
                    ['1111111111101011', '1111111111101100', '1111111111101101', '1111111111101110', '1111111111101111', '1111111111110000', '1111111111110001', '1111111111110010', '1111111111110011', '1111111111110100'],
                    ['11111111001', '1111111111110101', '1111111111110110', '1111111111110111', '1111111111111000', '1111111111111001', '1111111111111010', '1111111111111011', '1111111111111100', '1111111111111101', '1111111111111110']],
                   [['00', '01', '100', '1010', '11000', '11001', '111000', '1111000', '111110100', '1111110110', '111111110100'],
                    ['1011', '111001', '11110110', '111110101', '11111110110', '111111110101', '1111111110001000', '1111111110001001', '1111111110001010', '1111111110001011'],
                    ['11010', '11110111', '1111110111', '111111110110', '111111111000010', '1111111110001100', '1111111110001101', '1111111110001110', '1111111110001111', '1111111110010000'],
                    ['11011', '11111000', '1111111000', '111111110111', '1111111110010001', '1111111110010010', '1111111110010011', '1111111110010100', '1111111110010101', '1111111110010110'],
                    ['111010', '111110110', '1111111110010111', '1111111110011000', '1111111110011001', '1111111110011010', '1111111110011011', '1111111110011100', '1111111110011101', '1111111110011110'],
                    ['111011', '1111111001', '1111111110011111', '1111111110100000', '1111111110100001', '1111111110100010', '1111111110100011', '1111111110100100', '1111111110100101', '1111111110100110'],
                    ['1111001', '11111110111', '1111111110100111', '1111111110101000', '1111111110101001', '1111111110101010', '1111111110101011', '1111111110101100', '1111111110101101', '1111111110101110'],
                    ['1111010', '11111111000', '1111111110101111', '1111111110110000', '1111111110110001', '1111111110110010', '1111111110110011', '1111111110110100', '1111111110110101', '1111111110110110'],
                    ['11111001', '1111111110110111', '1111111110111000', '1111111110111001', '1111111110111010', '1111111110111011', '1111111110111100', '1111111110111101', '1111111110111110', '1111111110111111'],
                    ['111110111', '1111111111000000', '1111111111000001', '1111111111000010', '1111111111000011', '1111111111000100', '1111111111000101', '1111111111000110', '1111111111000111', '1111111111001000'],
                    ['111111000', '1111111111001001', '1111111111001010', '1111111111001011', '1111111111001100', '1111111111001101', '1111111111001110', '1111111111001111', '1111111111010000', '1111111111010001'],
                    ['111111001', '1111111111010010', '1111111111010011', '1111111111010100', '1111111111010101', '1111111111010110', '1111111111010111', '1111111111011000', '1111111111011001', '1111111111011010'],
                    ['111111010', '1111111111011011', '1111111111011100', '1111111111011101', '1111111111011110', '1111111111011111', '1111111111100000', '1111111111100001', '1111111111100010', '1111111111100011'],
                    ['11111111001', '1111111111100100', '1111111111100101', '1111111111100110', '1111111111100111', '1111111111101000', '1111111111101001', '1111111111101010', '1111111111101011', '1111111111101100'],
                    ['11111111100000', '1111111111101101', '1111111111101110', '1111111111101111', '1111111111110000', '1111111111110001', '1111111111110010', '1111111111110011', '1111111111110100', '1111111111110101'],
                    ['1111111010', '111111111000011', '1111111111110110', '1111111111110111', '1111111111111000', '1111111111111001', '1111111111111010', '1111111111111011', '1111111111111100', '1111111111111101', '1111111111111110']],
                   [['00', '01', '100', '1010', '11000', '11001', '111000', '1111000', '111110100', '1111110110', '111111110100'],
                    ['1011', '111001', '11110110', '111110101', '11111110110', '111111110101', '1111111110001000', '1111111110001001', '1111111110001010', '1111111110001011'],
                    ['11010', '11110111', '1111110111', '111111110110', '111111111000010', '1111111110001100', '1111111110001101', '1111111110001110', '1111111110001111', '1111111110010000'],
                    ['11011', '11111000', '1111111000', '111111110111', '1111111110010001', '1111111110010010', '1111111110010011', '1111111110010100', '1111111110010101', '1111111110010110'],
                    ['111010', '111110110', '1111111110010111', '1111111110011000', '1111111110011001', '1111111110011010', '1111111110011011', '1111111110011100', '1111111110011101', '1111111110011110'],
                    ['111011', '1111111001', '1111111110011111', '1111111110100000', '1111111110100001', '1111111110100010', '1111111110100011', '1111111110100100', '1111111110100101', '1111111110100110'],
                    ['1111001', '11111110111', '1111111110100111', '1111111110101000', '1111111110101001', '1111111110101010', '1111111110101011', '1111111110101100', '1111111110101101', '1111111110101110'],
                    ['1111010', '11111111000', '1111111110101111', '1111111110110000', '1111111110110001', '1111111110110010', '1111111110110011', '1111111110110100', '1111111110110101', '1111111110110110'],
                    ['11111001', '1111111110110111', '1111111110111000', '1111111110111001', '1111111110111010', '1111111110111011', '1111111110111100', '1111111110111101', '1111111110111110', '1111111110111111'],
                    ['111110111', '1111111111000000', '1111111111000001', '1111111111000010', '1111111111000011', '1111111111000100', '1111111111000101', '1111111111000110', '1111111111000111', '1111111111001000'],
                    ['111111000', '1111111111001001', '1111111111001010', '1111111111001011', '1111111111001100', '1111111111001101', '1111111111001110', '1111111111001111', '1111111111010000', '1111111111010001'],
                    ['111111001', '1111111111010010', '1111111111010011', '1111111111010100', '1111111111010101', '1111111111010110', '1111111111010111', '1111111111011000', '1111111111011001', '1111111111011010'],
                    ['111111010', '1111111111011011', '1111111111011100', '1111111111011101', '1111111111011110', '1111111111011111', '1111111111100000', '1111111111100001', '1111111111100010', '1111111111100011'],
                    ['11111111001', '1111111111100100', '1111111111100101', '1111111111100110', '1111111111100111', '1111111111101000', '1111111111101001', '1111111111101010', '1111111111101011', '1111111111101100'],
                    ['11111111100000', '1111111111101101', '1111111111101110', '1111111111101111', '1111111111110000', '1111111111110001', '1111111111110010', '1111111111110011', '1111111111110100', '1111111111110101'],
                    ['1111111010', '111111111000011', '1111111111110110', '1111111111110111', '1111111111111000', '1111111111111001', '1111111111111010', '1111111111111011', '1111111111111100', '1111111111111101', '1111111111111110']]]


def getRunlength(t, size, huffcode):
    for i in range(16):
        if AC_HuffmanTable[t][i][size] == huffcode:
            return i