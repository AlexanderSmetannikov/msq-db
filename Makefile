all:
	nvcc -o nearest vec_sem.cu -I/home/lutfulin/Desktop/cnpy -L/home/lutfulin/Desktop/cnpy/lib -lcnpy -std=c++11
query:
	rm ../query.npy
	python3 embedder.py
test:
	python3 test.py
clean:
	rm nearest