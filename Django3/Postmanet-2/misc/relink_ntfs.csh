#!/bin/csh -f
#    usage: relink_ntfs.csh linux_dir ntfs_dir backup_dir
#    such as: relink_ntfs.csh /u/Postmanet /u/rywang/tmp/Postmanet baks2
#    run as root
#


#
# get the arguments straight.
#
if ($#argv != 3) then
    echo "usage: $0 linux_dir ntfs_dir backup_dir"
    exit (-1)
endif

set linux_dir = $1
echo 'linux directory is: '$linux_dir

set ntfs_dir = $2
echo 'ntfs directory is: '$ntfs_dir

set backup_dir = $3
echo 'backup directory is: '$backup_dir


cd $linux_dir
cd repository


#
# saving the originals.
#
echo "moving away originals..."

mkdir $backup_dir

if (-e SearchFile) then
    mv SearchFile $backup_dir/
endif

if (-e ReverseLists) then
    mv ReverseLists $backup_dir/
endif

if (-e WWW/ObjectStore) then
    mv WWW/ObjectStore $backup_dir/
endif

if (-e View) then
    mv View $backup_dir/
endif


#
# copy or link the new...
# 
echo "linking new..."

set from_dir = $ntfs_dir/repository
#cp $from_dir/Searchfile SearchFile
cp $from_dir/SearchFile SearchFile
cp $from_dir/ReverseLists ReverseLists
rm -f View
ln -s $from_dir/View .
cd WWW
rm -f ObjectStore
ln -s $from_dir/WWW/ObjectStore .
cd ..


#
# deal with permissions...
#
echo "setting permissions..."
chown www-data SearchFile ReverseLists
