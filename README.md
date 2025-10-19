# Happy Lang

I was bored, so I made my own language.
It transpiles to python, and uses the `.hpy` extension which is a short-form for happy.

The syntax- 
```happyLang
speak "Enter the number of terms (n > 1):"
listen n int

a=0
b=1
speak a
speak b

repeat n times
    c=a+b
    speak c
    a=b
    b=c
end


```

In Python-

```python

print("Enter the number of terms (n > 1):")
n = int(input())
a=0
b=1
print(a)
print(b)
for _i in range(n):
    c=a+b
    print(c)
    a=b
    b=c

```
