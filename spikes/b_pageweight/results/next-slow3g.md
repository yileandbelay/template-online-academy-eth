## Option 1: Next.js 16 static, slow3g, 4x CPU (slow3g)
| page | status | requests | total KB | JS KB | CSS KB | HTML KB | font KB | image KB | FCP ms | LCP ms | network idle ms | h-overflow |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| / | 200 | 20 | 158.4 | 139.1 | 1.2 | 3.3 | 0.0 | 0.0 | 960 | 960 | 6069 | no |
| /courses | 200 | 22 | 162.3 | 139.1 | 1.2 | 4.4 | 0.0 | 0.0 | 996 | 996 | 6419 | no |
| /courses/project-management-fundamentals | 200 | 17 | 154.0 | 140.2 | 1.2 | 3.1 | 0.0 | 0.0 | 996 | 996 | 6040 | no |
| /lesson/1 | 200 | 14 | 150.3 | 139.4 | 1.2 | 3.2 | 0.0 | 0.0 | 964 | 964 | 6007 | no |
| /plain | 200 | 13 | 148.9 | 138.3 | 1.2 | 2.9 | 0.0 | 0.0 | 964 | 964 | 5980 | no |
