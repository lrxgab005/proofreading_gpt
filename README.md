# Proofread from pdf scans

## Convert pdf to text

Convert pdf to images
```
mkdir data/images
convert -density 300 PDF -quality 100 -contrast-stretch 40% -blur 3x3 -sharpen 1.5x1.2+1.0+0.10 data/images/part_N_%03d.png
```

Install tesseract
```
brew install tesseract
```

Convert to text
```
for i in *.png; do
  tesseract "$i" "${i%.*}";
done
```

## Correct with chatgpt

```
python proof_reader_gpt.py
```
