#/bin/bash
mkdir -p build
mkdir -p bin
echo "d9fe2def2a423cec1597180ff27706ee5fbf6c3db8c618a4ad2f91904e3331f8 bin/dwebp" | sha256sum -c - >/dev/null 2>/dev/null
if [ $? -ne 0 ]; then
	echo "No dwebp binary or sha256sum doesn't match, downloading"
	wget -q -c https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.0.3-linux-x86-64.tar.gz -O - | tar xOzv libwebp-1.0.3-linux-x86-64/bin/dwebp > bin/dwebp
fi
zip -r build/package.zip bin/* lambda_function.py
