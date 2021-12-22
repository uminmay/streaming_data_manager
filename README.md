###########

Make Folders named Processing,queue and processed and Write a code that makes a file(txt) every second in the Processing folder, picks up all the files from processing and moves all the files to queue every 5 seconds. It then picks files from the queue folder and updates a column in MySQL/mongoDB table as 0/1 and moves the file to the Processed folder
Also, make sure that no files are moved from Processing to queue until the queue folder is empty.

###########

For Linux Systems, there is reoccuring MySQL connection error(Sometimes also for windows):

To fix, run 

SET GLOBAL max_allowed_packet=67108864;

on MySQL server.

If it still does not work might need to increase connection timeout value.

############

Uncomment sleep(0.2) before starting task1 and task2 (threads) if there is an error related to file being used by another process.

############


