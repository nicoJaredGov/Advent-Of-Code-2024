use std::collections::HashMap;
use std::collections::HashSet;
use std::hash::Hash;
use std::io;

pub fn read_filename_from_input() -> String {
    let mut file_name = String::new();

    io::stdin()
        .read_line(&mut file_name)
        .expect("Failed to read input");

    return file_name.trim().to_owned();
}

//builds a graph in the adjacency list format
//format of input is a list of lines where each line is a pair of vertices 'a-b' representing an edge between the two
pub fn build_graph(input: &str, is_directed: bool) -> HashMap<&str, HashSet<&str>> {
    let mut graph: HashMap<&str, HashSet<&str>> = Default::default();

    let pairs = input.lines().map(|line| line.split('-'));

    for mut pair in pairs {
        let first_computer = pair.next().unwrap();
        let second_computer = pair.next().unwrap();

        let first_adjacency_set = graph.entry(first_computer).or_insert(HashSet::new());
        first_adjacency_set.insert(second_computer);

        if !is_directed {
            let second_adjacency_set = graph.entry(second_computer).or_insert(HashSet::new());
            second_adjacency_set.insert(first_computer);
        }
    }

    graph
}

pub fn build_undirected_graph(input: &str) -> HashMap<&str, HashSet<&str>> {
    build_graph(input, false)
}

//algorithm for finding all maximal cliques in a graph
pub fn bron_kerbosch<T: Hash + Eq + Clone + Ord>(
    current_clique: HashSet<T>,
    mut potential_candidates: HashSet<T>,
    mut processed_vertices: HashSet<T>,
    graph: &HashMap<T, HashSet<T>>,
    cliques: &mut HashSet<Vec<T>>,
) {
    if potential_candidates.is_empty() && processed_vertices.is_empty() {
        if current_clique.len() > 2 {
            let mut ordered_clique: Vec<T> = current_clique.iter().cloned().collect();
            ordered_clique.sort();
            cliques.insert(ordered_clique);
        }
        return;
    }

    let pivot = potential_candidates
        .union(&processed_vertices)
        .max_by(|x, y| graph.get(x).iter().len().cmp(&graph.get(y).iter().len()))
        .unwrap();

    let pivot_neighbours = graph.get(pivot).unwrap();
    let candidates = potential_candidates.clone();
    let candidates = candidates.difference(pivot_neighbours);

    for candidate in candidates {
        let mut new_clique = current_clique.clone();
        new_clique.insert(candidate.clone());

        let candidate_neighbours = graph.get(candidate).unwrap();
        let new_potential: HashSet<T> = potential_candidates
            .intersection(candidate_neighbours)
            .cloned()
            .collect();
        let new_processed: HashSet<T> = processed_vertices
            .intersection(candidate_neighbours)
            .cloned()
            .collect();

        bron_kerbosch(new_clique, new_potential, new_processed, graph, cliques);

        potential_candidates.remove(candidate);
        processed_vertices.insert(candidate.clone());
    }
}

pub fn bron_kerbosch_max_only<T: Hash + Eq + Clone + Ord>(
    current_clique: HashSet<T>,
    mut potential_candidates: HashSet<T>,
    mut processed_vertices: HashSet<T>,
    graph: &HashMap<T, HashSet<T>>,
    max_clique: &mut Vec<T>,
) {
    if potential_candidates.is_empty() && processed_vertices.is_empty() {
        if current_clique.len() > 2 && current_clique.len() > max_clique.len() {
            max_clique.clear();
            for v in current_clique.iter() {
                max_clique.push(v.clone());
            }
        }
        return;
    }

    let pivot = potential_candidates
        .union(&processed_vertices)
        .max_by(|x, y| graph.get(x).iter().len().cmp(&graph.get(y).iter().len()))
        .unwrap();

    let pivot_neighbours = graph.get(pivot).unwrap();
    let candidates = potential_candidates.clone();
    let candidates = candidates.difference(pivot_neighbours);

    for candidate in candidates {
        let mut new_clique = current_clique.clone();
        new_clique.insert(candidate.clone());

        let candidate_neighbours = graph.get(candidate).unwrap();
        let new_potential: HashSet<T> = potential_candidates
            .intersection(candidate_neighbours)
            .cloned()
            .collect();
        let new_processed: HashSet<T> = processed_vertices
            .intersection(candidate_neighbours)
            .cloned()
            .collect();

        bron_kerbosch_max_only(new_clique, new_potential, new_processed, graph, max_clique);

        potential_candidates.remove(candidate);
        processed_vertices.insert(candidate.clone());
    }
}

//get a set of 2d coords from a string input
pub fn get_2d_obstacles_set(input: &str) -> HashSet<(i32, i32)> {
    let set: HashSet<(i32, i32)> = input
        .lines()
        .map(|line| {
            let pair = line.split_once(',').unwrap();
            let first = pair.0.trim().parse::<i32>().unwrap();
            let second = pair.1.trim().parse::<i32>().unwrap();
            (first, second)
        })
        .collect();
    set
}
