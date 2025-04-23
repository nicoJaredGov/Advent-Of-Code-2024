use std::collections::HashSet;

use crate::utils;

pub fn sol(input: &str) {
    let graph = utils::build_undirected_graph(input);

    let mut cliques: Vec<HashSet<&str>> = vec![];
    for (computer, adjacency_set) in graph.iter() {
        if adjacency_set.len() < 2 {
            continue;
        }

        let computer_starts_with_t = computer.starts_with('t');
        for adjacency in adjacency_set {
            let starts_with_t = adjacency.starts_with('t') || computer_starts_with_t;
            let intersect = graph
                .get(adjacency)
                .unwrap()
                .intersection(adjacency_set);

            intersect
                .filter(|x| x.starts_with('t') || starts_with_t)
                .map(|i| {
                    let mut l = HashSet::new();
                    l.insert(*i);
                    l.insert(*adjacency);
                    l.insert(*computer);
                    l
                })
                .for_each(|h| {
                    if !cliques.contains(&h) {
                        cliques.push(h)
                    }
                });
            //println!("{computer} {adjacency}");
        }
    }

    let num_cliques = cliques.len();
    println!("{num_cliques}");
}
