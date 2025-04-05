use crate::utils;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;

pub fn sol() {
    let mut filename = utils::read_filename_from_input();
    if String::is_empty(&filename) {
        filename = String::from("example_inputs/day19.txt");
    }
    //println!("file name:\n{filename}\n");

    let contents = fs::read_to_string(&filename).expect("Failed to read file contents");
    let contents: Vec<&str> = contents.lines().collect();
    //println!("{:?}  {}", contents, contents.len());

    let towel_patterns: HashSet<&str> = match contents.get(0) {
        Some(patterns) => patterns.split(",").map(|word| word.trim()).collect(),
        None => HashSet::new(),
    };
    //println!("Towel patterns: {:?}", towel_patterns);

    let required_patterns = &contents[2..];
    //println!("Required patterns: {:?}", required_patterns);

    // let contains = towel_patterns.contains("wr");
    // println!("{contains}");

    // let isvalid = is_valid_towel_pattern(&towel_patterns, "rwr");
    // println!("{isvalid}")

    let mut memo: HashMap<String, bool> = HashMap::new();
    let count = required_patterns.iter().fold(0, |acc, pattern: &&str| {
        if is_valid_towel_pattern(&towel_patterns, pattern, &mut memo) {
            acc + 1
        } else {
            acc
        }
    });
    println!("num valid: {count}");
}

fn is_valid_towel_pattern(
    towel_patterns: &HashSet<&str>,
    pattern: &str,
    memo: &mut HashMap<String, bool>,
) -> bool {
    match memo.get(pattern) {
        Some(is_valid) => return *is_valid,
        None => (),
    }

    let mut curr_idx = 1;
    let mut word_slice = &pattern[..curr_idx];
    let mut is_valid = false;

    while !word_slice.is_empty() {
        if towel_patterns.contains(word_slice) {
            if word_slice.len() == pattern.len() {
                return true;
            }

            is_valid = is_valid_towel_pattern(towel_patterns, &pattern[curr_idx..], memo);
            memo.insert(String::from(&pattern[curr_idx..]), is_valid);
            if is_valid {
                return true;
            }
        }
        curr_idx += 1;
        if curr_idx > pattern.len() {
            break;
        }
        word_slice = &pattern[..curr_idx];
    }

    is_valid
}
