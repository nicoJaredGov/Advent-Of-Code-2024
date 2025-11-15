use crate::utils::EMPTY_LINE;
use std::{collections::HashMap, str::FromStr};

#[derive(Debug, Clone, Copy)]
pub enum LogicGate {
    And,
    Or,
    Xor,
}

impl FromStr for LogicGate {
    type Err = ();

    fn from_str(input: &str) -> Result<Self, Self::Err> {
        match input.trim().to_lowercase().as_str() {
            "and" => Ok(LogicGate::And),
            "or" => Ok(LogicGate::Or),
            "xor" => Ok(LogicGate::Xor),
            _ => Err(()),
        }
    }
}

#[derive(Debug, Clone)]
struct LogicOperation {
    gate: LogicGate,
    lhs: String,
    rhs: String,
}

fn parse_bool(s: &str) -> Option<bool> {
    match s.trim() {
        "0" => Some(false),
        "1" => Some(true),
        _ => None,
    }
}

fn get_wire_value(
    wire: &str,
    operations: &HashMap<String, LogicOperation>,
    memo: &mut HashMap<String, bool>,
) -> bool {
    if let Some(value) = memo.get(wire) {
        return *value;
    }

    let op = operations
        .get(wire)
        .expect("Operation for this wire does not exist. Cannot continue.");

    let lhs_value = get_wire_value(&op.lhs, operations, memo);
    let rhs_value = get_wire_value(&op.rhs, operations, memo);

    // Perform operation
    let result = match op.gate {
        LogicGate::And => lhs_value && rhs_value,
        LogicGate::Or => lhs_value || rhs_value,
        LogicGate::Xor => lhs_value ^ rhs_value,
    };

    memo.insert(wire.to_string(), result);
    result
}

pub fn sol(input: &str) {
    let (initial_wires, operations) = input.split_once(EMPTY_LINE).unwrap();

    let mut memo: HashMap<String, bool> = initial_wires
        .lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() {
                return None;
            }

            let (k, v) = line.split_once(':')?;
            let v = parse_bool(v)?;
            Some((k.to_string(), v))
        })
        .collect();

    let operations: HashMap<String, LogicOperation> = operations
        .lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() {
                return None;
            }

            let parts: Vec<&str> = line.split_whitespace().collect();

            // Expect format: "<lhs> <gate> <rhs> -> <out>"
            if parts.len() != 5 {
                return None;
            }

            let gate = match parts[1].parse::<LogicGate>() {
                Ok(g) => g,
                Err(_) => return None,
            };

            let lhs = parts[0].to_string();
            let rhs = parts[2].to_string();
            let out = parts[4].to_string();

            Some((out, LogicOperation { gate, lhs, rhs }))
        })
        .collect();

    let mut bits: Vec<char> = Vec::new();
    let mut count: usize = 0;
    loop {
        let z_wire = format!("z{:02}", count);

        if !operations.contains_key(&z_wire) {
            break;
        }

        let value = get_wire_value(&z_wire, &operations, &mut memo);
        bits.push(if value { '1' } else { '0' });
        count += 1;
    }

    let result = bits
        .iter()
        .rev()
        .fold(0i64, |acc, &c| (acc << 1) | if c == '1' { 1 } else { 0 });

    println!("{result}");
}
