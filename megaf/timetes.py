import time

tes = time.strptime('11/11/2014', '%d/%m/%Y')
print(time.strftime('%Y-%m-%d', tes))

cod = '{one} {two} {three} {four}'
print(cod.format(one="asd", two="sad", three='asd', four='qwe'))

ssd = []

if not ssd:
    print("NONONONO")

def thaitoarab(num):
    ll = ''
    for i in num:
        if i == '๐':
            ll += '0'
        elif i == '๑':
            ll += '1'
        elif i == '๒':
            ll += '2'
        elif i == '๓':
            ll += '3'
        elif i == '๔':
            ll += '4'
        elif i == '๕':
            ll += '5'
        elif i == '๖':
            ll += '6'
        elif i == '๗':
            ll += '7'
        elif i == '๘':
            ll += '8'
        elif i == '๙':
            ll += '9'
        else:
            ll += '/'


    print(ll)
    return ll

print(thaitoarab('๑๑/๑๑/๒๐๑๔'))



