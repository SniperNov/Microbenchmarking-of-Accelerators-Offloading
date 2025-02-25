#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define DL 2000

double sumit(long n);

int main()
{

    const long maxdel = 10000;
    const long innerreps = 200;

    double start, t1, t2, t1and2, sum;
    long del;

    del = 20;

    while (del < maxdel)
    {

        sum = sumit(DL);
        start = omp_get_wtime();
        for (int r = 0; r < innerreps; r++)
        {
            sum += sumit(DL);
        }
        t1 = omp_get_wtime() - start;
        if (sum < 0.0)
            printf("%12.8f", sum);

        sum = sumit(del);
        start = omp_get_wtime();
        for (int r = 0; r < innerreps; r++)
        {
            sum = sumit(del);
        }
        t2 = omp_get_wtime() - start;
        if (sum < 0.0)
            printf("%12.8f", sum);

        sum = sumit(DL);
        sum += sumit(del);
        start = omp_get_wtime();
        for (int r = 0; r < innerreps; r++)
        {
            sum += sumit(DL);
            sum += sumit(del);
        }
        t1and2 = omp_get_wtime() - start;
        if (sum < 0.0)
            printf("%12.8f", sum);
        printf("del %d t1 %12.8f t2 %12.8f t1and2 %12.8f t1+t2-t1and2 %12.8f t1and2-t2 %12.8f\n", del, t1, t2, t1and2, t1 + t2 - t1and2, t1and2 - t2);

        del *= 1.1;
    }
}
