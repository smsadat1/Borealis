pip install nuitka
python -m nuitka --onefile cli/main.py
mv main.bin borealis
chmod +x borealis 
cp borealis /usr/local/bin/