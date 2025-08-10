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

    for line in input.lines() {
        let mut secret: i64 = line.parse().expect("Failed to parse input to integer.");
        let mut prev = secret % 10;
        let mut price_diffs: Vec<i64> = vec![];
        let mut seen_sequences: HashSet<(i64, i64, i64, i64)> = HashSet::new();

        // only get the first 3 price diffs
        for _ in 0..3 {
            secret = next_secret_number(secret);
            let price = secret % 10;
            price_diffs.push(price - prev);
            prev = price;
        }

        // get the rest of the price diffs and update 4-sequence values
        for i in 3..num_iters {
            secret = next_secret_number(secret);
            let price = secret % 10;
            price_diffs.push(price - prev);
            prev = price;

            let sequence = (
                price_diffs[i - 3],
                price_diffs[i - 2],
                price_diffs[i - 1],
                price_diffs[i],
            );
            if !seen_sequences.contains(&sequence) {
                let value = sequence_values.entry(sequence).or_insert(0);
                *value += price;
                seen_sequences.insert(sequence);
            }
        }

        seen_sequences.clear();
    }

    // sort sequence map by highest value to get best sequence
    let mut sequence_vec: Vec<(&(i64, i64, i64, i64), &i64)> = sequence_values.iter().collect();
    sequence_vec.sort_by(|a, b| b.1.cmp(a.1));
    let best_sequence = sequence_vec.first().unwrap();
    println!("{best_sequence:?}")
}
