use std::io;

pub fn read_filename_from_input() -> String {
    let mut file_name = String::new();

    io::stdin()
        .read_line(&mut file_name)
        .expect("Failed to read input");

    return file_name.trim().to_owned();
}