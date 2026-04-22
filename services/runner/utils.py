image_map = {
    "Python3.8": "borealis-exec-py-3-8:latest",
    "Python3.10": "borealis-exec-py-3-10:latest",
    "Python3.12": "borealis-exec-py-3-12:latest",
    "C11": "borealis-exec-c-cpp:latest",
    "C17": "borealis-exec-c-cpp:latest",
    "C99": "borealis-exec-c-cpp:latest",
    "C++11": "borealis-exec-c-cpp:latest",
    "C++17": "borealis-exec-c-cpp:latest",
    "C++20": "borealis-exec-c-cpp:latest",
    "Node14": "borealis-exec-js-node-20:latest",
    "Node18": "borealis-exec-js-node-18:latest",
    "Node20": "borealis-exec-js-node-20:latest",
    "Java8": "borealis-exec-java-8:latest",
    "Java11": "borealis-exec-java-11:latest",
    "Java17": "borealis-exec-java-17:latest",
    "PHP7.4": "borealis-exec-php-7.4:latest",
    "PHP8.0": "borealis-exec-php-8.0:latest",
    "PHP8.2": "borealis-exec-php-8.2:latest",
    "Go1.18": "borealis-exec-go-1.18:latest",
    "Go1.20": "borealis-exec-go-1.20:latest",
    "Go1.22": "borealis-exec-go-1.22:latest",
    "Rust1.60": "borealis-exec-rust-1.60:latest",
    "Rust1.70": "borealis-exec-rust-1.70:latest",
    "Rust1.75": "borealis-exec-rust-1.75:latest",
    ".NET6": "borealis-exec-csharp-6:latest",
    ".NET7": "borealis-exec-csharp-7:latest",
    ".NET8": "borealis-exec-csharp-8:latest",
    "Ruby2.7": "borealis-exec-ruby-2.7:latest",
    "Ruby3.0": "borealis-exec-ruby-3.0:latest",
    "Ruby3.2": "borealis-exec-ruby-3.2:latest",
}

c_cpp_std = {
    'C': {
        'C99': '-std=c99',
        'C11': '-std=c11',
        'C17': '-std=gnu17'
    },
    'C++': {
        'C++11': '-std=c++11',
        'C++17': '-std=c++17',
        'C++20': '-std=c++20',
    }
}

compiled_langs = ["C", "C++", "C#", "Go", "Java", "Rust"]
interpreted_langs = ["Javascript", "Python", "PHP", "Ruby"]

compiler = {
    "C": "gcc", 
    "C++": "g++",
    "C#": "mcs",
    "Go": "go",
    "Java": "javac",
    "Rust": "rustc",
}