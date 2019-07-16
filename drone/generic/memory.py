import mmap
import struct



class Memory():

    VALID_REGS = [0, 4, 8, 16]

    @staticmethod
    def read_from_mem(base_addr, reg, file='/dev/mem', size=32):
        """Reads 32 bit value from a register in memory
        
        NOTE: This can crash the snickerdoodle if accessible memory addresses are not defined.
        This can happen if the FPGA design is not loaded.
        
        Args:
            base_addr (hex): The base address to read from
            reg (int): Which 32 bit register to read from (0: Reg0, 4: Reg1, 8: Reg2, 16: Reg3)
            file (str): Reference to mapped location where to minupilate data in
            
        Returns:
            32 bit value read from memory
        """

        if reg not in Memory.VALID_REGS:
            raise Exception('Invalid register "' + str(reg) + '"; Valid registers: ' + str(Memory.VALID_REGS))
        
        # Open dev mem for reading
        with open(file, 'r+b') as f:
            mem = mmap.mmap(f.fileno(), size, offset=base_addr)
            
            # Jump to the register
            mem.seek(reg)
            
            # Read 'l' (long - unsigned 4 byte type) from memory
            fromMem = struct.unpack('L', mem.read(4))[0] 
            
            # Close dev mem
            mem.close()
        
        return fromMem

    
    @staticmethod
    def read_bulk(base_addr, regs, file='/dev/mem'):
        """Reads 32 bit value from a register in memory
        
        NOTE: This can crash the snickerdoodle if accessible memory addresses are not defined.
        This can happen if the FPGA design is not loaded.
        
        Args:
            base_addr (hex): The base address to read from
            regs (list(int)): A list of 32 bit registers to read from (0: Reg0, 4: Reg1, 8: Reg2, 16: Reg3)
            file (str): Reference to mapped location where to minupilate data in
            
        Returns:
            32 bit values read from memory
        """

        for reg in regs:
            if reg not in Memory.VALID_REGS:
                raise Exception('Invalid register "' + str(reg) + '"; Valid registers: ' + str(Memory.VALID_REGS))
        
        vals = []

        # Open dev mem for reading
        with open(file, 'r+b') as f:
            mem = mmap.mmap(f.fileno(), 32, offset=base_addr)
            
            for reg in regs:
                # Jump to the register
                mem.seek(reg)
                
                # Read 'l' (long - unsigned 4 byte type) from memory
                vals.append(struct.unpack('L', mem.read(4))[0])
            
            # Close dev mem
            mem.close()
        
        return vals


    @staticmethod
    def write_to_mem(base_addr, reg, value, file='/dev/mem'):
        """Writes a 32 bit value to memory
        
        NOTE: This can crash the snickerdoodle if accessible memory addresses are not defined.
        This can happen if the FPGA design is not loaded.
        
        Args:
            base_addr (hex): The base address to write to
            reg (int): Which 32 bit register to write to (0: Reg0, 4: Reg1, 8: Reg2, 16: Reg3)
            value (int): Value to write into memory
            file (str): Reference to mapped location where to minupilate data in
        """

        if reg not in Memory.VALID_REGS:
            raise Exception('Invalid register "' + str(reg) + '"; Valid registers: ' + str(Memory.VALID_REGS))

        # Open dev mem for reading
        with open(file, 'r+b') as f:
            mem = mmap.mmap(f.fileno(), 32, offset=base_addr)
            
            # Jump to the register
            mem.seek(reg)
            
            # Write 'l' (long - unsigned 4 byte type) to memory
            mem.write(struct.pack('L', int(value)))
            
            # Close dev mem
            mem.close()


    @staticmethod
    def set_bit(base_addr, register, bit, value, file='/dev/mem'):
        """Sets a bit in a 32 bit register
        
        NOTE: This can crash the snickerdoodle if accessible memory addresses are not defined.
        This can happen if the FPGA design is not loaded.
        
        Args:
            base_addr (hex): The base address to write to
            reg (int): Which 32 bit register to write to (0: Reg0, 4: Reg1, 8: Reg2, 16: Reg3)
            bit (int): Which bit in the register to set
            value (bool): Whether to set the bit to 1 (True) or 0 (False)
            file (str): Reference to mapped location where to minupilate data in
        """
        if not (-1 < bit < 32):
            raise Exception('Trying to set bit outside the [0 - 31] range acceptable by the 32 bit register')

        src = Memory.read_from_mem(base_addr, register, file)

        if value: Memory.write_to_mem(base_addr, register, src | (1 << bit), file)
        else:     Memory.write_to_mem(base_addr, register, src & ~(1 << bit), file)


    @staticmethod
    def read_bit(base_addr, register, bit, file='/dev/mem'):
        """Reads a bit from a 32 bit register
        
        NOTE: This can crash the snickerdoodle if accessible memory addresses are not defined.
        This can happen if the FPGA design is not loaded.
        
        Args:
            base_addr (hex): The base address to read from
            reg (int): Which 32 bit register to read from (0: Reg0, 4: Reg1, 8: Reg2, 16: Reg3)
            bit (int): Which bit in the register to read
            file (str): Reference to mapped location where to read data from
        """
        if not (-1 < bit < 32):
            raise Exception('Trying to set bit outside the [0 - 31] range acceptable by the 32 bit register')

        src = Memory.read_from_mem(base_addr, register, file)
        return ((src & (1 << bit)) >> bit)

