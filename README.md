# Pinheirinho - Assetto Corsa Drag Race Mod

**Professional Drag Race Logic System for Assetto Corsa**

Pinheirinho is a Python-based mod for Assetto Corsa that implements a realistic, rigorous Drag Racing system. It is designed to replace simple visual scripts with a robust engineering solution capable of managing strict competition rules found in real-world drag strips.

## 🚀 Features

### Realistic Staging Logic
- **Precision Sensors**: Uses vector math to detect the exact position of the vehicle's front wheels relative to the track's laser-scanned beams.
- **Strict Staging**: Requires both "Pre-Stage" and "Stage" beams to be active for a valid "Ready" state.
- **Deep Stage Support**: Handles professional "Deep Staging" (rolling past the first beam) with configurable rules.

### Competition Rules
- **The "7-Second Rule"**: Automatically enforces a timeout. Once the first driver is fully staged, the opponent has 7 seconds to stage, or they are disqualified (Red Light).
- **Double Fault Independence**: The system tracks each lane independently. A fault (red light) in the left lane does not interrupt the sequence for the right lane.
- **Sportsman Tree**: Implements the standard 0.5s cascading amber light sequence (1.5s total duration).

### Performance Optimization
- **Zero Disk I/O**: Unlike legacy scripts that write to `.ini` files to change lights (causing lag), Pinheirinho uses the **Custom Shaders Patch (CSP)** API to manipulate material emissives directly in GPU memory.
- **Event-Driven Architecture**: Built on a Finite State Machine (FSM) to ensure bug-free state transitions (e.g., you can't get a Green Light if you haven't Staged).

## 🛡️ Audit & "Black Box Recorder"

In competitive environments (e-sports or betting), traceability is more important than visual functionality. If there is a dispute about who jumped the start, the system must provide a mathematical proof, not just "I saw a red light".

To ensure **Auditability, Security, and Transparency** without compromising performance (solving the Disk I/O issue), we implement the **"Black Box Recorder"** pattern:

### Engineering Strategy
1.  **In-Memory Buffer (Zero Latency)**: During the race, nothing is written to disk. Every event (sensor activation, light change, driver input) is appended to a list in RAM. This guarantees the game does not stutter (lag) at the critical moment.
2.  **Asynchronous Dump**: The buffer is flushed to a JSON/Log file only when the race ends (transiting to FINISHED or IDLE state).
3.  **Digital Signature (Hash)**: To ensure the driver hasn't edited the log file to claim they "didn't jump", we generate an MD5/SHA Hash of the race content. If a single comma in the .json file is altered after the race, the Hash will mismatch.

## 🛠️ Technology Stack
*   **Language**: Python 3.3 (Embedded)
*   **Platform**: Assetto Corsa
*   **Key APIs**: `ac`, `acsys`, `ac_ext` (CSP)
*   **Architecture**: Component-Based with Finite State Machine

## 📂 Project Structure
```
apps/python/pinheirinho/
├── config/             # JSON database for Track/Sensor coordinates
├── src/
│   ├── core/           # RaceManager (FSM) & Event System
│   ├── domain/         # Rules & Lane Logic
│   └── infrastructure/ # CSP Lighting & AC Adapters
└── pinheirinho.py      # Main Entry Point
```

## 🔧 Installation
1.  Copy the `apps/python/pinheirinho` folder to your Assetto Corsa installation directory: `.../steamapps/common/assettocorsa/apps/python/`.
2.  Enable "Pinheirinho" in Assetto Corsa Settings > Python Apps.
3.  In-game, open the side app bar and select "Pinheirinho".

## 🤝 Contributing
This project is structured to be developer-friendly. Logic (Domain) is separated from the Game Engine (Infrastructure).
To run tests locally without the game, use the provided `tests/mock_ac.py` environment.
