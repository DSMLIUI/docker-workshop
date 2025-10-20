**What we'll build**: A PostgreSQL database with pgAdmin web interface to learn:
- **Docker Networks**: How containers communicate
- **Docker Volumes**: How data persists
- **Docker Compose**: Multi-container orchestration

## Exercise 0.5: Understanding Multi-Container Applications

### Task
Learn why we need Docker Compose and what problems it solves.

### What You'll Learn:
- Why we need multiple containers
- What problems Docker Compose solves
- How services communicate
- Why we need persistent storage

### Instructions

**Step 1**: Try running multiple containers manually
```bash
# This is painful without Docker Compose!
docker run -d --name db postgres:15-alpine -e POSTGRES_PASSWORD=pass
docker run -d --name app --link db:db nginx:alpine
```

**Step 2**: See the problems
- Hard to manage dependencies
- No easy way to start/stop everything
- No shared networking
- No persistent storage
- Manual configuration for each container

**Step 3**: Understand the solution
Docker Compose solves these problems by:
- **Single configuration file** for all services
- **Automatic networking** between services
- **Volume management** for data persistence
- **Dependency management** (start order)
- **Environment variable** management

### Expected Result
- You understand why Docker Compose exists
- You see the problems it solves
- You're ready to learn the solution

## Exercise 1: Set Up Project Structure

### Task
Navigate to folder docker-compose 

```bash
cd ..
cd docker-compose
```
## Exercise 2: Check Database Schema & Environment

### Task
Open the init.sql adn the .env file to view the configuration

## Exercise 3: Review docker-compose.yml

### Task
Review Docker Compose configuration for PostgreSQL + pgAdmin stack.

**Step 2**: Key Concepts Explained

**🔗 Docker Networks**:
- `db-network` allows containers to communicate
- Services can reach each other using service names (`db`, `db-ui`)
- Isolated from other Docker networks

**💾 Docker Volumes**:
- `postgres_data` persists database data permanently
- `./init.sql` mounts initialization script
- Data survives container restarts and removal

**⚙️ Service Dependencies**:
- `depends_on` ensures pgAdmin waits for database to be healthy
- `healthcheck` monitors database readiness
- `restart: unless-stopped` ensures services restart automatically

## Exercise 4: Launch the Database Stack!

### Task
Launch PostgreSQL database with pgAdmin UI using Docker Compose.

### Instructions

**Step 1**: Start all services
```bash
docker-compose up -d
```

This creates:
1. Docker network for communication
2. Volume for data persistence  
3. PostgreSQL database with sample data
4. pgAdmin web interface

**Step 2**: Check status
```bash
docker-compose ps
```
**Step 3**: Access pgAdmin
Open **http://localhost:5050** in your browser

Login:
- Email: `admin@example.com`
- Password: `admin123`

# Exercise 5: Connect pgAdmin to PostgreSQL (2 minutes)

### Task
Connect pgAdmin UI to the PostgreSQL database using Docker network.

### Instructions

**Step 1**: Add database server in pgAdmin
- In pgAdmin (http://localhost:5050), right-click "Servers" → "Register" → "Server"
- **General tab**: Name: `E-Commerce DB`
- **Connection tab**:
  - Host: `db` ← **Key: Use service name, not localhost!**
  - Port: `5432`
  - Database: `ecommerce`
  - Username: `dbuser`
  - Password: `secure_pass_123`
- Click "Save"

**Step 2**: Explore the database
Expand: E-Commerce DB → Databases → ecommerce → Schemas → public → Tables
You'll see the `users` table with sample data.

**Step 3**: Run a query
- Right-click "ecommerce" → "Query Tool"
- Run: `SELECT * FROM users;`

## Exercise 6: Understanding Docker Networks & Volumes

### Task
Explore Docker networks and volumes to understand how containers communicate and persist data.

### Instructions

**Step 1**: Explore Docker Networks
```bash
# List all networks
docker network ls

# Inspect our network
docker network inspect database-demo_db-network
```

**Key Learning**: 
- Docker Compose creates isolated networks
- Services can reach each other using service names (`db`, `db-ui`)
- Each container gets an IP address automatically

**Step 2**: Explore Docker Volumes
```bash
# List all volumes
docker volume ls

# Inspect our data volume
docker volume inspect database-demo_postgres_data
```

**Step 3**: Test data persistence
```bash
# Add test data
docker-compose exec db psql -U dbuser -d ecommerce -c "INSERT INTO users (name, email) VALUES ('Test User', 'test@example.com');"

# Stop containers
docker-compose down

# Start again
docker-compose up -d

# Check data is still there!
docker-compose exec db psql -U dbuser -d ecommerce -c "SELECT * FROM users WHERE email='test@example.com';"
```

**Key Learning**: 
- Volumes persist data independently of containers
- Data survives container removal and recreation
- Perfect for databases and file storage

## Bonus Exercise 1: Essential Troubleshooting (3 minutes)

### Task
Learn to troubleshoot common Docker Compose issues.

### Instructions

**Step 1**: Common issues and solutions
```bash
# Issue: "Port already allocated"
# Solution: Change port or stop conflicting service
docker-compose down
# Edit docker-compose.yml ports: "5433:5432"
docker-compose up -d

# Issue: "Cannot connect to database"
# Solution: Check service is healthy
docker-compose ps
# Wait for db to be "healthy", not just "up"
```

**Step 2**: Debug service communication
```bash
# Check if services can reach each other
docker-compose exec db-ui ping db

# View service logs
docker-compose logs db
docker-compose logs db-ui
```

**Step 3**: Reset if needed
```bash
# Nuclear option (removes everything including data!)
docker-compose down -v
docker-compose up -d
```

### Expected Result
- Understanding of common Docker Compose issues
- Ability to debug service communication
- Knowledge of when to use `-v` flag

---

## Bonus Exercise 2: Cleanup & Management (1 minute)

### Task
Learn essential Docker Compose management commands.

### Instructions

**Step 1**: View logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs db
```

**Step 2**: Manage services
```bash
# Restart a service
docker-compose restart db-ui

# Stop services
docker-compose down
```

**Step 3**: Clean up (when done)
```bash
# Remove containers and networks, keep volumes
docker-compose down

# Remove everything including volumes (⚠️ deletes data!)
docker-compose down -v
```

---

