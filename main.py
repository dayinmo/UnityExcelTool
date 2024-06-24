import logging

from Excel2Unity import Excel2Unity
from Excel2Json import Excel2Json
def main():
    Excel2Unity().Process()
    Excel2Json().Process()

if __name__ == '__main__':
    main()