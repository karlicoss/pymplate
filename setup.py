url = 'https://github.com/TODO'
author = 'TODO'
author_email = 'todo@todo.com'
description = 'TODO'


from setuptools import setup, find_packages


if __name__ == '__main__':
    # from setuptools_scm import get_version
    # https://github.com/pypa/setuptools_scm#default-versioning-scheme
    # get_version(version_scheme='python-simplified-semver', local_scheme='no-local-version')
   
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
        install_requires=['atomicwrites'],
        extras_require={
            'testing': ['pytest'],
            'linting': ['pytest', 'mypy', 'pylint'],
        },
        package_data={pkg: ['py.typed']},
    )
