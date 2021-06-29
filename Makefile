restricted_conga:
	python3 main.py 0

unrestricted_conga:
	python3 main.py 1

clean:
	rm -r __pycache__/*.pyc
	rm -d __pycache__