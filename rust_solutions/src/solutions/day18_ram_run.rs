use std::{collections::HashSet, i32::MAX};

use crate::utils;

pub struct Node {
    cell: (i32, i32),
    dist: i32,
    future_cost: i32,
}

// returns true if destination is found else false
pub fn a_star_search(
    obstacles: &HashSet<(i32, i32)>,
    grid_dim: (i32, i32),
    start_cell: (i32, i32),
    dest_cell: (i32, i32),
) -> bool {
    let (width, height) = grid_dim;

    let is_valid_position = |pos: &(i32, i32)| -> bool {
        let is_out_of_bounds = pos.0 < 0 || pos.0 >= width || pos.1 < 0 || pos.1 >= height;
        if is_out_of_bounds || obstacles.contains(&pos) {
            return false;
        }
        true
    };

    let start = Node {
        cell: start_cell,
        dist: 0,
        future_cost: MAX,
    };
    let deltas = [(0, 1), (1, 0), (-1, 0), (0, -1)];
    let mut frontier: Vec<Node> = vec![start];
    let mut visited: HashSet<(i32, i32)> = HashSet::new();

    while !frontier.is_empty() {
        frontier.sort_by(|a, b| (b.dist + b.future_cost).cmp(&(a.dist + a.future_cost)));
        let curr = frontier.pop().unwrap();

        if curr.cell == dest_cell {
            let path_length = curr.dist;
            println!("{path_length}");
            return true;
        }

        visited.insert(curr.cell);

        for delta in &deltas {
            let next = (curr.cell.0 + delta.0, curr.cell.1 + delta.1);
            if is_valid_position(&next) && !visited.contains(&next) {
                let next_position = Node {
                    cell: next,
                    dist: curr.dist + 1,
                    future_cost: utils::calculate_manhattan(&next, &dest_cell),
                };
                frontier.push(next_position);
            }
        }
    }

    println!("Destination was not reached.");
    return false;
}

pub fn sol(input: &str, board_length: i32, limit: usize) {
    let obstacles = utils::get_2d_obstacles_set(input, limit);
    let start = (0, 0);
    let dest = (board_length - 1, board_length - 1);
    utils::draw_grid(&obstacles, board_length, board_length);

    a_star_search(&obstacles, (board_length, board_length), start, dest);
}
