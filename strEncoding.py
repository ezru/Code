string = 'pythön!'
print(f'The string is: {string}')

string_utf = string.encode()
print(f'The encoded string is: {string_utf}')

try:
    print(f'The encoded version (with ignore) is: {string.encode("ascii", "replace")}')
except:
    print(UnicodeEncodeError)