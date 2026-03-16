# File Upload Service

Flask API that accepts any file type and returns live URLs. Automatically handles long filenames and duplicates.

## Live URL
https://file-upload.doless.work

## Endpoints

### Upload File
```bash
curl -F "file=@yourfile.pdf" https://file-upload.doless.work/upload
```

Response:
```json
{
  "success": true,
  "filename": "yourfile.pdf",
  "original_filename": "yourfile.pdf",
  "url": "https://file-upload.doless.work/files/yourfile.pdf",
  "size": 1024
}
```

### Download File
```
GET https://file-upload.doless.work/files/<filename>
```

## Features
- Accepts any file extension
- Max file size: 100MB
- Long filenames (>100 chars) are automatically shortened with hash
- Duplicate filenames get numbered suffix (file_1.txt, file_2.txt)
- Secure filename sanitization

## Examples

```bash
# Upload text file
curl -F "file=@document.txt" https://file-upload.doless.work/upload

# Upload image
curl -F "file=@photo.jpg" https://file-upload.doless.work/upload

# Upload with very long filename (auto-shortened)
curl -F "file=@very_long_filename_that_exceeds_limit.pdf" https://file-upload.doless.work/upload
```
