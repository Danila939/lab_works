// ConsoleApplication83.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include <thread>
#include <Windows.h>
#include <atomic>
using namespace std;

const size_t NTHREAD = 4;

atomic_flag aflag = ATOMIC_FLAG_INIT; //инициализация atomic_flag



double f(double a, int i, double h)
{
	double x = a + i * h;

	return x * x + 1;
}


void Simp_sum(int n, double left, double right, double& global_sum, int k)
{
	double local_sum = 0.0;
	double h = (right - left) / double(n);
	double z = left;
	local_sum += h / 3 * f(left, 0, h);
	z += h;
	int j = 1;
	while ((z > left) && (z <= right + 0.001))
	{
		if (j == n)
			local_sum += h / 3 * f(left, j, h);
		else if (j % 2 == 0)
			local_sum += 2.0 * h / 3.0 * f(left, j, h);
		else
			local_sum += 4.0 * h / 3.0 * f(left, j, h);
		j++;
		z += h;
	}
	if (k == 0) {
		global_sum = local_sum;
		return;
	}


	while (aflag.test_and_set()) //организация критической секции
		Sleep(0);
	global_sum += local_sum;
	aflag.clear();
}


double Simp_parallel(double a, double b, int n)
{
	thread t[NTHREAD];
	double block_size = (b - a) / double(NTHREAD);

	int k = 1;
	double global_Simp_sum = 0.0;
	for (int i = 0; i < NTHREAD; i++)
	{

		if (i == NTHREAD - 1)
			t[i] = thread(Simp_sum, n, a + block_size * i, b, ref(global_Simp_sum), k);
		else
			t[i] = thread(Simp_sum, n, a + block_size * i, a + block_size * (i + 1), ref(global_Simp_sum), k);
	}

	for (size_t i = 0; i < NTHREAD; i++)
	{
		t[i].join();
	}



	return global_Simp_sum;

}



int main()
{
	double a = 1, b = 2;
	int n = 10;
	int k = 0;
	double nonpp;
	Simp_sum(n, a, b, nonpp, k);
	cout << "Simp_nonparallel: " << nonpp << "\n";
	cout << "Simp_parallel: " << Simp_parallel(a, b, n);


	return 0;

}


