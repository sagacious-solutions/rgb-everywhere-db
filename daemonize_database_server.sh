
pm2 stop rgb-database
pm2 delete rgb-database
source "start_database.sh"
pm2 start "python server.py" --name rgb-database
pm2 save
pm2 logs

