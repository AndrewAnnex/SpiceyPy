IF DEFINED DevEnvDir (
    ECHO "vcvarall.bat has been called"
) ELSE (
    IF "%ARCH%"=="32" (
        call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86
    ) ELSE (
        ECHO "probably a 64bit build"
    )
    IF "%ARCH%"=="64" (
        call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64
    ) ELSE (
        ECHO "probably a 32bit build"
    )
)

"%PYTHON%" setup.py install
if errorlevel 1 exit 1

:: Add more build steps here, if they are necessary.

:: See
:: http://docs.continuum.io/conda/build.html
:: for a list of environment variables that are set during the build process.
