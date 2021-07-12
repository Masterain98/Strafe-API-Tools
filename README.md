# Strafe-API-Tools
Automation Tools for com.strafe.strafeapp

## Introduction

Strafe-API-Tools is a Python programing, using Strafe API to collect esports odds data for analytics purpose. With some simple judgment, it can also cast vote for teams automatically based on odds and vote counts of the community.

## How to use

1. Gets your Strafe authorization code with your network tool and Strafe Apps, and fill it in ```strafeRequest.py```, it should starts with ```Bearer```

2. Set your black list in ```config.py```, you can set ```debugLevel``` to `2` if you need more program output

3. Set your MySQL database connection information in ```/mysql_pool/db_config.py```, you should not use a ```root``` account for security concerns
4. Run ```main.py```

