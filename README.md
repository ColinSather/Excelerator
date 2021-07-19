# Excelerator

Example of a config file `config/config.ini`, note how file paths do not have quotes.

```
[Exports]
path = C:\\Users\\csather\\Projects\\Excelerator\\examples\\exports\\

[Accounts]
checking = C:\\Users\\csather\\Projects\\Excelerator\\examples\\test.csv
savings = C:\\Users\\csather\\Projects\\Excelerator\\examples\\test2.csv
```

## CSV Schemas

Implement below samples in Excelerator's `config.ini` file. [See referenced document.](https://digital-preservation.github.io/csv-schema/csv-schema-1.0.html)

**Schema**
```
version 1.0
@totalColumns 3
name: notEmpty
age: range(0, 120)
gender: is("m") or is("f") or is("t") or is("n")
```

**Valid CSV**
```
name,age,gender
james,21,m
lauren,19,f
simon,57,m
```