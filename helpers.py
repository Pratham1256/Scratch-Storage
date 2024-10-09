

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(),.<>?/';:][}{=-+_\|`~ "

def encode(txt):
  result = ''
  for i in range(len(txt)):
    result += "{:02}".format(chars.find(txt[i])+1)
  return result

def decode(txt):
  result = ''
  for i in range(0, len(txt), 2):
    result += chars[int(txt[i]+txt[i+1])-1]
  return result

