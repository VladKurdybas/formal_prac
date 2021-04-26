run:
	/usr/bin/python3 main.py

test:
	for file in `ls tests | grep input`; do \
		/usr/bin/python3 main.py \
   		<tests/$$file >tests/output`echo "$$file" | cut -c6-`; \
	done
	for file in `ls tests | grep input`; do \
		exp="tests/expected`echo "$$file" | cut -c6-`"; \
		out="tests/output`echo "$$file" | cut -c6-`"; \
		tst="test`echo "$$file" | cut -c6-`"; \
		echo "\n\n`echo $$tst`:\n\n`cat tests/$$file`\nexpected: `cat $$exp` output: `cat $$out`"; \
		if `echo `diff $$out $$exp``; then echo checker: OK; else echo checker: NOT OK; fi \
	done
