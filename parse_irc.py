import imlog
import os
import glob
import codecs

source_root = '/root/adium_logs/Logs/IRC.marvinpinto'
dest_root = '/tmp/logs'

for channel in os.listdir(source_root):
  # print channel
  mpath = os.path.join(source_root, channel)
  # print mpath
  for chatlog in glob.glob(mpath + "/*.chatlog"):
    # print chatlog
    log = imlog.AdiumLog(chatlog)
    for msg in log.messages:

      # Create the YYYY-MM directory, if it doesn't already exist
      year_month_dir = os.path.join(dest_root, msg.time.strftime('%Y-%m'))
      if not os.path.exists(year_month_dir):
        print "Creating directory " + year_month_dir
        os.makedirs(year_month_dir)

      # Write out the log message to the file
      text_entry = msg.time.strftime('%H:%M:%S') + '<' + msg.sender + '> ' + msg.text
      log_file = os.path.join(year_month_dir, channel + "." + msg.time.strftime('%d') + ".log")
      # print "log file is " + log_file
      with open(log_file, "a") as f:
        f.write(text_entry.encode('ascii', 'ignore') + '\n')
        f.close()
