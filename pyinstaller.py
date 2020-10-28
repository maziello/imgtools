import PyInstaller.__main__

package_name = 'imgtools'
PyInstaller.__main__.run([
    f'--name={package_name}',
    # '--onedir',
    '--onefile',
    '--console',
    # '--exclude=PIL',
    # '--exclude=scipy',
    '--exclude=tk',
    '--exclude=tcl',
    'main.py'
])
