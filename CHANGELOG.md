# documents_service CHANGELOG

## [v1.0.10] - 2019-02-28

### Added

- Added a SECRET_KEY - restriction: the `SECRET_KEY` must be provided by the environment

### Changed

- Updated `.gitignore` with `media` - folder for not uploading test-files
- Updated `Document.file_name` and -`file_description` `max_length` to 200

### Removed

- Removed NGINX and static files from the image
