# traffic-optimization

## Description
This project addresses an **optimization problem of traffic circulation** within a region composed of several cities and towns.  
**Version 1** represents the initial and simplified model, which will serve as the foundation for more realistic future extensions.

## Main Features
1. **Node generation (cities):**
   - Each city is represented as a **node** in a graph.
   - Each node is assigned a **weight proportional to its population**, generated randomly within a predefined range.
   
2. **City connections:**
   - **Random links** are established between cities with a given probability.
   - Each connection has a **weight representing the distance**, assigned randomly.
   - The resulting graph is **not fully connected**: the number of links is limited to avoid a complete network of all cities.

3. **Population movements:**
   - The population of each city moves **randomly** to other cities.
   - No transportation capacity limit is set in this version.
   - The goal is to **simulate basic displacements** and obtain data on the number of movements and travel times.

4. **Optimization (not yet implemented in this version):**
   - In this first version, the focus is on building the network and simulating basic movement.
   - Improvements such as capacity limits, travel routines, accidents, and optimal speed will be added in later versions.

## Visual Representation
- Each city is shown as a **node** whose size reflects its population.
- Connections between nodes are **edges with weights** that represent distances in kilometers.
- Example visualization:

## Next Steps (future versions)
- Implement more realistic rules for distributing population across large, medium, and small cities.
- Add transportation capacity limits for segments.
- Introduce movement routines (daily work travel, holidays, etc.).
- Accidents and risks associated with speed.
- Differentiate between public and private transportation.
- Implement evolutionary algorithm to optimize the network of connections.

