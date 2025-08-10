use std::collections::{HashMap, HashSet};

pub fn next_secret_number(secret: i64) -> i64 {
    let next_num = |secret: i64, num: i64| (secret ^ num) % 16777216;

    let first = next_num(secret, 64 * secret);
    let second = next_num(first, first / 32);
    let third = next_num(second, 2048 * second);

    third
}

pub fn sol(input: &str, num_iters: i64) {
    let mut secret_sum = 0;

    for line in input.lines() {
        let initial_secret: i64 = line.parse().expect("Failed to parse input to integer.");
        let mut secret = initial_secret;

        for _ in 0..num_iters {
            secret = next_secret_number(secret);
        }

        secret_sum += secret;

        //println!("{initial_secret}: {secret}");
    }
    println!("secret sum: {secret_sum}");
}

pub fn sol2(input: &str, num_iters: usize) {
    let mut sequence_values: HashMap<(i64, i64, i64, i64), i64> = HashMap::new();
    let mut seen_sequences: HashSet<(i64, i64, i64, i64)> = HashSet::new();

    for line in input.lines() {
        let mut secret: i64 = line.parse().expect("Failed to parse input to integer.");
        let mut prev = secret % 10;
        let mut diffs = [0i64; 4];

        // fill the first 4 price diffs
        for i in 0..4 {
            secret = next_secret_number(secret);
            let price = secret % 10;
            diffs[i] = price - prev;
            prev = price;
        }

        // get the rest of the price diffs and update 4-sequence values
        for _ in 4..num_iters + 1 {
            let sequence = (diffs[0], diffs[1], diffs[2], diffs[3]);
            if !seen_sequences.contains(&sequence) {
                *sequence_values.entry(sequence).or_insert(0) += prev;
                seen_sequences.insert(sequence);
            }

            secret = next_secret_number(secret);
            let price = secret % 10;
            // shift diffs left
            diffs[0] = diffs[1];
            diffs[1] = diffs[2];
            diffs[2] = diffs[3];
            diffs[3] = price - prev;
            prev = price;
        }

        seen_sequences.clear();
    }

    // sort sequence map by highest value to get best sequence
    let mut sequence_vec: Vec<(&(i64, i64, i64, i64), &i64)> = sequence_values.iter().collect();
    sequence_vec.sort_by(|a, b| b.1.cmp(a.1));
    if let Some(best_sequence) = sequence_vec.first() {
        println!("{best_sequence:?}");
    }
}
