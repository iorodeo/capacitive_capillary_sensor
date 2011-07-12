#ifndef AD7746_H
#define AD7746_H
#include <SoftI2cMaster.h>

//AD7746 definitions
#define AD7746_I2C_ADDRESS  0x90 
 
// Registers
#define AD7746_REG_STATUS         0x00
#define AD7746_REG_CAP_DATA       0x01
#define AD7746_REG_VT_DATA        0x04
#define AD7746_REG_CAP_SETUP      0x07
#define AD7746_REG_VT_SETUP       0x08
#define AD7746_REG_EXC_SETUP      0x09
#define AD7746_REG_CONFIGURATION  0x0A
#define AD7746_REG_CAP_DAC_A      0x0B
#define AD7746_REG_CAP_OFFSET     0x0D
#define AD7746_REG_CAP_GAIN       0x0F
#define AD7746_REG_VOLTAGE_GAIN   0x11
#define AD7746_RESET_ADDRESS      0xBF

#define AD7746_CAP_ZERO 0x800000L

// Excitation voltage levels
#define AD7746_EXC_LEVEL_0 0b00 
#define AD7746_EXC_LEVEL_1 0b01 
#define AD7746_EXC_LEVEL_2 0b10 
#define AD7746_EXC_LEVEL_3 0b11

class AD7746 : public SoftI2cMaster {
    public:

        uint8_t channel;
        uint8_t reset();
        uint8_t writeRegister(uint8_t reg, uint8_t val);

        uint8_t enableEXCA(uint8_t voltageLevel);
        uint8_t enableCap();
        uint8_t capOffsetCal();
        uint8_t setModeContinuous();
        uint8_t setModeSingleConversion();
        uint8_t setCapGain(uint16_t gain);

        uint8_t readData(uint8_t address, uint8_t *buf, uint8_t count);
        uint8_t readInteger(uint8_t address, uint16_t &value);
        uint8_t readLong(uint8_t address, uint32_t &value);
        uint8_t readValue(uint32_t &value);
        uint8_t capDataReady();

};

#endif
