import imlog
import os
import glob
import codecs

source_root = '/root/adium_logs/Logs/Jabber.marvin@jabber.org.com'
dest_root = '/tmp/logs'
jabber_domain = 'jabber.org.com'

for channel in os.listdir(source_root):

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

      # Sanitize the 'channel' string a bit
      if channel.startswith('._'):
        channel = channel[len('._'):]
      if channel.endswith('@' + jabber_domain):
        channel = channel[:-len('@' + jabber_domain)]
      elif channel.endswith('@conference.' + jabber_domain): 
        channel = channel[:-len('@conference.' + jabber_domain)]
        channel = '#' + channel

      # Sanitize the 'sender' string a bit
      sender = msg.sender
      if sender.startswith('._'):
        sender = sender[len('._'):]
      if sender.endswith('@' + jabber_domain):
        sender = sender[:-len('@' + jabber_domain)]

      # Write out the log message to the file
      text_entry = msg.time.strftime('%H:%M:%S') + '<' + sender + '> ' + msg.text
      log_file = os.path.join(year_month_dir, channel + "." + msg.time.strftime('%d') + ".log")
      # print "log file is " + log_file
      with open(log_file, "a") as f:
        f.write(text_entry.encode('ascii', 'ignore') + '\n')
        f.close()
