#include<stdio.h>
void main(){
    int m,n,i,j;
    printf("enter the no of rows and column: ");
    scanf("%d %d",&m,&n);
    int mat1[m][n],mat2[m][n],diff[m][n];
    printf("enter elements of the first matrix: ");
    for(i=0;i<m;i++){
        for(j=0;j<n;j++){
            scanf("%d",&mat1[i][j]);
        }
    }
    printf("enter elements of the second matrix: ");
    for(i=0;i<m;i++){
        for(j=0;j<n;j++){
            scanf("%d",&mat2[i][j]);
        }
    }
    for(i=0;i<m;i++){
        for(j=0;j<n;j++){
            diff[i][j]=mat1[i][j]-mat2[i][j];
        }
    }
    printf("the difference matrix is: ");
    for(i=0;i<m;i++){
        for(j=0;j<n;j++){
            printf("%d\t",diff[i][j]);
        }
        printf("\n");
    }
}