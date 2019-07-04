
for i in 5 10 20 30 40 50 100 120 140 160 180 200 250 300 400 500 600 800 1000 1200 1500 2000
do
	for hilos in 2 3 4 5 6 7 8
	do
		for j in 1 2 3 4 5 6 7 8 9 10
		do
			echo $i
			./Nthread $i $hilos>> tiemposhilosxfilas.csv
		done
	done	
done
