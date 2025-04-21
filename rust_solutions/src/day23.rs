use std::collections::HashMap;
use std::collections::HashSet;

pub fn sol(input: &String) {
    let mut adjacency_map: HashMap<&str, HashSet<&str>> = Default::default();
    let pairs: Vec<Vec<&str>> = input
        .lines()
        .map(|line| line.split('-').collect())
        .collect();

    for pair in pairs {
        let first_computer = pair.get(0).unwrap();
        let second_computer = pair.get(1).unwrap();

        let first_adjacency_set = adjacency_map
            .entry(first_computer)
            .or_insert(HashSet::new());
        first_adjacency_set.insert(second_computer);

        let second_adjacency_set = adjacency_map
            .entry(second_computer)
            .or_insert(HashSet::new());
        second_adjacency_set.insert(first_computer);
    }
    //println!("{adjacency_map:?}");

    let mut cliques: Vec<HashSet<&str>> = vec![];
    for (computer, adjacency_set) in adjacency_map.iter() {
        if adjacency_set.len() < 2 {
            continue;
        }

        let computer_starts_with_t = computer.starts_with('t');
        for adjacency in adjacency_set {
            let starts_with_t = adjacency.starts_with('t') || computer_starts_with_t;
            let intersect = adjacency_map
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
