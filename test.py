from drone.generic.logger import Logger
from tests.modules.test_memory import TestMemory


def run_tests():
    logger = Logger('UnitTester')
    logger.info('Starting testing...')

    try:
        TestMemory.run_tests(logger) 
    except AssertionError as e:
        logger.exception('Test failed')


if __name__ == '__main__':
    run_tests()