import sys
import pyperclip

def diff(init, actual):
    diffVal = actual - init
    pctVal = abs(diffVal / init) * 100
    return diffVal, pctVal

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print('Usage: \tdiff.py <oldValue> <actualValue>')
        exit(1)
    if not is_float(sys.argv[1]) or not is_float(sys.argv[2]):
        print('<oldValue> and <actualValue> must be float numbers')
        exit(1)
    string = '%.2f (%.2f%%)' % diff(float(sys.argv[1]), float(sys.argv[2]))
    string = string.replace('.', ',')
    pyperclip.copy(string)
    print(string)
