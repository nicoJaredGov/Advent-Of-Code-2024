mod day19;
mod utils;

use std::fs;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let len = args.len();
    for arg in &args[1..len] {
        match fs::read_to_string(arg) {
            Ok(content) => day19::sol2(&content),
            Err(e) => eprintln!("Failed to read file {arg}: {e}"),
        }
    }
}
