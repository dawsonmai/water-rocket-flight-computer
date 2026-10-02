# Water Rocket Flight Computer
CircuitPython-based autonomous flight computer. The system uses onboard pressure and orientation sensors to determine the rocket's flight stage and autonomously deploy its parachute recovery system.

## Background
The flight computer was built as part of a water rocket project. Rather than relying on a fixed timer, the goal was to create an onboard system capable of determining flight stage using real-time sensor data and deploying the parachute when necessary.

The flight computer was designed around a servo-actuated parachute mechanism and tested through full water rocket launches.

## Features
- Autonomous flight stage detection
- Barometric altitude measurement
- IMU-based pitch and yaw monitoring
- Apogee detection using maximum recorded altitude
- Servo-controlled parachute deployment system
- LED flight-status indicators

## Hardware
The flight computer is built around a CircuitPython compatible **Adafruit Metro M4 Express microcontroller** and processes data from:
- **BNO055** - orientation and gravity sensor
- **BMP390** - barometric pressure sensor and altimeter

Based on these measurements, the flight computer controls:
- **Servo motor** - releases the parachute recovery system
- **Status LEDs** - indicates current flight phase

The BNO055 and BMP390 communicate with the microcontroller over **I<sup>2</sup>C**.

## Software
The flight software is written in **CircuitPython** and organized as a simple state machine with four flight stages.

### Phase 0: Initialization
Sensors and recovery servo are initialized and calibrated, recording:

- Ground altitude
- Initial pitch angle
- Initial yaw angle

After initialization, the LED indicator turns **green** and the system transitions into launch-ready state.

### Phase 1: Launch Ready
Altitude and vehicle orientation are constantly monitored while waiting for launch.

Launch is detected when the measured altitude exceeds the initial ground altitude by more than **2 meters**. Once detected, the system transitions to the ascent phase.

Pitch and yaw are also monitored as a pre-launch/flight failsafe. A deviation greater than **30°** from the initial orientation triggers the recovery sequence.

### Phase 2: Ascent
The computer continously:

- Measures barometric altitude
- Tracks maximum altitude reached
- Calculates pitch and yaw from IMU gravity measurements
- Monitors vehicle for abnormal orientations

Apogee is detected when the current altitude falls more than **2 meters** below the maximum recorded altitude.

Apogee detection or a pitch/yaw deviation greater than **30°** causes the system to transition to the descent phase.

### Phase 3: Descent/Recovery
The computer:

1. Changes LED indicator to **red** to indicate descent
2. Rotates recovery servo for parachute deployment
3. Holds recovery servo position for two seconds to ensure parachute is fully deployed
4. Returns servo to its original position for reuse

The flight program then terminates.

## Potential Improvements
1. **Altitude filtering** - Apply a moving average or other filtering method to barometric altitude measurements to prevent premature stage transitions due to sensor noise.
2. **Configurable flight parameters** - Replace hard-coded altitude, attitude, and timing thresholds with named configuration constants.
3. **Data recording** - Record altitude, velocity, and other data for post-flight analysis and improvements.