url = 'https://github.com/TODO'
author = 'TODO'
author_email = 'todo@todo.com'
description = 'TODO'

install_requires = [
]


from setuptools import setup, find_packages # type: ignore


def main():
    [pkg] = find_packages('src')
    setup(
        name=pkg,
        use_scm_version={
            'version_scheme': 'python-simplified-semver',
            'local_scheme': 'dirty-tag',
        },
        setup_requires=['setuptools_scm'],

        url=url,
        author=author,
        author_email=author_email,
        description=description,

        packages=[pkg],
        package_dir={'': 'src'},
        package_data={pkg: ['py.typed']},

        install_requires=install_requires,
        extras_require={
            'testing': ['pytest'],
            'linting': ['pytest', 'mypy', 'pylint'],
        },
    )

if __name__ == '__main__':
    main()

# TODO
# from setuptools_scm import get_version
# https://github.com/pypa/setuptools_scm#default-versioning-scheme
# get_version(version_scheme='python-simplified-semver', local_scheme='no-local-version')
