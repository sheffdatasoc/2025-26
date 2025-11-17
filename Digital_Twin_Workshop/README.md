# 🏭 Digital Twin Workshop

Welcome to the **Digital Twin Workshop** - an interactive learning experience that demonstrates the power of digital twins in modern manufacturing and IoT systems!

## 🎯 Overview

This workshop provides a hands-on introduction to digital twin technology using a simulated manufacturing environment. You'll work with virtual machines, conveyor belts, and sorting systems that mirror real-world industrial processes.

## 🚀 Quick Start Guide

Follow these simple steps to get your digital twin environment up and running:

### Prerequisites

Before you begin, make sure you have:

- A computer running Windows, macOS, or Linux
- At least 4GB of available RAM
- An internet connection for downloading Docker images

### Step 1: Install Docker Desktop

1. **Download Docker Desktop** from the official website: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. **Install Docker Desktop** by following the installation wizard for your operating system
3. **Start Docker Desktop** and wait for it to fully initialize (the Docker icon in your system tray should show as running)

### Step 2: Navigate to the Project Folder

Open your terminal or command prompt and navigate to the Digital Twin Workshop directory:

```bash
cd Digital_Twin_Workshop
```

### Step 3: Launch the Digital Twin Environment

Run the following command to build and start all the digital twin services:

```bash
docker compose -p digitaltwin up --build -d
```

This command will:

- Build all necessary Docker images
- Start the MQTT broker for machine communication
- Launch the digital twin simulation services
- Run everything in the background (`-d` flag)

### Step 4: Access Your Digital Twin

Once the containers are running, you can:

- Monitor machine data through the MQTT broker
- View logs and system status
- Interact with the simulated manufacturing line