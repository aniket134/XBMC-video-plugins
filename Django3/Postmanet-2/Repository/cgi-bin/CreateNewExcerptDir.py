import sys, os
import su
import pickle
import logging
import cgi
import ryw, SearchFile, ryw_meta, ryw_view
import objectstore
import CreateNewThumbDir


def main():

    #
    # initialization businesses.
    #
    success,objID,version = CreateNewThumbDir.init(
        'CreateNewExcerptDir: entered...',
        '<FONT SIZE=4>Creating new excerpt directory...</FONT><P>')
    if not success:
        sys.exit(1)

    #
    # get all the paths.
    #
    success,auxiURL,auxiDir = CreateNewThumbDir.get_paths(objID, version)
    if not success:
        sys.exit(1)

    #
    # create thumbnail directory.
    #
    success = CreateNewThumbDir.create_auxi_dir(
        auxiDir, 'excerpts',
        'Excerpt directory created: ',
        'Excerpt directory exists: ',
        'Add arbitrary excerpt files into the directory.')
    if not success:
        sys.exit(1)
                    

    #
    # create explorer strings.
    # 
    CreateNewThumbDir.print_explorer_string(auxiURL,
                                            'excerpts',
                                            'excerpt directory')
    
    sys.exit(0)



if __name__ == '__main__':
    main()


