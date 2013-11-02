import hashlib
import sys
def readAsWord(array, ofset=0):
  out=0
  for i in range(4):
    out=out<<8
    out+=array[ofset+i]
  return(out)
def writeAsWord(number, array, ofset):
  for i in range(4):
    tmp=number&0xFF
    array[(ofset+3-i)]=tmp
    number = number>>8
stupidMagicArray=[0x70581e8, 0xff7411e3, 0x8373b619, 0xa1ef5492]

if (len(sys.argv)>1):
  fileInputName=sys.argv[1]
  print(fileInputName)
  fileInput=open(fileInputName, 'rb')
  fileBytes=bytearray(fileInput.read())
  fileInput.close()
  fileBytes=fileBytes+bytearray(len(fileBytes)%4096) #File size seems to be required to be of n*8kB long
  writeAsWord(0xFFFFFFFF, fileBytes, 0x404)     #Can be anything, but for md5 must be this 
  writeAsWord(0x4E415742, fileBytes, 0x408)     #Unknown but has to be this or will trigger an corrupted firmware triger
  writeAsWord(0x00000000, fileBytes, 0x410)     #Can be anything, but for md5 must be this
  writeAsWord(len(fileBytes), fileBytes, 0x40C) #Set file size
  writeAsWord(0x00A51409, fileBytes, 0x414)     #Set product code
  writeAsWord(0x00000001, fileBytes, 0x418)     #Set revision


#  MD5inFile=fileBytes[0xFF0:0x1000]
  MD5ofFile=hashlib.md5(fileBytes[:0xFF0]+fileBytes[0x1000:]).digest()

  for i in range(4):
    writeAsWord(stupidMagicArray[i]^readAsWord(MD5ofFile, i*4), fileBytes, 0xFF0+i*4)
  fileOut=open(fileInputName[:-4]+"cool.bin", 'wb')
  fileOut.write(fileBytes)
  fileOut.close()

else :
  print("Please give the file as an argument")
