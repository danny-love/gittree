# gittree

`gittree` is a command-line tool designed to display the directory structure of a Git repository while highlighting files that are tracked by Git. Additionally, it provides functionality to display the contents of tracked files that match a specific pattern.

---

## Features
- Recursively displays the directory tree of a Git repository.
- Highlights files and directories that are tracked by Git.
- Allows users to view the contents of tracked files matching a specified pattern.

---

## Installation

To install `gittree`, use the provided `.deb` package:

```bash
sudo dpkg -i gittree_1.0_all.deb
```

---

## Usage

Once installed, you can run `gittree` from the command line:

### Display the Directory Tree
To display the tree structure of a Git repository, navigate to the repository's root directory and run:

```bash
gittree
```

### View Contents of Specific Files
To view the contents of tracked files matching a pattern, use the `--cat` flag:

```bash
gittree --cat=<pattern>
```

For example, to view the contents of all `.py` files:

```bash
gittree --cat=*.py
```

### Example Output
Running `gittree` in a Git repository might produce the following output:

```
/path/to/repository
├── file1.py
├── file2.txt
└── src
    ├── main.py
    └── utils.py
```

---

## Uninstallation

To remove `gittree` from your system:

```bash
sudo apt remove gittree
```

---

## Development

### Project Structure
```
gittree/
├── DEBIAN/                 # Metadata for the Debian package
│   ├── control             # Package information
│   └── copyright           # License information
├── src/                    # Source code
│   └── gittree.py          # Main executable script
├── build/                  # Build artifacts
│   └── gittree_1.0_all.deb # Generated Debian package
├── LICENSE                 # License file
└── README.md               # Project README
```

### Building the Package

To rebuild the `.deb` package:

1. Ensure the directory structure matches the layout above.
2. Run the following command from the project's root directory:

   ```bash
   dpkg-deb --build gittree
   ```

This will generate the `.deb` package in the `build/` directory.

---

## License

This project is licensed under the terms of the [LICENSE](./LICENSE).

---

## Contact

For questions, suggestions, or bug reports, please contact:

Danny Love
<dannylovehaus@gmail.com>