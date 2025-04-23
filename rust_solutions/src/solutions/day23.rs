use std::collections::HashSet;

use crate::utils;

pub fn sol(input: &str) {
    let graph = utils::build_undirected_graph(input);
    let mut cliques: HashSet<Vec<&str>> = HashSet::new();

    for (computer, adjacency_set) in graph.iter() {
        if adjacency_set.len() < 2 || !computer.starts_with('t') {
            continue;
        }

        for adjacency in adjacency_set {
            let intersect = graph.get(adjacency).unwrap().intersection(adjacency_set);
            intersect
                .map(|i| vec![*computer, *adjacency, *i])
                .for_each(|mut clique| {
                    clique.sort();
                    if !cliques.contains(&clique) {
                        cliques.insert(clique);
                    }
                });
        }
    }

    let num_cliques = cliques.len();
    println!("{num_cliques}");
}

pub fn sol2(input: &str) {
    let graph = utils::build_undirected_graph(input);

    let r: HashSet<&str> = HashSet::new();
    let p: HashSet<&str> = graph.keys().cloned().collect();
    let x: HashSet<&str> = HashSet::new();
    let mut max_clique: Vec<&str> = Vec::new();
    utils::bron_kerbosch_max_only(r, p, x, &graph, &mut max_clique);

    max_clique.sort();
    max_clique.iter().for_each(|c| print!("{c},"));
}
