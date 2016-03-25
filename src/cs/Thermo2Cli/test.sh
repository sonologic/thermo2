#!/bin/sh

set -e

mono --debug packages/xunit.runner.console.2.1.0/tools/xunit.console.exe Thermo2Cli.Tests/bin/Debug/Thermo2Cli.Tests.dll $@
