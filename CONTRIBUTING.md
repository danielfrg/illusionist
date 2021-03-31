# How to Contribute

## Development environment

Python:

Create conda env

```
make env
conda activate illusionist
make extensions
```

Install the package on dev mode

```
make develop
```

JS:

```
# Install deps
make npm-install
```

### Iteration cycle

Start webpack in watch mode, this will place the built files in the
nbconvert template static directory.

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
- To see changes on the JS part you can just refresh the page
- To see changes on the python (nbconvert) part, run `make examples` again

## Testing

Check linting and format

```
make check
make fmt
```

Run tests

````
make test
```