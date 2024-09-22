use std::process::{Command, exit};

fn main() {
    let output = Command::new("pip")
        .arg("show")
        .arg("black")
        .output()
        .expect("Failed to check if black is installed");

    if !output.status.success() {
        let status = Command::new("pip")
            .arg("install")
            .arg("black")
            .status()
            .expect("Failed to install black");

        if !status.success() {
            eprintln!("Failed to install black");
            exit(1);
        }
    }

    let files = vec!["main.py", "log.py"];
    for file in files {
        let status = Command::new("black")
            .arg(file)
            .status()
            .expect("Failed to format file");

        if !status.success() {
            eprintln!("Failed to format {}", file);
            exit(1);
        }
    }
}
