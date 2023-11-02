/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "DS1820.h"
#include "rtos.h"    
#include "SerialStream.h"        
#include <string.h>


BufferedSerial serial(USBTX, USBRX, 57600);
SerialStream<BufferedSerial> pc(serial);
// Max number of tasks 
#define MAX_TASKS 5
#define THERMOMETER_PIN p5
#define ACCEPTABLE_TEMPERATURE_DIFF 1

typedef struct heat_task {
    int targetTemp;
    int timeLeftSec;
    time_t lastUpdateTime;
} heat_task;

typedef struct heat_schedule {
    heat_task taskArr[MAX_TASKS];
    int currTaskIndex;
    int numTasks;
} heat_schedule;

heat_schedule* sched;
time_t now;
DS1820 thermometer(THERMOMETER_PIN);

Thread update_thread;
EventQueue update_queue;

void createDummySchedule() {
    sched = (heat_schedule*) malloc(sizeof(heat_schedule));
    sched->currTaskIndex = 0;
    sched->numTasks = 1;
    for(int i = 0; i < 2; i++) {
        heat_task*  currTask = &sched->taskArr[i];
        if(i == 0) {
            currTask->targetTemp = 76;
            currTask->timeLeftSec = 30;
        } else {
            currTask->targetTemp = 80;
            currTask->timeLeftSec = 15;
        }
        time(&now);
        currTask->lastUpdateTime = now;
    }
}

void increaseTemp() {
    //temp function
    pc.printf("Need to Increase Temp\n");
}

void decreaseTemp() {
    //temp function
    pc.printf("Need to Decrease Temp\n");
}

float getTemp() {
    thermometer.convertTemperature(true, DS1820::all_devices);         //Start temperature conversion, wait until ready
    return thermometer.temperature('f');
}

void updateSchedule(){
    if(sched->currTaskIndex >= sched->numTasks) {
        pc.printf("Out of Tasks\n");
        return;
    }
    heat_task* currTask = &sched->taskArr[sched->currTaskIndex];
    float currTemp = getTemp();
    pc.printf("Curr Temp: %f  Target Temp Range: (%d, %d)  Time Remaining: %d\r\n", 
        currTemp, currTask->targetTemp - ACCEPTABLE_TEMPERATURE_DIFF, currTask->targetTemp + ACCEPTABLE_TEMPERATURE_DIFF, currTask->timeLeftSec);

    if(currTemp > currTask->targetTemp + ACCEPTABLE_TEMPERATURE_DIFF) {
        decreaseTemp();
        time(&now);
        currTask->timeLeftSec = currTask->timeLeftSec - (now-currTask->lastUpdateTime);
    } else if(currTemp < currTask->targetTemp - ACCEPTABLE_TEMPERATURE_DIFF) {
        increaseTemp();
    } else {
        time(&now);
        currTask->timeLeftSec = currTask->timeLeftSec - (now-currTask->lastUpdateTime);
    }

    if(currTask->timeLeftSec <= 0) {
        pc.printf("Finished Current Task");
        sched->currTaskIndex += 1;
    }
    
    time(&now);
    currTask->lastUpdateTime = now;
}

int main()
{
    pc.printf("Starting temperature\n");
    pc.printf("Sizeof schedule: %d Sizeof task: %d\n", sizeof(heat_schedule), sizeof(heat_task));
    //update_thread.start(callback(&update_queue,&EventQueue::dispatch_forever));
    //update_queue.call_every(2000ms,&updateSchedule);
    createDummySchedule();
    while(1) {
        updateSchedule();
        ThisThread::sleep_for(chrono::seconds(1));
    }
    /**
        pc.printf("It is %f\r\n", getTemp());
        //pc.printf("bruh\n");
        ThisThread::sleep_for(chrono::seconds(1));
    **/
}
