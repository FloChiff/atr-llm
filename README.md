# Automatic Text Recognition (ATR) with post-ATR correction with LLM

## Running the ATR Script

### 1. Set Up the Environment

Before running the script, it is recommended to install **Kraken** in a Python virtual environment. This helps isolate dependencies and prevents conflicts with other projects.

```bash
python3 -m venv env_name
source env_name/bin/activate
pip install kraken
````

### 2. Execute the Script

Once Kraken is installed, you can launch the script using the following command:

```bash
python3 atr_kraken.py <images_dir> <output_dir> <segmentation_model> <recognition_model> <output_format>
```

#### Argument Descriptions

* `<images_dir>`: Path to the folder containing the input images
* `<output_dir>`: Path to the folder where output files will be saved
* `<segmentation_model>`: Path to the **segmentation model** (Kraken `.mlmodel`)
* `<recognition_model>`: Path to the **text recognition model** (Kraken `.mlmodel`)
* `<output_format>`: Output format, choose one of the following:

  * `-n`: Plain text (`.txt`)
  * `-a`: ALTO XML format (`.xml`)
  * `-x`: PAGE XML format (`.xml`)

---

## Selecting the Right Models
All the models have been collected from the [Zenodo Kraken](https://zenodo.org/communities/ocr_models/) OCR/HTR models repository.

### Segmentation
| Model Name | Model Filename | Model Link |
|--|--|--|
| General segmentation model for print and handwriting | blla.mlmodel | https://doi.org/10.5281/zenodo.14602569 |
| Kraken segmentation model for vital records | seg_vital_records.mlmodel | https://doi.org/10.5281/zenodo.11913537 |
| Kraken segmentation model for two-column prints | seg_news_1.0.mlmodel | https://doi.org/10.5281/zenodo.10783346 |

### Recognition
| Model Name | Model Filename | Model Link |
|--|--|--|
| CATMuS Medieval | catmus-medieval-1.6.0.mlmodel | https://doi.org/10.5281/zenodo.15030337 |
| CATMuS-Print [Large] | catmus-print-fondue-large.mlmodel | https://doi.org/10.5281/zenodo.10592716 |
| Transcription model for Lucien Peraire's handwriting (French, 20th century) | peraire2_ft_MMCFR.mlmodel | https://doi.org/10.5281/zenodo.8193498 |
| Printed Arabic-Script Base Model Trained on the OpenITI Corpus | all_arabic_scripts.mlmodel | https://doi.org/10.5281/zenodo.7050270 |
| HTR-United - Manu Mc Fondue (Manuscripts of Modern and Contemporaneous French - Manu McFrench v4) | ManuMcFondue.mlmodel | https://doi.org/10.5281/zenodo.10886224 |
| McCATMuS - Transcription model for handwritten, printed and typewritten documents from the 16th century to the 21st century | McCATMuS_nfd_nofix_V1.mlmodel | https://doi.org/10.5281/zenodo.13788177 |