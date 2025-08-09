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
