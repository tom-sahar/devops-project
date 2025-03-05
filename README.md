# **DevOps Project**

## **Overview**
This project showcases a **load-balanced** architecture using **NGINX as a reverse proxy** with **sticky session handling**. The backend consists of **Flask applications running in Docker containers**, with a **MySQL database** for logging requests and maintaining state.

## **Tech Stack**
- **NGINX** – Load balancing with sticky session handling
- **Flask** – Lightweight Python-based backend framework
- **Docker & Docker Compose** – Containerization and orchestration
- **MySQL** – Database for request logging and counter tracking

## **Project Features**
### **1. Load Balancing with Sticky Sessions**
- NGINX is configured as a reverse proxy to distribute traffic across multiple Flask instances.
- Sticky session handling ensures that a user remains connected to the same backend server for a predefined duration.

### **2. Session Persistence Using Cookies**
- Each user is assigned a unique `srv_id` cookie, identifying the backend server handling their session.
- Deleting the cookie results in reassignment to a new backend instance.

### **3. Automatic Counter Increment**
- A global counter stored in **MySQL** is incremented on each page refresh.
- The counter value is shared across all backend instances to maintain consistency.

### **4. Database Logging**
- All requests are logged into the database, capturing:
  - Timestamp
  - Client IP address
  - Assigned backend server (`srv_id`)

## **Project Setup & Deployment**
### **Prerequisites**
Ensure the following are installed on your system:
- Docker
- Docker Compose

### **Installation**
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd devops-project
   ```

2. **Start the services:**
   ```bash
   docker-compose up --build -d
   ```

3. **Access the application:**
   - Open a browser and go to: `http://localhost`

### **Testing Sticky Sessions**
1. Open Developer Tools (`F12`) and navigate to **Storage → Cookies**.
2. Find the `srv_id` cookie.
3. Refresh the page multiple times and ensure the **same server ID remains assigned**.
4. Delete the cookie and refresh – the server ID should change.
5. Repeat the process to confirm that **all servers are being utilized over time**.

## **Configuration Details**
### **NGINX Configuration (`nginx.conf`)**
- Reverse proxy with **sticky session handling** using cookies.
- Ensures session persistence for **5 minutes**.
- Automatically assigns a `srv_id` cookie if missing.

### **Flask Application (`app.py`)**
- Reads the `srv_id` cookie from incoming requests.
- If the cookie is missing, it is assigned based on the backend server’s IP.
- Updates and retrieves the global page counter from the **MySQL database**.

### **MySQL Database**
- Stores request logs (`access_log` table).
- Maintains a persistent global counter (`global_counter` table).

## **Scaling the Application**
To increase the number of backend instances, modify `docker-compose.yml`:
```yaml
  app:
    deploy:
      replicas: 10  # Adjust this number as needed
```
Then restart the services:
```bash
docker-compose down
docker-compose up --build -d
```

## **Potential Enhancements**
- Implement **health checks** to monitor backend instance availability.
- Integrate **monitoring and alerting** using Prometheus and Grafana.
- Optimize **NGINX load balancing settings** for improved performance.

**Tom Sahar**  
Contact: **Tom.sahar10@gmail.com**  
LinkedIn: [Tom Sahar](https://www.linkedin.com/in/tom-sahar)


