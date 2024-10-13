@echo off
rem precisa ante ter:
rem pip install pipreqs
rem pip3 install pip-tools
pipreqs ./src --savepath=requirements.in && pip-compile
if %errorlevel% GTR 0 (
  echo "#################################################"
  echo "Erro durante criacao do requeriments. Verifique: "
  echo "#################################################"
  echo "Se instalou o 'pipreqs': "
  echo "pip install pipreqs"
  echo "#################################################"
  echo "#################################################"
  echo "Se instalou o 'pip-tools': "
  echo "pip install pip-tools"
) ELSE (
  echo "Tudo ok! :)"
)
pause
exit 0