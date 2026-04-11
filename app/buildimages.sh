docker build -t borealis-exec-c-cpp -f docker/languages/Dockerfile.c_cpp

docker build -t borealis-exec-csharp-6 -f docker/languages/Dockerfile.cs.6.0 .
docker build -t borealis-exec-csharp-7 -f docker/languages/Dockerfile.cs.7.0 .
docker build -t borealis-exec-csharp-8 -f docker/languages/Dockerfile.cs.8.0 .

docker build -t borealis-exec-go-1.18 -f docker/languages/Dockerfile.go.1.18 .
docker build -t borealis-exec-go-1.20 -f docker/languages/Dockerfile.go.1.20 .
docker build -t borealis-exec-go-1.22 -f docker/languages/Dockerfile.go.1.22 .

docker build -t borealis-exec-java-8 -f docker/languages/Dockerfile.java.8 .
docker build -t borealis-exec-java-11 -f docker/languages/Dockerfile.java.11 .
docker build -t borealis-exec-java-17 -f docker/languages/Dockerfile.java.17 .

docker build -t borealis-exec-js-node-14 -f docker/languages/Dockerfile.node.14 .
docker build -t borealis-exec-js-node-18 -f docker/languages/Dockerfile.node.18 .
docker build -t borealis-exec-js-node-20 -f docker/languages/Dockerfile.node.20 .

docker build -t borealis-exec-php-7.4 -f docker/languages/Dockerfile.php.7.4 .
docker build -t borealis-exec-php-8.0 -f docker/languages/Dockerfile.php.8.0 .
docker build -t borealis-exec-php-8.2 -f docker/languages/Dockerfile.php.8.2 .

docker build -t borealis-exec-py-3-8 -f docker/languages/Dockerfile.py.3.8 .
docker build -t borealis-exec-py-3-10 -f docker/languages/Dockerfile.py.3.10 .
docker build -t borealis-exec-py-3-12 -f docker/languages/Dockerfile.py.3.12 .

docker build -t borealis-exec-ruby-2.7 -f docker/languages/Dockerfile.ruby.2.7 .
docker build -t borealis-exec-ruby-3.0 -f docker/languages/Dockerfile.ruby.3.0 .
docker build -t borealis-exec-ruby-3.2 -f docker/languages/Dockerfile.ruby.3.2 .

docker build -t borealis-exec-rust-1.60 -f docker/languages/Dockerfile.rust.1.60 .
docker build -t borealis-exec-rust-1.70 -f docker/languages/Dockerfile.rust.1.70 .
docker build -t borealis-exec-rust-1.75 -f docker/languages/Dockerfile.rust.1.75 .
