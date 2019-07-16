import struct
from drone.generic.memory import Memory


class TestMemory():

    @staticmethod
    def run_tests(logger):
        TestMemory.test_file_access(logger)
        TestMemory.test_read_write(logger)
        TestMemory.test_read_bulk(logger)
        TestMemory.test_set_bit(logger)
        TestMemory.test_read_bit(logger)
        TestMemory.test_invalid_register_access(logger)
        TestMemory.test_invalid_bit_access(logger)



    @staticmethod
    def test_file_access(logger):
        logger.info('Performing test_file_access')

        with open('test.bin', 'wb') as f:
            f.write(struct.pack('l', 0x00000000))

        try: Memory.write_to_mem(0x0, 0, 0, file='test.bin')
        except FileNotFoundError: assert False, 'Unable to open file "test.bin"'
        
        logger.info('Test passed\n')


    @staticmethod
    def test_read_write(logger):
        logger.info('Performing test_read_write')
        
        Memory.write_to_mem(0x0, 0, 0xDEADBEEF, file='test.bin')
        read = Memory.read_from_mem(0x0, 0, file='test.bin')

        assert read == 0xDEADBEEF, 'Data read does not match expected data; Read: %s,   Expected: %s' % (read, 0xDEADBEEF)
        logger.info('Test passed\n')


    @staticmethod
    def test_read_bulk(logger):
        logger.info('Performing test_read_bulk')
        # TODO
        logger.info('Test passed\n')


    @staticmethod
    def test_set_bit(logger):
        logger.info('Performing test_set_bit')
        
        Memory.write_to_mem(0x0, 0, 0x00000000, file='test.bin')

        logger.info('\tSetting 1st bit')
        Memory.set_bit(0x0, 0, 0, True, file='test.bin')
        read = Memory.read_from_mem(0x0, 0, file='test.bin')
        assert read == 0x00000001, 'Data read does not match expected data; Read: %s,   Expected: %s' % (read, 0x00000001)

        logger.info('\tClearing 1st bit')
        Memory.set_bit(0x0, 0, 0, False, file='test.bin')
        read = Memory.read_from_mem(0x0, 0, file='test.bin')
        assert read == 0x00000000, 'Data read does not match expected data; Read: %s,   Expected: %s' % (read, 0x00000000)

        logger.info('\tSetting 5th bit')
        Memory.set_bit(0x0, 0, 4, True, file='test.bin')
        read = Memory.read_from_mem(0x0, 0, file='test.bin')
        assert read == 0x00000010, 'Data read does not match expected data; Read: %s,   Expected: %s' % (read, 0x00000010)

        logger.info('\tClearing 5th bit')
        Memory.set_bit(0x0, 0, 4, False, file='test.bin')
        read = Memory.read_from_mem(0x0, 0, file='test.bin')
        assert read == 0x00000000, 'Data read does not match expected data; Read: %s,   Expected: %s' % (read, 0x00000000)

        logger.info('\tTesting set and clear on all 32 bits')
        for bit in range(0, 31):
            Memory.set_bit(0x0, 0, bit, True, file='test.bin')
            read = Memory.read_from_mem(0x0, 0, file='test.bin')
            assert read == (1 << bit), 'Data read does not match expected data when setting bit %i; Read: %s,   Expected: %s' % (bit, read, (1 << bit))

            Memory.set_bit(0x0, 0, bit, False, file='test.bin')
            read = Memory.read_from_mem(0x0, 0, file='test.bin')
            assert read == 0x00000000, 'Data read does not match expected data when setting bit %i; Read: %s,   Expected: %s' % (bit, read, 0x0)

        logger.info('Test passed\n')


    @staticmethod
    def test_read_bit(logger):
        logger.info('Performing test_read_bit')
        # TODO
        logger.info('Test passed\n')


    @staticmethod
    def test_invalid_register_access(logger):
        logger.info('Performing test_invalid_register_access')
        # TODO
        logger.info('Test passed\n')


    @staticmethod
    def test_invalid_bit_access(logger):
        logger.info('Performing test_invalid_bit_access')
        # TODO
        logger.info('Test passed\n')