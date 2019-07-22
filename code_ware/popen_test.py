import os
import logging


def set_logger(log_file):

    logging.getLogger().handlers = []
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    logging.basicConfig(filename=log_file,
                        filemode='w',
                        format='%(asctime)s,%(msecs)d|%(levelname)s|%(funcName)s|%(lineno)d|%(threadName)s|%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    return logging.getLogger()

if __name__=='__main__':
	logger = set_logger('./test.log')
	file_name = f"./test"
	for i in range(-10000,10000,1):
		cmd = f'{file_name} {i}'
		res = os.popen(cmd)
		return_code = res.close()
		logger.info(f'input={i}\treturn_code={return_code}')
