use crate::utils::EMPTY_LINE;
use std::collections::HashMap;

#[derive(Debug, Clone, Copy)]
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

pub fn map_bool_to_char(input: bool) -> char {
    match input {
        true => '1',
        false => '0',
    }
}

fn get_wire_value(
    wire: &str,
    operations: &HashMap<&str, (LogicGate, &str, &str)>,
    wire_values: &mut HashMap<String, bool>,
) -> bool {
    // Return if wire value is memoized
    if let Some(value) = wire_values.get(wire) {
        return *value;
    }

    // Get operation value (recursive if input wires are not memoized)
    let &(op, wire1, wire2) = operations
        .get(wire)
        .expect("Operation for this wire does not exist. Cannot continue.");

    let wire1_value = wire_values.get(wire1);
    let wire1_value = match wire1_value {
        Some(&val) => val,
        None => get_wire_value(wire1, operations, wire_values),
    };

    let wire2_value = wire_values.get(wire2);
    let wire2_value = match wire2_value {
        Some(&val) => val,
        None => get_wire_value(wire2, operations, wire_values),
    };

    // Perform operation
    let result = match op {
        LogicGate::And => wire1_value && wire2_value,
        LogicGate::Or => wire1_value || wire2_value,
        LogicGate::Xor => wire1_value ^ wire2_value,
    };

    wire_values.insert(wire.to_string(), result);

    return result;
}

pub fn sol(input: &str) {
    let (initial_wires, operations) = input.split_once(EMPTY_LINE).unwrap();

    //println!("{initial_wires:?}");
    //println!("{operations:?}");

    let mut wire_values: HashMap<String, bool> = initial_wires
        .lines()
        .map(|line| {
            let (k, v) = line.trim().split_once(':').unwrap();
            let v = map_str_to_bool(v);
            (k.to_string(), v)
        })
        .collect();

    //println!("{wire_values:?}");

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

    //println!("{operations:?}");

    let mut output = String::new();
    let mut count = 0;
    loop {
        let z_wire;
        if count < 10 {
            z_wire = "z0".to_string() + &count.to_string();
        } else {
            z_wire = "z".to_string() + &count.to_string();
        }

        if operations.contains_key(z_wire.as_str()) {
            let value = get_wire_value(&z_wire, &operations, &mut wire_values);
            output.push(map_bool_to_char(value));
        } else {
            break;
        }

        count += 1;
    }

    let reversed_output: String = output.chars().rev().collect();
    let result = i64::from_str_radix(&reversed_output, 2).unwrap();

    println!("{result}");
}
