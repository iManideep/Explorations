set /p local_repo_name="Local Repository Name?"
set /p repo_url="Repository URL?"
set /p venv_name="Virtual Environment Name?"
git clone %repo_url% %local_repo_name%
mkdir %venv_name%
cd %venv_name%
python -m venv %CD%