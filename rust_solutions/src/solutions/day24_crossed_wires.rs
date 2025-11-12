use crate::utils::EMPTY_LINE;
use std::collections::HashMap;

pub enum LogicGate {
    And,
    Or,
    Xor,
}

impl LogicGate {
    fn from_str(input: &str) -> Option<Self> {
        match input.trim().to_lowercase().as_str() {
            "and" => Some(LogicGate::And),
            "or" => Some(LogicGate::Or),
            "xor" => Some(LogicGate::Xor),
            _ => None,
        }
    }
}

pub fn map_str_to_bool(input: &str) -> bool {
    match input.trim() {
        "0" => false,
        "1" => true,
        _ => false,
    }
}

pub fn sol(input: &str) {
    let (initial_wires, operations) = input.split_once(EMPTY_LINE).unwrap();

    println!("{initial_wires:?}");
    println!("{operations:?}");

    let mut wire_values: HashMap<&str, bool> = initial_wires
        .lines()
        .map(|line| {
            let (k, v) = line.trim().split_once(':').unwrap();
            let v = map_str_to_bool(v);
            (k, v)
        })
        .collect();

    println!("{wire_values:?}");

    let operations: HashMap<&str, (LogicGate, &str, &str)> = operations
        .lines()
        .map(|line| {
            let args: Vec<&str> = line.trim().split(' ').collect();

            let out = *args.last().unwrap();

            let op = (
                LogicGate::from_str(args.get(1).unwrap()).unwrap(),
                *args.get(0).unwrap(),
                *args.get(2).unwrap(),
            );

            (out, op)
        })
        .collect();
}
