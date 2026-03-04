# Buenos Aires Metro Route Planner (SUBTE)

## Overview
This project implements a route planning application for the Buenos Aires metro system (Subte).  
The system computes the optimal route between two stations using the A* search algorithm and provides an interactive graphical interface for users.

## Features
- Optimal route calculation using the A* algorithm
- Travel time estimation between stations
- Consideration of:
  - train frequencies
  - operating schedules
  - transfers between lines
- Graphical user interface for selecting origin, destination, date and time
- Visualization of the route and transfers

## Methodology

### Graph Representation
The metro network is modeled as a graph where:
- nodes represent stations
- edges represent connections between stations

The graph was implemented using the **NetworkX** library.

### Heuristic Function
The heuristic used in the A* algorithm estimates the travel time between two stations using the **Haversine formula**, which calculates geographic distance based on latitude and longitude coordinates.

### Travel Time Calculation
The total travel time considers:
- waiting time at stations
- train frequency
- transfer times
- travel time between stations

### User Interface
The graphical interface was developed using **Tkinter** and allows users to:
- select origin and destination stations
- select travel date and time
- visualize the optimal route
- view travel time and transfers

## Technologies Used
- Python
- NetworkX
- Pandas
- NumPy
- Tkinter
- Matplotlib

## Data Sources
- Buenos Aires metro station data
- Train schedules and frequencies
- Geographic coordinates of stations

## Future Improvements
- Real-time metro data integration
- More advanced heuristics
- Improved UI and visualization

## Academic Context
This project was developed as part of the **Data Science and Artificial Intelligence degree**.

## Documentation
Full project report available in `Memoria.pdf`.
