use std::collections::HashSet;

use crate::utils;

pub fn sol(input: &str, board_length: i32, limit: usize) {
    let obstacles = utils::get_2d_obstacles_set(input, limit);
    let destination = (board_length - 1, board_length - 1);
    utils::draw_grid(&obstacles, board_length as usize, board_length as usize);

    let is_valid_position = |pos: &(i32, i32)| -> bool {
        let is_out_of_bounds =
            pos.0 < 0 || pos.0 >= board_length || pos.1 < 0 || pos.1 >= board_length;
        if is_out_of_bounds || obstacles.contains(&pos) {
            return false;
        }
        true
    };

    let mut frontier = vec![(0, 0)];
    let mut visited: HashSet<(i32, i32)> = HashSet::new();
    let mut path_length = 0;

    while !frontier.is_empty() {
        let curr = frontier.pop().unwrap();
        visited.insert(curr);

        let neighbours = [
            (curr.0 - 1, curr.1),
            (curr.0 + 1, curr.1),
            (curr.0, curr.1 - 1),
            (curr.0, curr.1 + 1),
        ];
        for pos in neighbours {
            if pos == destination {
                path_length += 1;
                break;
            }
            if is_valid_position(&pos) && !visited.contains(&pos) {
                frontier.push(pos);
            }
        }

        path_length += 1;
    }

    println!("{path_length}");
}
