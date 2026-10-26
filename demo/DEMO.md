# SnapSort Lite demo

These are reproducible, synthetic screenshots generated with Pillow. They are fictional and contain no real user data.

```powershell
python demo/generate_samples.py
python snapsort.py demo/input --output demo/output
python snapsort.py demo/input --output demo/output --apply
Get-ChildItem demo/input
Get-ChildItem demo/output -Recurse
```

The first organizer command is a dry run. The second copies the three images into `Code`, `Documents`, and `Web`, writes `demo/output/manifest.json`, and leaves `demo/input` unchanged. The actual terminal output and directory listings are captured in `terminal-output.txt` when the demo is run.

On the captured run, Pillow generated all three images successfully, but this Windows environment did not have `tesseract.exe` on PATH. The CLI therefore stopped safely with an actionable error before creating output; install Tesseract and rerun the commands above for the full OCR demo.
