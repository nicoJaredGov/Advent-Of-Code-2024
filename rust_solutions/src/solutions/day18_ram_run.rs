use std::{collections::HashSet, i32::MAX};

use crate::utils;

pub struct Node {
    cell: (i32, i32),
    dist: i32,
    future_cost: i32,
}

pub fn sol(input: &str, board_length: i32, limit: usize) {
    let obstacles = utils::get_2d_obstacles_set(input, limit);
    let destination = (board_length - 1, board_length - 1);
    let start = Node {
        cell: (0, 0),
        dist: 0,
        future_cost: MAX,
    };
    let deltas = [(0, 1), (1, 0), (-1, 0), (0, -1)];
    utils::draw_grid(&obstacles, board_length, board_length);

    let is_valid_position = |pos: &(i32, i32)| -> bool {
        let is_out_of_bounds =
            pos.0 < 0 || pos.0 >= board_length || pos.1 < 0 || pos.1 >= board_length;
        if is_out_of_bounds || obstacles.contains(&pos) {
            return false;
        }
        true
    };

    let mut frontier: Vec<Node> = vec![start];
    let mut visited: HashSet<(i32, i32)> = HashSet::new();

    while !frontier.is_empty() {
        frontier.sort_by(|a, b| (b.dist + b.future_cost).cmp(&(a.dist + a.future_cost)));
        let curr = frontier.pop().unwrap();

        if curr.cell == destination {
            let path_length = curr.dist;
            println!("{path_length}");
            return;
        }

        visited.insert(curr.cell);

        for delta in &deltas {
            let next = (curr.cell.0 + delta.0, curr.cell.1 + delta.1);
            if is_valid_position(&next) && !visited.contains(&next) {
                let next_position = Node {
                    cell: next,
                    dist: curr.dist + 1,
                    future_cost: utils::calculate_manhattan(&next, &destination),
                };
                frontier.push(next_position);
            }
        }
    }

    println!("Destination was not reached.");
}
