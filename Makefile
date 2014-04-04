aria2c-server-start:
	@ ./tests/bin/aria2c-server.sh start

aria2c-server-stop:
	@ ./tests/bin/aria2c-server.sh stop

aria2c-server-status:
	@ ./tests/bin/aria2c-server.sh status

aria2c-server-restart:
	@ ./tests/bin/aria2c-server.sh restart


dev-server-start:
	@ ./tests/bin/dev-server.sh start

dev-server-stop:
	@ ./tests/bin/dev-server.sh stop

dev-server-status:
	@ ./tests/bin/dev-server.sh status

dev-server-restart:
	@ ./tests/bin/dev-server.sh restart


test-all: aria2c-server-restart dev-server-restart
	@ rm -f tests/store/*
	@ sleep 2
	@ nosetests --cover-package=aria2clib --verbosity=1 --cover-erase

test-all-with-coverage: aria2c-server-restart dev-server-restart
	@ rm -f tests/store/*
	@ sleep 2
	@ nosetests --with-coverage --cover-package=aria2clib  --verbosity=1 --cover-erase
	
	
	
