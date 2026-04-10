# borealis-exec-java:latest
FROM eclipse-temurin:21-jdk-jammy

WORKDIR /workspace

# For executing Java files
ENTRYPOINT ["sh", "-c"]