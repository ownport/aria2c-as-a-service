aria2c-start:
	@ echo '- Starting aria2c as daemon with RPC support'
	@ aria2c --enable-rpc --daemon --dir=store
	@ echo '- Done'

aria2c-stop:
	@ echo '- Stoppind aria2c'
	@ killall aria2c
	@ echo '- Done'

aria2c-status:
	@ ps aux | grep aria2c | grep 'daemon' | grep -v '/bin/sh'



test-server-start:
	@ ./tests/test-server.sh start

test-server-stop:
	@ ./tests/test-server.sh stop

test-server-status:
	@ ./tests/test-server.sh status

test-server-restart:
	@ ./tests/test-server.sh restart


			
