#! /usr/bin/env python

import logging


def initlog(verbose=3, cfg_file=None):

    if cfg_file == None:

        datefmt = '%y/%m/%d %H:%M:%S'
        log_file = 'output.log'

    # l = logging.getLevelName('rtlog')
    logging.basicConfig(format='%(asctime)s.%(msecs)d %(funcName)s %(levelname)s '
                         '%(message)s', filename=log_file,
                  level=logging.DEBUG, datefmt=datefmt)
    logging.info('= = = = = = = = = =   started   = = = = = = = = = = ')


