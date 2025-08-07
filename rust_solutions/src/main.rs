use rust_solutions::solutions;
use std::env;
use std::fs;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    let len = args.len();
    for arg in &args[1..len] {
        match fs::read_to_string(arg) {
            Ok(content) => {
                let before = Instant::now();
                solutions::day18_ram_run::sol(&content, 71, 1024);
                println!("\nSolution time: {} ms", before.elapsed().as_millis());
            }
            Err(e) => eprintln!("Failed to read file {arg}: {e}"),
        }
    }
}
