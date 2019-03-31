import csv,logging as lg

lg.basicConfig(filename='example.log',level=lg.DEBUG)
lg.debug('This message should go to the log file')
lg.info('So should this')
lg.warning('And this, too')