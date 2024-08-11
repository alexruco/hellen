
## Features ✨

- **No recursive Crawling**: Just crawl the provided url 🌐
- **Link Extraction**: Retrieves both internal and external links. 🔗
- **links_on_page(url)**:Retrieves links from a given url

## Installation 💻

Install the package via pip:

```bash
pip install GIT+https://github.com/alexruco/hellen/
```

## Usage 📚

Here's a quick example to get you started:

```python
from hellen import links_on_page
```
# Example usage
result = hellen.links_on_page('https://example.com')
print(result)

## Running Tests 🧪

To run the tests, you can use the unittest module or pytest.

```bash
python -m unittest discover test
# or
pytest
```
## Contributing 🤝

We welcome contributions from the community! Here’s how you can get involved:

1. **Report Bugs**: If you find a bug, please open an issue [here](https://github.com/alexruco/hellen/issues).
2. **Suggest Features**: We’d love to hear your ideas! Suggest new features by opening an issue.
3. **Submit Pull Requests**: Ready to contribute? Fork the repo, make your changes, and submit a pull request. Please ensure your code follows our coding standards and is well-documented.
4. **Improve Documentation**: Help us improve our documentation. Feel free to make edits or add new content.

### How to Submit a Pull Request

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin my-feature-branch`.
5. Open a pull request on the original repository.

## License 📄

This project is licensed under the Apache License 2.0. Feel free to use, modify, and distribute this software in accordance with the terms outlined in the [LICENSE](LICENSE) file.

Named in honor of Ellen MacArthur https://en.wikipedia.org/wiki/Ellen_MacArthur

