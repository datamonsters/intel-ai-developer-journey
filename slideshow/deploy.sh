scp -P 17022 -r [!.]* publisher@datamonsters.co:/home/publisher/intel-slideshow
ssh root@datamonsters.co -p 17022 'supervisorctl restart intel-slideshow'