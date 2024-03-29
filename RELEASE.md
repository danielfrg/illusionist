# Releasing

## Upload to PyPI

- Update version on `__init__.py`
- Update version on `pyproject.toml`
- Update `CHANGELOG.md`
- Update `README.md` and docs

```shell
export VERSION=1.0.0

# Optional reset
make cleanall resetjs
make npm-install

# Build
make all
make upload-pypi

git commit -am "Release ${VERSION}" --allow-empty
git tag ${VERSION}

git push origin ${VERSION}
git push
```

## Upload to NPM

- Update version in `package.json`

```shell
export VERSION=1.0.0

cd js

npm version ${VERSION}
npm publish

git commit -am "NPM Release ${VERSION}" --allow-empty
git push
```
