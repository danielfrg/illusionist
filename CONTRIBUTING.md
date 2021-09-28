# Contributing

## Development environment

### Python

Create Python env

```
make env
```

### JS

Install deps

```
make npm-install
```

### Iteration cycle

Start webpack in watch mode.

```
make npm-dev
```

Now run nbconvert on one or all the examples:

```
make example
make examples
```

Run the http server on the examples dir:

```
make serve-examples
```

With this setup:

-   To see changes on the JS part you can just refresh the page
-   To see changes on the python (nbconvert) part, run `make examples` again

## Tests

```
make test
```

Check linting and format

```
make check
make fmt
```
