OLD_DIR="$(pwd)"
cd ..
git add . && git commit -m "meow" && git push origin main
cd ../IME-Converter-web/
git add . && git commit -m "meow" && git push origin main
cd "$OLD_DIR"