all:
	nvcc -o nearest vec_sem.cu -I/home/lutfulin/Desktop/cnpy -L/home/lutfulin/Desktop/cnpy/lib -lcnpy -std=c++11
clean:
	rm nearest