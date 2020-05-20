#! SHELL=/bin/sh

supervisorctl = /home/work/supervisor/bin/supervisorctl

restart:
	${supervisorctl} restart vadd_ws:*;

restart1:
	${supervisorctl} restart vadd_ws:vadd_ws-9900;

