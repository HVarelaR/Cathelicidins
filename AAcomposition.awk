## Amino acid composition defined with AWK.
function dump(arr,n)
    {
    for(i in arr)
        {
        printf("%s %d %f\n",i,arr[i],arr[i]/n);
        }
    }
BEGIN   {}
/^>/ {dump(array,N);print;delete array;N=0.0;next;}
    {
    for(i=1;i<=length($0);i++) { array[substr($0,i,1)]++;N++;}
    }
END {
    dump(array,N);
    }
