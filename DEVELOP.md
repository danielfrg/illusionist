# Development

Setting up development for quick iteration

Python:

```
# Create conda env
make env
conda activate illusionist

# Install package
make develop
```

JS:

```
# Install deps
make npm-install
```

## Iteration cycle

Start webpack in watch mode, this will place the built files in the
nbconvert template static directory.

```
make npm-dev
```

Now run nbconvert on the examples:

```
make examples
```

Run the http server on the examples dir:

```
make serve-examples
```

With this for changes on the JS you can just refresh the page.
For changes on the python (nbconvert) part, run `make examples` each time.

## Testing

```
# Check linting and format
make check
make fmt

# Run tests
make test
```
