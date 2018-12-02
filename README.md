# flextable
tabular data formatter, for code, cli or pipes



### Pipe a file into a table
```
cat file | python flextable/cli.py  -d ':' --line 120 --length 10 -hc -hw -cc 9
```

### load a file with the cli
```
ft  -d ':' --line 0 --length 10 -cc 9
```

### format with code
```
import fte

print table(args).format
``


