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
stupidMagicArray={0x00A50800:[0x47048945, 0xE831F68B, 0x450C8907, 0xC7442404],
                  0x00A50804:[0x4a202520, 0x2064736f, 0x000a0000, 0x6425252c],
                  0x00A51400:[0x07018B10, 0x83C20189, 0x1089D10F, 0xB7C20FB7],
                  0x00A51409:[0x070581e8, 0xff7411e3, 0x8373b619, 0xa1ef5492],
                  0x00A52000:[0x07018888, 0x83222289, 0x1414d10f, 0xb7c207b7],
                  0x00A52004:[0xc7bc80da, 0xea320881, 0x18a21be1, 0x484e3b0c]}

if (len(sys.argv)>1):
  fileInputName=sys.argv[1]
  print(fileInputName)
  fileInput=open(fileInputName, 'rb')
  fileBytes=bytearray(fileInput.read())
  fileInput.close()
  fileBytes=fileBytes+bytearray(4096-len(fileBytes)%4096) #File size seems to be required to be of n*8kB long
  writeAsWord(0xFFFFFFFF, fileBytes, 0x404)     #Can be anything, but for md5 must be this 
  writeAsWord(0x4E415742, fileBytes, 0x408)     #Unknown but has to be this or will trigger an corrupted firmware triger
  writeAsWord(0x00000000, fileBytes, 0x410)     #Can be anything, but for md5 must be this
  writeAsWord(len(fileBytes), fileBytes, 0x40C) #Set file size
  writeAsWord(0x00000001, fileBytes, 0x418)     #Set revision
  
  magicArray=[]
  try: 
    magicArray=stupidMagicArray[readAsWord(fileBytes, 0x414)]
  except:
    print("Unknown Product code")
    print(hex(readAsWord(fileBytes, 0x414)))
    try:
      print("Attempting Product family")
      familyCode=readAsWord(fileBytes, 0x414)&0xFFFFFF00
      print(hex(familyCode))
      magicArray=stupidMagicArray[familyCode]
      print("Forcing usage of family code, this may or may not work")
      writeAsWord(familyCode, fileBytes, 0x414)
    except:
      print("Unknown Family code")
      exit()

#  MD5inFile=fileBytes[0xFF0:0x1000]
  MD5ofFile=hashlib.md5(fileBytes[:0xFF0]+fileBytes[0x1000:]).digest()

  for i in range(4):
    writeAsWord(magicArray[i]^readAsWord(MD5ofFile, i*4), fileBytes, 0xFF0+i*4)
  fileOut=open(fileInputName[:-4]+"-fixed-header.bin", 'wb')
  fileOut.write(fileBytes)
  fileOut.close()

else :
  print("Please give the file as an argument")
