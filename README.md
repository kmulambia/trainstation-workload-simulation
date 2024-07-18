# Train Station Workload Simulator

The Train Station Workload Simulator is a Python application designed to simulate the workload at train stations based on configurable parameters. The simulation includes generating trips between stations, considering train capacities, and calculating delays due to passenger loads.

## Features

- Configurable trains, stations, platforms, and tracks
- Simulation of trips between stations
- Calculation of delays based on passenger load
- Detailed simulation report

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/train-station-workload-simulator.git
    cd train-station-workload-simulator
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Edit the `config/config.json` file to set up the trains, stations, platforms, tracks, number of people (demand), start time, and end time for the simulation.

Example `config.json`:
```json
{
    "trains": [
        {"train_id": "train1", "passenger_capacity": 200},
        {"train_id": "train2", "passenger_capacity": 150},
        {"train_id": "train3", "passenger_capacity": 180},
        {"train_id": "train4", "passenger_capacity": 220},
        {"train_id": "train5", "passenger_capacity": 170}
    ],
    "stations": [
        {"id": "station1", "platforms": [{"passenger_capacity": 100}, {"passenger_capacity": 150}]},
        {"id": "station2", "platforms": [{"passenger_capacity": 120}, {"passenger_capacity": 80}]},
        {"id": "station3", "platforms": [{"passenger_capacity": 140}]},
        {"id": "station4", "platforms": [{"passenger_capacity": 130}, {"passenger_capacity": 110}, {"passenger_capacity": 90}]},
        {"id": "station5", "platforms": [{"passenger_capacity": 200}, {"passenger_capacity": 100}]}
    ],
    "tracks": [
        {"from_station_id": "station1", "to_station_id": "station2", "direction_code": "UF", "average_section_running_time": 10},
        {"from_station_id": "station2", "to_station_id": "station3", "direction_code": "DF", "average_section_running_time": 15},
        {"from_station_id": "station3", "to_station_id": "station4", "direction_code": "US", "average_section_running_time": 20},
        {"from_station_id": "station4", "to_station_id": "station5", "direction_code": "DS", "average_section_running_time": 25},
        {"from_station_id": "station5", "to_station_id": "station1", "direction_code": "UF", "average_section_running_time": 30},
        {"from_station_id": "station1", "to_station_id": "station3", "direction_code": "UF", "average_section_running_time": 35},
        {"from_station_id": "station2", "to_station_id": "station4", "direction_code": "DS", "average_section_running_time": 40}
    ],
    "num_people_per_day": 500,
    "start_time": "09:00",
    "end_time": "12:00"
}

```

4. Running the Simulation:
    ```sh
    python -m simulate
    ```

    The simulation will generate a detailed report and store the results in an SQLite database file in the data directory.

    ```
    This setup provides a clear description of the project, installation instructions, configuration details, and running instructions for the simulator. The configuration file is updated to include `num_people_per_day`, `start_time`, and `end_time`. The script uses these parameters to control the simulation.
    ```

    