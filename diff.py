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


def format(s):
    return s.replace(
        'R$ ', '').replace('.', '').replace(',', '.').replace('\n', '')


def subtract_lists(list1, list2, position):
    difference = []
    zip_object = zip(list1, list2)
    oldBalance = 0
    newBalance = 0
    for list1_i, list2_i in zip_object:
        diffVal, pctVal = diff(list1_i, list2_i)
        oldBalance += list1_i
        newBalance += list2_i
        string = '%.2f (%.2f%%)' % (diffVal, pctVal)
        index = list1.index(list1_i)
        if index in position:
            string += '\t' * position[index]
        difference.append(string.replace('.', ','))
    diffVal, pctVal = diff(oldBalance, newBalance)
    difference.append(('\t%.2f (%.2f%%)' % (diffVal, pctVal)
                       ).replace('.', ',').replace('\t', ''))
    return difference, oldBalance, newBalance


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print('Usage: \tdiff.py <file>')
        exit(1)
    try:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    except:
        print(sys.argv[1] + ' could not be found')
        exit(1)
    oldValues = []
    newValues = []
    position = {}
    for index, line in enumerate(lines):
        breakLine = line.split('\t')
        for bLine in breakLine:
            if bLine != '':
                formattedVal = format(bLine)
                if not is_float(formattedVal):
                    print('Line: %d, Value: "%s" -> is not float!' %
                          (index, bLine))
                    exit(1)
                formattedVal = float(formattedVal)
                if index == 0:
                    oldValues.append(formattedVal)
                else:
                    newValues.append(formattedVal)
            elif index == 0:
                if (len(oldValues) - 1) in position:
                    position[len(oldValues) - 1] += 1
                else:
                    position[len(oldValues) - 1] = 1
    if len(oldValues) != len(newValues):
        print('The lists have different lengths')
        exit(1)
    diffList, oldBalance, newBalance = subtract_lists(
        oldValues, newValues, position)
    pyperclip.copy('\t'.join(diffList))
    print('Result copied to clipboard')
    print('This month your balance was: R$ ' +
          diffList[len(diffList) - 1])
    print('Old balance: R$ ' + ('%.2f' % oldBalance).replace('.', ','))
    print('New balance: R$ ' + ('%.2f' % newBalance).replace('.', ','))
