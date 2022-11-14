set root=C:\Users\home\anaconda3
call %root%\Scripts\activate.bat %root%
call conda activate py37_light
pyinstaller --onefile --noconsole main.py