#/bin/bash
mkdir -p build
mkdir -p bin
wget -c https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.0.3-linux-x86-64.tar.gz -O - | tar xz - libwebp-1.0.3-linux-x86-64/bin/dwebp > bin/dwebp
zip -r build/package.zip bin/* lambda_function.py
