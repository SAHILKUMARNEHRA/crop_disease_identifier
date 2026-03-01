# Deployment Guide: Handling Large Model Files

Your AI model file (`model.keras`) is **128MB**, which exceeds GitHub's standard **100MB** limit. Follow these steps to ensure the model is available on Render.

## Option A: Git LFS (Recommended)
Git Large File Storage (LFS) allows you to track large files in your repository.

1.  **Install Git LFS** (if not already installed):
    ```bash
    git lfs install
    ```
2.  **Track the model file**:
    ```bash
    git lfs track "*.keras"
    ```
3.  **Ensure `.gitattributes` is added**:
    ```bash
    git add .gitattributes
    ```
4.  **Remove from `.gitignore`**: Ensure `*.keras` is NOT in your `.gitignore`.
5.  **Push to GitHub**:
    ```bash
    git add model.keras
    git commit -m "chore: add model file via Git LFS"
    git push origin main
    ```

## Option B: Download during Build (Alternative)
If you don't want to use Git LFS, you can host the model on a public URL (Google Drive, Dropbox, S3) and download it during the Render build.

1.  Upload `model.keras` to a cloud drive.
2.  Get a direct download link.
3.  Modify your Render **Build Command**:
    ```bash
    curl -L "YOUR_DOWNLOAD_LINK" -o model.keras && pip install -r requirements.txt
    ```

## How to Check Status
After deploying, visit your backend health URL:
`https://your-app.onrender.com/health`

It should show:
```json
{
  "model_loaded": true,
  "status": "serving"
}
```
If it shows `model_loaded: false`, verify that `model.keras` is present in the root directory.
