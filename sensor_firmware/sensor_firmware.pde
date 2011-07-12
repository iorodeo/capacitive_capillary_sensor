// ----------------------------------------------------------------------------
// sensor.pde 
//
// Firmware for arduino base capillary capacitance sensor.  Note, current 
// functionality is partial. 
//
// Author: Will Dickson
// ----------------------------------------------------------------------------
#include <Streaming.h>
#include <SoftI2cMaster.h>
#include <DictPrinter.h>
#include "AD7746.h"

// Constants
#define ERR_MSG_SIZE 30
#define SW_SCL_1 4
#define SW_SDA_1 5
#define SW_SCL_2 6
#define SW_SDA_2 7
#define NUM_CHANNEL 2
#define NUM_SENSOR 2
#define MASTER_LED_PIN 8
#define SLAVE_LED_PIN 9 
#define MASTER_SLAVE_SELECT_PIN 2      

// Function prototypes
bool initSensors(char *errMsg);
void initMasterSlave();

// Capacitance sensors 
AD7746 ad7746[NUM_SENSOR];
uint8_t sw_scl[NUM_SENSOR] = {SW_SCL_1, SW_SCL_2};
uint8_t sw_sda[NUM_SENSOR] = {SW_SDA_1, SW_SDA_2};


// Dictionary Printer for serial communications
DictPrinter dprint;

// ----------------------------------------------------------------------------
// setup
//
// Sets up serial communications, determines is master or slave, and initializes
// capacitance sensors
// 
// ----------------------------------------------------------------------------
void setup() {
    char errMsg[ERR_MSG_SIZE];

    // Initialize serial communications
    Serial.begin(9600);
    delay(1000);
    Serial << " " << endl;
    Serial << " " << endl; 
    Serial << " " << endl;

    // Determine if master or slave
    initMasterSlave();

    // Initialize capacitance sensors
    if (initSensors(errMsg) == false) {
        dprint.start();
        dprint.addStrItem("type", "init");
        dprint.addStrItem("flag", "fail");
        dprint.addStrItem("error", errMsg);
        dprint.stop();
        } else {
        dprint.start();
        dprint.addStrItem("type", "init");
        dprint.addStrItem("flag", "success");
        dprint.stop();
    }
}

// ----------------------------------------------------------------------------
// loop
//
// Program main loop
//
// ----------------------------------------------------------------------------
void loop() {
    uint8_t rtnVal;
    uint32_t data;
    uint32_t sensorNum;
    uint32_t timeMs;
    static uint32_t count[NUM_SENSOR] = {0,0};

    for (uint8_t i=0; i<NUM_SENSOR; i++) {

        rtnVal = ad7746[i].readValue(data);
        timeMs = millis();

        if (rtnVal) {
            sensorNum = ad7746[i].channel + NUM_CHANNEL*i;
            count[i]++;
            dprint.start();
            dprint.addStrItem("type", "sensor");
            dprint.addIntItem("number", sensorNum);
            dprint.addLongItem("time", timeMs);
            dprint.addLongItem("count", count[i]);
            dprint.addLongItem("value", data);
            dprint.stop();
        }
    }
}

// ----------------------------------------------------------------------------
// initSensors
//
// Initializes capacitance sensors
//
// ----------------------------------------------------------------------------
bool initSensors(char *errMsg) {
    uint8_t rtnVal;
    uint8_t status;
    uint16_t capOffset;

    for (uint8_t i=0;i<NUM_SENSOR;i++) {

        // Initialize ad7746 sensors
        ad7746[i].init(sw_scl[i], sw_sda[i]);
        rtnVal = ad7746[i].reset();
        if (rtnVal == 0) { 
            snprintf(errMsg,ERR_MSG_SIZE, "reset failed");
            return false;
        }
        delay(1000);

        // Enble exication and sensor capacitor
        rtnVal = ad7746[i].enableEXCA(AD7746_EXC_LEVEL_3);
        if (rtnVal == 0) {
            snprintf(errMsg, ERR_MSG_SIZE, "enableEXCA failed");
            return false;
        }
        rtnVal = ad7746[i].enableCap();
        if (rtnVal == 0) {
            snprintf(errMsg, ERR_MSG_SIZE, "enableCap failed");
            return false;
        }

        // Read status regiseter
        rtnVal = ad7746[i].readData(AD7746_REG_STATUS,&status,1);
        if (rtnVal == 0) {
            snprintf(errMsg, ERR_MSG_SIZE, "read status failed");
            return false;
        }

        // Autocalibration of capacitor offset
        rtnVal = ad7746[i].capOffsetCal();
        delay(1000);
        if (rtnVal == 0) {
            snprintf(errMsg, ERR_MSG_SIZE, "capOffsetCal failed");
            return false;
        }
        rtnVal = ad7746[i].readInteger(AD7746_REG_CAP_OFFSET, capOffset);
        if (rtnVal == 0) {
            snprintf(errMsg, ERR_MSG_SIZE, "read capOffset failed");
            return false;
        }

        // Enable sensor capacitor, excitation and set mode
        rtnVal = ad7746[i].enableCap();
        if (rtnVal == 0) {
            snprintf(errMsg, ERR_MSG_SIZE, "enableCap failed");
            return false;
        }

        rtnVal = ad7746[i].enableEXCA(AD7746_EXC_LEVEL_3);
        if (rtnVal == 0) {
            snprintf(errMsg, ERR_MSG_SIZE, "enableEXCA failed");
            return false;
        }

        rtnVal = ad7746[i].setModeContinuous();
        if (rtnVal == 0) {
            snprintf(errMsg, ERR_MSG_SIZE, "setModeContinuous failed");
            return false;
        }
        //rtnVal = ad7746[i].setModeSingleConversion();

    }
    return true;
}

// ----------------------------------------------------------------------------
// masterSlaveInit
//
// Determines whether board is set up as master or slave. (Currently not 
// completely implementet - just sets LEDs)
//
// ----------------------------------------------------------------------------
void initMasterSlave() {
    int ms_select;
    // Set master slave select and led pin modes
    pinMode(MASTER_LED_PIN, OUTPUT);
    pinMode(SLAVE_LED_PIN, OUTPUT);
    pinMode(MASTER_SLAVE_SELECT_PIN, INPUT);

    // Determine if master or slave
    ms_select = digitalRead(MASTER_SLAVE_SELECT_PIN);
    if (ms_select == HIGH) {
        digitalWrite(MASTER_LED_PIN, HIGH);
        digitalWrite(SLAVE_LED_PIN, LOW);
    }
    else {
        digitalWrite(MASTER_LED_PIN,LOW);
        digitalWrite(SLAVE_LED_PIN, HIGH);
    }
}
