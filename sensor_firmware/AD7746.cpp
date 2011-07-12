#include "WProgram.h"
#include "Streaming.h"
#include "AD7746.h"

uint8_t AD7746::reset() {
    if (!start(AD7746_I2C_ADDRESS|I2C_WRITE)) return false;
    if (!write(AD7746_RESET_ADDRESS)) return false;
    stop();
    return true; 
}

uint8_t AD7746::writeRegister(uint8_t reg, uint8_t val) {
    if (!start(AD7746_I2C_ADDRESS|I2C_WRITE)) return false;
    if (!write(reg)) return false;
    if (!write(val)) return false;
    stop();
    return true;
}

uint8_t AD7746::enableEXCA(uint8_t voltageLevel) {
    return writeRegister(AD7746_REG_EXC_SETUP, _BV(3) | voltageLevel);
}

uint8_t AD7746::enableCap() {
    channel = 0;
    return writeRegister(AD7746_REG_CAP_SETUP, _BV(7));
}

uint8_t AD7746::capOffsetCal() {
    uint8_t value;
    // set configuration to calib. mode, slow sample
    value =  _BV(7) | _BV(6) | _BV(5) | _BV(4) | _BV(3) | _BV(2) | _BV(0);  
    if (!writeRegister(AD7746_REG_CONFIGURATION,value)) return false;
    return true;
}

uint8_t AD7746::setModeContinuous() {
    uint8_t value;
    value = _BV(7) | _BV(6) | _BV(5) | _BV(4) | _BV(3) | _BV(0); 
    if (!writeRegister(AD7746_REG_CONFIGURATION,value)) return false;
    return true;
}

uint8_t AD7746::setModeSingleConversion() {
    uint8_t value;
    value = _BV(7) | _BV(6) | _BV(5) | _BV(4) | _BV(3) | _BV(1); 
    if (!writeRegister(AD7746_REG_CONFIGURATION,value)) return false;
    return true;
}

uint8_t AD7746::setCapGain(uint16_t gain) {
    uint8_t byte;
    if (!start(AD7746_I2C_ADDRESS|I2C_WRITE)) return false;
    if (!write(AD7746_REG_CAP_GAIN)) return false;
    byte = (uint8_t) (gain >> 8);
    if (!write(byte)) return false;
    byte = (uint8_t) (gain & 0xFF); if (!write(byte)) return false;
    stop();
    return true;
}

uint8_t AD7746::readData(uint8_t address, uint8_t *buf, uint8_t count) {
    // issue a start condition, send device address and write direction bit
    if (!start(AD7746_I2C_ADDRESS|I2C_WRITE)) return false;

    // send the DS1307 address  
    if (!write(address)) return false;

    // issue a repeated start condition, send device address and read direction bit  
    if (!restart(AD7746_I2C_ADDRESS|I2C_READ)) return false;

    // read data 
    for (uint8_t i = 0; i < count; i++) {
        // send Ack until last byte then send Ack
        buf[i] = read(i == (count-1));
    }
    // issue a stop condition  
    stop();
    return true;
}

uint8_t AD7746::readInteger(uint8_t address, uint16_t &value) {
    uint8_t buf[2];
    if (!readData(address, buf, 2)) return false;
    value = ((uint16_t) buf[0]) << 8;
    value |= (uint16_t) buf[1];
    return true;
}

uint8_t AD7746::readLong(uint8_t address,  uint32_t &value) {
    uint8_t buf[3];
    if (!readData(address, buf, 3)) return false;
    value = 0;
    value |= ((uint32_t) buf[0]) << 16;
    value |= ((uint32_t) buf[1]) << 8;
    value |= (uint32_t) buf[2];
    return true;
}

uint8_t AD7746::readValue(uint32_t &value) {
    uint8_t status = 0;

    //while (!(status &  _BV(2))) {
    //    readData(AD7746_REG_STATUS, &status, 1);
    //    Serial << "status: " << _BIN(status) << endl;
    //}
    if (capDataReady() == false) {
        return false;
    }
    return readLong(AD7746_REG_CAP_DATA,value);
}

uint8_t AD7746::capDataReady() {
    uint8_t status;
    readData(AD7746_REG_STATUS, &status, 1);
    if (!(status & _BV(2))) {
        return true;
    }
    else {
        return false;
    }
}

