# Unix File Permissions - Full Setup Guide

## Overview
This guide demonstrates basic Unix user management and file permission concepts by creating two users with different access levels to a simple script.

## Prerequisites
- A Unix-like operating system (Linux, macOS, etc.)
- Root or sudo access

## Full Setup Instructions

1. Create two groups:
   ```bash
   sudo groupadd access_group
   sudo groupadd no_access_group
   ```

2. Create two users and add them to the respective groups:
   ```bash
   sudo useradd -m -G access_group user1
   sudo useradd -m -G no_access_group user2
   ```

3. Set passwords for the new users:
   ```bash
   sudo passwd user1
   sudo passwd user2
   ```
   You'll be prompted to enter and confirm a password for each user.

4. Create a shared directory and a simple "Hello, World!" script:
   ```bash
   sudo mkdir /home/shared
   echo '#!/bin/bash' | sudo tee /home/shared/hello_world.sh
   echo 'echo "Hello, World!"' | sudo tee -a /home/shared/hello_world.sh
   ```

5. Set the ownership and permissions of the script:
   ```bash
   sudo chown root:access_group /home/shared/hello_world.sh
   sudo chmod 750 /home/shared/hello_world.sh
   ```

6. Make the shared directory accessible:
   ```bash
   sudo chmod 755 /home/shared
   ```

## Testing the Setup

1. Verify the file permissions:
   ```bash
   ls -l /home/shared/hello_world.sh
   ```
   You should see output similar to:
   ```
   -rwxr-x--- 1 root access_group 31 [date] /home/shared/hello_world.sh
   ```

2. Test access as user1:
   ```bash
   su - user1
   /home/shared/hello_world.sh
   ls -l /home/shared/hello_world.sh
   exit
   ```
   You should see "Hello, World!" printed and be able to see the file permissions.

3. Test access as user2:
   ```bash
   su - user2
   /home/shared/hello_world.sh
   ls -l /home/shared/hello_world.sh
   exit
   ```
   You should see a "Permission denied" error for running the script, but you should be able to see the file permissions.

## Explanation

- `user1` can execute the script because they are part of the `access_group`.
- `user2` cannot execute the script but can see that it exists.
- Both users can view the file permissions using `ls -l`.
- The permissions "750" on the script mean:
  - Owner (root) can read, write, and execute (7)
  - Group (access_group) can read and execute (5)
  - Others (including user2) have no permissions (0)

## Cleaning Up (Optional)

To remove the users, groups, and files created for this demo:

```bash
sudo userdel -r user1
sudo userdel -r user2
sudo groupdel access_group
sudo groupdel no_access_group
sudo rm -r /home/shared
```

## What You'll Learn

- Creating users and groups in a Unix-like system
- Setting file permissions using chmod
- Understanding the effects of file ownership and group membership
- Basic sudo usage for administrative tasks

## Security Note

This is a demonstration project. In a real-world scenario, you would use more secure practices for user creation, password management, and file permissions.

