const fs = require("fs");

const input = fs.readFileSync(0, "utf-8").trim().split("\n");

let t = parseInt(input[0]);
let idx = 1;

for (let i = 0; i < t; i++) {
    const [a, b, c] = input[idx++].split(" ").map(Number);

    const sum = a + b + c;
    const product = a * b * c;

    console.log(`Sum: ${sum}, Product: ${product}`);
}