#include<stdio.h>
void main(){
    int a[100],i,n,x,p;
    printf("\n Enter the number of elements in the array: ");
    scanf("%d",&n);
    printf("enter the elements: ");
    for(i=0;i<n;i++)
    {
        scanf("%d",&a[i]);
    }
    printf("array elements are: \n");
    for(i=0;i<n;i++)
    {
        printf("%d",a[i]);
    }
    printf("\n Enter the element is to be inserted: ");
    scanf("%d",&x);
    printf("\n enter the position where u have to insert the new element: ");
    scanf("%d",&p);
    for(i=n;i>=p;i--)
    a[i]=a[i-1];
    a[p-1]=x;
    for(i=0;i<=n;i++)
    {
        printf("%d",a[i]);
    }
}