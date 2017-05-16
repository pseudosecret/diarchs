Hello.

The files in this folder are intended to help with the maintenance of the democracy world. Here are a few things required to get started:

- update pg_hba.conf from peer to md5 on the line concerning postgres
- restart PostgreSQL server
- create a user per the create_db.py file
- run the create_db.py file

From there, create the following cron jobs (modify as appropriate):

*/47 * * * * /path/to/virtualenv/python3 /path/to/diarchs/democracy/world_building/robots_vote.py > /dev/null 2>&1

1 0 * * * /path/to/virtualenv/python3 /path/to/diarchs/world_building/democracy/nightly_maitenance.py > /dev/null 2>&1
