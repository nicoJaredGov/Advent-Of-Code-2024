use std::fs;
use crate::utils;

pub fn day19() {
    let mut filename = utils::read_filename_from_input();
    if String::is_empty(&filename) {
        filename = String::from("example_inputs/day19.txt");
    }
    println!("file name:\n{filename}\n");
    
    let contents = fs::read_to_string(&filename)
        .expect("Failed to read file contents");
    let contents: Vec<&str> = contents
        .lines()
        .collect();
    println!("{:?}  {}", contents, contents.len());

    let towel_patterns =  match contents.get(0) {
        Some(patterns) => patterns.split(",").map(|word| word.trim()).collect(),
        None => vec![],
    };
    println!("Towel patterns: {:?}", towel_patterns);

    let required_patterns = &contents[2..];
    println!("Required patterns: {:?}", required_patterns);
}