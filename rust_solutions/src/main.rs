use std::fs;
use std::env;
use std::time::Instant;
use rust_solutions::solutions;

fn main() {
    let args: Vec<String> = env::args().collect();
    let len = args.len();
    for arg in &args[1..len] {
        match fs::read_to_string(arg) {
            Ok(content) => {
                let before = Instant::now();
                solutions::day23::sol(&content);
                println!("Solution time: {} ms", before.elapsed().as_millis());
            },
            Err(e) => eprintln!("Failed to read file {arg}: {e}"),
        }
    }
}
