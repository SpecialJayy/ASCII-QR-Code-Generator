#includy (shame)
from reedsolo import RSCodec, ReedSolomonError
from PIL import Image
import numpy as np
import os, sys

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

def AddReedSolomon(segmentCount):
    #jak narazie wszyskie segmenty to FF
    temp = []
    for i in range(segmentCount):
        temp.append("FF")
    return temp


def FitToVersionNumber(bytes,ecc): #eec- error correction code
    for version, capacity in capacities:
        if bytes < capacity-1:
            return version

def MatchEccCapacity(version):
    return eccCapacities[version-1][1]

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

def ConvertToBinary(hexSequence):
    bitSequence =[]
    for segment in hexSequence:
        bitSequence.append(bin(int(segment, 16))[2:].zfill(8))
    return bitSequence

def ConcatenateToFinal(codeWorks,ecc):
    arr = []
    for i in codeWorks:
        arr.append(i)
    for i in ecc:
        arr.append(i)
    return arr

def CalculateSize(version):
    return 17+(version*4)

def CreateQr():
    #fixed patterns
    countY = 0
    countX = 0
    for x in range(len(qr)):
        if (countX % 2 == 0):
            qr[6][x] = "1"
        else:
            qr[6][x] = "0"
        countX+=1
    for y in range(len(qr)):
        if (countY % 2 == 0):
            qr[y][6] = "1"
        else:
            qr[y][6] = "0"
        countY+=1

    #finder patterns

def PrintQrCode():
    str = ""
    for i in range(len(qr)):
        for j in range(len(qr)):
            str += qr[i][j]
        str += "\n"
    print(str)

    # robienie obrazka z biblioteką Pillow
    width = len(qr)*2

    img = Image.new('RGB', (width, width), "white")
    pixels = img.load()

    for y in range(width):
        for x in range(width):
            if qr[y][x] == "1":
                pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (0, 0, 0)
    img.save("qrcode.png")
    img.show()


# Reszta
print("-----------------------------------Super Tworzator kodu QR-----------------------------------")
# word = input("Podaj Ciąg znaków do utorzenia kodu QR\n")  "https://prisma-lab.pl/english/"
word = "https://www.freecodecamp.org/news/multi-dimensional-arrays-in-python/"

#zmienne globalne
capacities = [
        (1, 19), (2, 34), (3, 55), (4, 80), (5, 108), (6, 136), (7, 156), (8, 194), (9, 232),
        (10, 274), (11, 324), (12, 370), (13, 428), (14, 461), (15, 523), (16, 589), (17, 647),
        (18, 721), (19, 795), (20, 861), (21, 932), (22, 1006), (23, 1094), (24, 1174), (25, 1276),
        (26, 1370), (27, 1468), (28, 1531), (29, 1631), (30, 1735), (31, 1843), (32, 1955),
        (33, 2071), (34, 2191), (35, 2306), (36, 2434), (37, 2566), (38, 2702), (39, 2812), (40, 2956)
]
eccCapacities = [
    (1,7), (2,10), (3,15), (4,20), (5,26), (6,36), (7,40), (8,48), (9,60), (10,72), (11,80), (12,96),
    (13,104), (14,120), (15,132), (16,144), (17,168), (18,180), (19,196), (20,224), (21,224), (22,252),
    (23,270), (24,300), (25,312), (26,336),(27,360),(28,390),(29,420),(30,450),(31,480), (32,510),
    (33,540), (34,570), (35,570),(36,600), (37,630),(38,660), (39,720), (40,750)
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

amountOfDataCodeworks = sumBits/8

#obliczenie ilości potrzebnych segmentów reed-solomon
reedSolomonCount = MatchEccCapacity(version)

#dodanie Reed-Solomon Error Correction
ecc = AddReedSolomon(reedSolomonCount)

#ostateczna sekwencja danych do tworzenia kodu QR
finalHex = ConcatenateToFinal(hexSequence,ecc)

#przerobienie ostateczniej sekwencji hex na bin
finalArray = ConvertToBinary(finalHex)
finalString = "".join(finalArray)

#rysowanie kodu
size = CalculateSize(version)

#tworzenie pustego "szkieletu" kodu QR wypełnionego zerami
qr = np.array([ ["0"] * size] * size)

CreateQr()

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
      "\n Number of reed solomon segments : ", reedSolomonCount,
      "\nEncoded Sequence with Reed-Solomon Hex: ", finalHex,
      "\nFinal Binary Sequence for building the QR code:", finalArray,
      "\nOr :", finalString,
      "\nSize of QR code :", size,
      "\nQr : ", qr,)
PrintQrCode()
