# Releasing

## Upload to PyPI

- Update version on `__init__.py`
- Update version on `pyproject.toml`
- Update `CHANGELOG.md`
- Update `README.md` and docs

```
export VERSION=1.0.0

git commit -am "Release ${VERSION}" --allow-empty
git tag ${VERSION}

# Optional reset
make cleanall

make all
make upload-pypi
git push origin ${VERSION}
git push
```

## Upload to NPM

- Update version in `package.json`

```
make npm-publish
```
