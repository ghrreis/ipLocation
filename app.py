from NetTools import tracert
from NetTools import iplocation
from NetTools import maplocation
import sys

target_host = sys.argv[1]

def main():
    resultTracert = tracert(target_host)
    print(resultTracert.getListIPs())
    resultLocations = iplocation(resultTracert.getListIPs())
    print(resultLocations.getLocations())
    maplocation(resultLocations.getLocations())

if __name__ == '__main__':
    main()
