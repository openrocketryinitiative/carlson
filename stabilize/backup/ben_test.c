/**
 * THIS IS A TEST SCRIPT DO NOT USE
 */


#include <stdio.h>
#include <math.h>
#include "lapacke.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// Return norm of vector `src` (array) with `n` elements.
double norm(double *src, int n)
{
    double inner_sum = 0;
    for (int i = 0; i < n; i ++)
        inner_sum += (src[i] * src[i]);
    return sqrt(inner_sum);
}

int main()
{
    // http://www.netlib.org/clapack/old/double/dgetrs.c
    char    trans   = 'N';
    int     info    =  3;
    int     lda     =  3;
    int     ldb     =  3;
    int     n       =  3;
    int     nrhs    =  1;
    int     ipiv[3];
 
    // BEN testing

    // fin angles should be in RADIANS
    double fin_angles[3] = 
    {
        0.0,
        (2.0/3.0)*M_PI,
        (4.0/3.0)*M_PI
    };
    double velocity    = 1.0;
    double sq_velocity = velocity * velocity;

    // user inputs
    double angle    =  0.0;
    double force    =  0.0;
    double spin     = -1.0;



    // Preallocate the matrices. 
    //
    //    where `Ex = R`
    //
    // and x = E\R
    
    // Precompute norm division. We do the division here so we can use the
    // multiplication operator later (faster than division).
    double fa_norm     = norm(fin_angles, 3);
    double fa_norm_div = 1.0 / fa_norm;
    // printf("norm: %.2f, div: %.2f\n", fa_norm, fa_norm_div);

    // sin(fin_angles / norm(fin_angles))
    double fa_sin_norm[3] = {
        sin(fin_angles[0] - angle) * fa_norm_div,
        sin(fin_angles[1] - angle) * fa_norm_div,
        sin(fin_angles[2] - angle) * fa_norm_div
    };
    // printf("fa_sin_norm: ");
    // for (int k = 0; k < 3; k++)
    //     printf("%.2f ", fa_sin_norm[k]);
    // printf("\n");

    // cos(...)
    double fa_cos_norm[3] = {
        cos(fin_angles[0] - angle) * fa_norm_div,
        cos(fin_angles[1] - angle) * fa_norm_div,
        cos(fin_angles[2] - angle) * fa_norm_div
    };
    // printf("fa_cos_norm: ");
    // for (int k = 0; k < 3; k++)
    //     printf("%.2f ", fa_cos_norm[k]);
    // printf("\n");

    // Effects matrix, `E`
    double  E[9] =
    {
        fa_sin_norm[0], fa_sin_norm[1], fa_sin_norm[2],
        fa_cos_norm[0], fa_cos_norm[1], fa_cos_norm[2],
        1.0,            1.0,            1.0
    };
    // double E[9] = {
    //     1, 2, 3,
    //     2, 3, 4,
    //     3, 4, 1
    // };
    printf("E:\n");
    for (int r = 0; r < 3; r++)
    {
        for (int c = 0; c < 3; c++)
            printf("%.4f ", E[r*3 + c]);
        printf("\n");
    }
    printf("\n");

    // Results matrix, `R`
    double R[3] =
    {
        force,
        0.0,
        spin
    };
    // double R[3] = {
    //     -4,
    //     -1,
    //     -2
    // };
    printf("R:\n");
    for (int r = 0; r < 3; r++)
        printf("%.4f\n", R[r]);
    printf("\n");


 
    // Compute LU factorization
    // https://en.wikipedia.org/wiki/LU_decomposition

    //void LAPACK_dgetrf( lapack_int* m, lapack_int* n, double* a, lapack_int* lda, lapack_int* ipiv, lapack_int *info );
    LAPACK_dgetrf(&n, &n, E, &lda, ipiv, &info);
    // for (int j = 0; j < 9; j++)
    //     printf("%.4f ", E[j]);
    // printf("\n");

    // checks info, if info != 0 something goes wrong, for more information see the MAN page of dgetrf.
    if(info != 0)
    {
        printf("Error: %d\n", info);
    }
    else
    {
        // Solve a system of linear equations using LU factorization computed above.
        // http://www.netlib.org/clapack/old/double/dgetrs.c

        // void LAPACK_dgetrs( char* trans, lapack_int* n, lapack_int* nrhs, const double* a, lapack_int* lda, const lapack_int* ipiv,double* b, lapack_int* ldb, lapack_int *info );
        dgetrs_(&trans, &n, &nrhs, E, &lda, ipiv, R, &ldb, &info);
        if(info != 0)
        {
            // checks info, if info != 0 something goes wrong, for more information see the MAN page of dgetrs.
            printf("Error: %d\n", info);
        }
        else
        {
            printf("Result:\n{\n");
            for (int i = 0; i < n; i ++)
            {
                printf("\t%.2f\n", R[i]);
            }
            printf("}\n");
        }
    }



    // Convert forces result vector to angles and return
    // TODO: this should really just return RADIANs and then we can convert
    //       to degrees in Python
    double new_angles[3] = {
        asin(R[0] / sq_velocity) / M_PI * 180.0,
        asin(R[1] / sq_velocity) / M_PI * 180.0,
        asin(R[2] / sq_velocity) / M_PI * 180.0,
    };
 
    printf("new_angles: {\n");
    for (int i = 0; i < 3; i++)
        printf("\t%.2f\n", new_angles[i]);
    printf("}\n");

    // For some reason LAPACK output does not exactly match Matlab for \ (mldivide) operator

    return 0;
}