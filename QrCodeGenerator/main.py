#includy (shame)
from reedsolo import RSCodec, ReedSolomonError

# Funkcje
def CheckForType(string):
    # wersja 1.0 / tylko byte
    # if string.isnumeric():
    #     return "Numeric"
    # elif string.isalnum():
    #     return "Alphanumeric"
    # else:
        return "Byte"

def CreateDataSegment(string,array):
    for character in string:
        array.append(format(ord(character),'08b'))

def AddReedSolomon(data, ecc):
    rs = RSCodec(ecc)
    encoded_data = rs.encode(data.encode('utf-8'))
    return encoded_data

def FitToVersionNumber(bytes,ecc): #eec- error correction code
    for version, capacity in capacities:
        if bytes < capacity-1:
            return version

def CalculateBytePadding(codeWorks,maxCodeWorks):
    remainingCodeWorks = round((maxCodeWorks - codeWorks)/8)
    padding = ""
    for i in range(0,remainingCodeWorks):
        if i % 2 == 0:
            padding += "11101100"
        else:
            padding += "00010001"
    return padding

def ConcatenateSegments(seg0Mode,seg0Count,seg0Data,terminator,padding):
    bitSequence = ""
    bitSequence += seg0Mode + seg0Count + ''.join(seg0Data) + terminator + padding
    return bitSequence

def ConvertToHexadecimal(bitSequence):
    binary_segments = [bitSequence[i:i + 8] for i in range(0, len(bitSequence), 8)]
    hex_segments = [format(int(segment, 2), '02X') for segment in binary_segments]
    return hex_segments
# Reszta
print("-----------------------------------Super Tworzator kodu QR-----------------------------------")
word = input("Podaj Ciąg znaków do utorzenia kodu QR\n")  #"https://prisma-lab.pl/english/"

#zmienne globalne
capacities = [
        (1, 19), (2, 34), (3, 55), (4, 80), (5, 108), (6, 136), (7, 156), (8, 194), (9, 232),
        (10, 274), (11, 324), (12, 370), (13, 428), (14, 461), (15, 523), (16, 589), (17, 647),
        (18, 721), (19, 795), (20, 861), (21, 932), (22, 1006), (23, 1094), (24, 1174), (25, 1276),
        (26, 1370), (27, 1468), (28, 1531), (29, 1631), (30, 1735), (31, 1843), (32, 1955),
        (33, 2071), (34, 2191), (35, 2306), (36, 2434), (37, 2566), (38, 2702), (39, 2812), (40, 2956)
    ]

# Przypisanie trybu generowania
mode = CheckForType(word)

# przekształcenie na kod binarny
wordBinary = []
CreateDataSegment(word,wordBinary)
amountOfBytes = len(wordBinary)
amountOfBits = amountOfBytes *8

# Dopasowywanie Wersji

# W wersji 1.0 tylko low
# 1-low
# 2-medium
# 3-quartile
# 4-high
errorCorrectionLevel = 1
rsc = RSCodec(errorCorrectionLevel*10)
version = FitToVersionNumber(amountOfBytes,errorCorrectionLevel)
seg0Mode = "0100" # - zawsze 0100, ponieważ używam tylko trybu byte w wersji 1.0
bytesCount = len(wordBinary)
seg0Count = format(bytesCount, '08b')
terminator = "0000"
maxCodeWorks = capacities[version-1][1]*8 # potrzebne do obliczenia Byte Paddingu
sumBits = amountOfBits + len(seg0Mode) + len(seg0Count) + len(terminator)

#oblicznie Byte Paddingu
bytePadding = CalculateBytePadding(sumBits,maxCodeWorks) # - W kodowaniu QR, jeśli całkowita liczba bitów w danych nie jest wielokrotnością 8, konieczne może być dodanie bitów dopełniających, aby uzyskać pełny bajt (8 bitów). Dopełnianie to polega na dodawaniu zer na końcu danych. the right of the data.
sumBits += len(bytePadding)

#konkatenacja wszystkich danych w sekwencje
bitSequence = ConcatenateSegments(seg0Mode,str(seg0Count),wordBinary,terminator,bytePadding)

#przerobienie bitSequence na hexadecimal
hexSequence = ConvertToHexadecimal(bitSequence)

#dodanie Reed-Solomon Error Correction
encoded_data_reedSolomon = AddReedSolomon(bitSequence, errorCorrectionLevel)

# reedSolomonHex = ConvertToHexadecimal(encoded_data_reedSolomon)

amountOfDataCodeworks = sumBits/8

#debugging print
print("\nNumber of bytes: ", bytesCount,
      "\nMax Number of bits: ", maxCodeWorks,
      "\nNumber of bits: ", amountOfBits,
      "\nTotal Number of bits after contatenation: ", sumBits,
      "\nVersion: ", version,
      "\nSegment 0 Mode: ", seg0Mode,
      "\nSegment 0 Count: ", seg0Count,
      "\nTeminator: ", terminator,
      "\nByte Padding: ", bytePadding,
      "\nFinal Sequence Of Data Bits : ", bitSequence,
      "\nFinal Sequence Of Data Hex : ", hexSequence,
      "\n Number of data codeworks :", amountOfDataCodeworks,
      "\nEncoded Sequence with Reed-Solomon Hex: ")
