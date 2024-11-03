```
# Connect to MySQL container
docker exec -it mysql-container mysql -u myuser -pmypassword

# Once inside MySQL, here are useful commands:
show databases;           # List all databases
use userdb;              # Switch to our database
show tables;             # List all tables
select * from users;     # View all users
describe users;          # View table structure

# Some additional useful MySQL commands:
# Show created time and other details
show table status;

# Show specific columns
select id, name from users;

# Count total users
select count(*) from users;
```

```
# Connect to Redis container
docker exec -it redis-container redis-cli

# Once inside Redis, here are useful commands:
KEYS *                   # Show all keys
GET all_users           # Get value for specific key
TTL all_users          # Check remaining time (in seconds) for key
INFO                    # Show Redis server information
MONITOR                # Watch live requests (ctrl+c to exit)

# Some additional useful Redis commands:
# Delete a key
DEL all_users

# Check type of value
TYPE all_users

# Clear all data
FLUSHALL
```

```
# 1. First clear Redis cache
docker exec -it redis-container redis-cli FLUSHALL

# 2. Add new user via API
curl -X POST http://localhost:8000/users/ \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "address": "123 Street", "occupation": "Developer"}'

# 3. Get users (this will cache in Redis)
curl http://localhost:8000/users/

# 4. Check MySQL data
docker exec -it mysql-container mysql -u myuser -pmypassword -e "use userdb; select * from users;"

# 5. Check Redis cache
docker exec -it redis-container redis-cli GET all_users
```