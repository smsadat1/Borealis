t = int(input())

for _ in range(t):
    a, b, c = map(int, input().split())

    s = a + b + c
    p = a * b * c

    print(f"Sum: {s}, Product: {p}")