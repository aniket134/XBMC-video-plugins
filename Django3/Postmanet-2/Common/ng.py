

import os, win32file
import ryw

def usedSpace_MB(path):
    """returns the amount of used space in MB."""
    path = os.path.normpath(path)
    try:
        sectorsPerCluster,bytesPerSector,numFreeClusters,totalNumClusters = \
            win32file.GetDiskFreeSpace(path)
    except:
        give_bad_news(
            'fatal_error: failed to determine free disk space: '+path,
            logging.critical)
        return 0
    
    sectorsPerCluster = long(sectorsPerCluster)
    bytesPerSector = long(bytesPerSector)
    numFreeClusters = long(numFreeClusters)
    totalNumClusters = long(totalNumClusters)
    usedMB = ((totalNumClusters - numFreeClusters) * sectorsPerCluster * bytesPerSector) / \
             (1024 * 1024)
    return usedMB

