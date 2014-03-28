test-all:
	@ nosetests

test-all-with-coverage:
	@ nosetests --with-coverage


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

dev-server-start:
	@ ./tests/dev-server.sh start

dev-server-stop:
	@ ./tests/dev-server.sh stop

dev-server-status:
	@ ./tests/dev-server.sh status

dev-server-restart:
	@ ./tests/dev-server.sh restart

	
	
