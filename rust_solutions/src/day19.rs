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
    let mut word_slice: &str;
    let mut is_valid = false;

    while curr_idx <= pattern.len() {
        word_slice = &pattern[..curr_idx];
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
    }

    is_valid
}

pub fn sol2() {
    let mut filename = utils::read_filename_from_input();
    if String::is_empty(&filename) {
        filename = String::from("example_inputs/day19.txt");
    }
    let contents = fs::read_to_string(&filename).expect("Failed to read file contents");
    let contents: Vec<&str> = contents.lines().collect();

    let towel_patterns: HashSet<&str> = match contents.get(0) {
        Some(patterns) => patterns.split(",").map(|word| word.trim()).collect(),
        None => HashSet::new(),
    };
    let required_patterns = &contents[2..];

    let mut memo: HashMap<String, usize> = HashMap::new();
    let count = required_patterns.iter().fold(0, |acc, pattern: &&str| {
        let num = num_valid_towel_patterns(&towel_patterns, pattern, &mut memo);
        //println!("{num}");
        acc + num
    });
    println!("num valid: {count}");
}

fn num_valid_towel_patterns(
    towel_patterns: &HashSet<&str>,
    pattern: &str,
    memo: &mut HashMap<String, usize>,
) -> usize {
    match memo.get(pattern) {
        Some(num_valid) => return *num_valid,
        None => (),
    }

    let mut curr_idx = 1;
    let mut word_slice: &str;
    let mut num_valid: usize = 0;

    while curr_idx <= pattern.len() {
        word_slice = &pattern[..curr_idx];
        if towel_patterns.contains(word_slice) {
            if word_slice.len() == pattern.len() {
                num_valid += 1;
                memo.insert(String::from(&pattern[..curr_idx]), num_valid);
            } else {
                num_valid += num_valid_towel_patterns(towel_patterns, &pattern[curr_idx..], memo);
            }
        }
        
        curr_idx += 1;
    }
    
    memo.insert(String::from(pattern), num_valid);
    num_valid
}