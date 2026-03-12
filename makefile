build: build_app build_binary build_installer
	@echo Build Completed.
	@echo Result in dist/PyBuild-Installer.exe

install_clean: clean
	@echo Installing...
	@./dist/PyBuild-Installer.exe

clean: clear build

build_app:
	@echo Building app...
	@powershell -ExecutionPolicy Bypass -File pybuild.build.ps1

build_binary:
	@echo Setting up files...
	@python binary-build.py

build_installer:
	@echo Building installer...
	@powershell -ExecutionPolicy Bypass -File installer.build.ps1

clear:
	@echo Cleaning...
	@-del pybuild_app_binary_code.py
	@-rmdir /q /s build
	@-rmdir /q /s dist