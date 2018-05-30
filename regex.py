import re
import sys
import argparse

def _argparse():
    parser = argparse.ArgumentParser(description='A Python-check regrex script!')
    parser.add_argument('-u', '--url', action='store', dest='url', required=True, help='check url')
    parser.add_argument('-r', '--regrex', action='store', dest='regrex', required=True, help='regular expression')
    parser.add_argument(dest='position',metavar='position', help='Parameter position: url 1 2 3', nargs='*')
    return parser.parse_args()


def _regrex(url, regrex, kargs):
    n= len(kargs)
    try:
        rr = re.compile(r'%s' %regrex)
#        rr = re.compile(r'(150.)(138.238.)(2[3-9]$|3[0-8]$|4[0-7]$)')
        m = rr.search(url)
        if m:
            for i in kargs:
                res_list.append(m.group(int(i)))   
            print('=' * 70)
            reslut = ''.join(res_list)
            print('searched,reslut: {}'.format(reslut))
        else:
            print('not searched')
    except IndexError as ERROR_IndexError:
        print('ERROR_IndexError:{}'.format(i))



res_list = []
parser = _argparse()
_regrex(parser.url, parser.regrex, parser.position)

